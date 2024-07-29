from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.callbacks import StreamingStdOutCallbackHandler
import os
import json
#from dotenv import load_dotenv
from chains.experiments.qa_chain import get_chain

app = FastAPI()

texts = [Document("abc"), Document("def"), Document("ghi")]

db = Chroma.from_documents(texts, OpenAIEmbeddings(disallowed_special=()))
retriever = db.as_retriever(
    search_type="mmr",  # Also test "similarity"
    search_kwargs={"k": 8},
)

llm = ChatOpenAI(model="gpt-4")

chain = get_chain(llm=llm, retriever=retriever)

# Load environment variables
#load_dotenv()

# Initialize Langchain LLM
"""llm = ChatOpenAI(
    model_name="gpt-4o",  # Replace with your model
    temperature=0.5,
    max_tokens=2048,
    max_retries=2,
    api_key="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",
    #streaming=False,
    #callbacks=[StreamingStdOutCallbackHandler()]
)
"""


async def generate_response(question: str, stream_only_content: bool = False):
    async for chunk in chain.astream(**{"input": question}):

        if stream_only_content:
            yield chunk.content
        else:
            chunk = chunk.to_json()
            yield json.dumps(chunk) + "\n"


@app.post("/streaming_inference")
async def streaming_inference(request: Request):

    async def generate_response(question: str, stream_only_content: bool = False):

        #llm.streaming = False
        #llm.callbacks = [StreamingStdOutCallbackHandler()]

        async for chunk in chain.astream({"input": question}):
            print(chunk)

            try:
                chunk = json.dumps(chunk, indent=2)
            except Exception as e:
                print(e)
                chunk = "{}"
            yield chunk
            #if stream_only_content:
            #    yield chunk.content
            #else:
            #    chunk = chunk.to_json()
            #    yield json.dumps(chunk)  # + "\n"

    body = await request.json()
    question = body.get("question")
    stream_only_content = body.get("stream_only_content")
    return StreamingResponse(generate_response(question, stream_only_content), media_type="application/json")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
