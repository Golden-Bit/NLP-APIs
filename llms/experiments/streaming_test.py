import requests

def stream_response(url, payload):
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, json=payload, headers=headers, stream=True)

    if response.status_code == 200:
        full_content = ""
        for content in response.iter_content(decode_unicode=True): #.iter_lines(decode_unicode=True):
            if content:
                full_content += content
                print(full_content + "|")
    else:
        print(f"Request failed with status code {response.status_code}")

if __name__ == "__main__":
    url = "http://127.0.0.1:8106/llms/streaming_inference/"
    payload = {
        "model_id": "chat-openai_gpt-4o",
        "prompt": "Scrivimi un poema di due pagine sul senso della vita.",
        "stream_only_content": True
    }
    stream_response(url, payload)
