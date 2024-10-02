from openai import OpenAI

# Set the API base URL to your VLLM server
api_base = "http://127.0.0.1:8100/v1"
api_key = "EMPTY"  # The API key is ignored for local servers

# Initialize the OpenAI client
client = OpenAI(
    base_url=api_base,
    api_key=api_key,
)

# Make a streaming request
response = client.chat.completions.create(
    model="Qwen/Qwen2-1.5B-Instruct",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "write me a very log poem about meaning of life"},
    ],
    stream=True  # Enable streaming
)

# Process and print the streamed responses token by token
for chunk in response:
    print(chunk)
    #if "choices" in chunk and len(chunk.choices) > 0:
        #delta = chunk.choices[0].delta
        #print(delta)
        #content = delta.get("content", "")
        #if content:
        #    print(content, end="", flush=True)

print("\nStreaming complete.")
