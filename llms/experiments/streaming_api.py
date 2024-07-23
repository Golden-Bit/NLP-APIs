from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from langchain_openai import ChatOpenAI
from langchain.callbacks import StreamingStdOutCallbackHandler
import os
import json
#from dotenv import load_dotenv

app = FastAPI()

# Load environment variables
#load_dotenv()

# Initialize Langchain LLM
llm = ChatOpenAI(
    model_name="gpt-4o",  # Replace with your model
    temperature=0.5,
    max_tokens=2048,
    max_retries=2,
    api_key="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",
    #streaming=False,
    #callbacks=[StreamingStdOutCallbackHandler()]
)


async def generate_response(question: str, stream_only_content: bool = False):
    async for chunk in llm.astream(**{"input": question}):

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

        async for chunk in llm.astream(**{"input": question}):

            if stream_only_content:
                yield chunk.content
            else:
                chunk = chunk.to_json()
                yield json.dumps(chunk)  # + "\n"

    body = await request.json()
    question = body.get("question")
    stream_only_content = body.get("stream_only_content")
    return StreamingResponse(generate_response(question, stream_only_content), media_type="application/json")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
