import asyncio
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# Step 1: Initialize the ChatOpenAI instance to use the VLLM server
llm = ChatOpenAI(
    model="Qwen/Qwen2-7B-Instruct-AWQ",  # Specify the model name
    openai_api_key="EMPTY",  # API key is ignored for local VLLM server
    openai_api_base="http://34.78.163.86:8099/v1",  # Base URL of your VLLM server
    streaming=True  # Enable streaming
)

# Step 2: Define the conversation messages
messages = [
    #SystemMessage(content="You are a helpful assistant."),  # System message
    HumanMessage(content="write me a very log poem about meaning of life")  # User message
]

# Step 3: Asynchronous function to stream the response and print each token
async def main():
    async for token in llm.astream(messages):
        print(token)
        #print(token["choices"][0]["delta"]["content"], end="", flush=True)

# Run the asynchronous function
if __name__ == "__main__":
    print("#"*120)
    asyncio.run(main())
