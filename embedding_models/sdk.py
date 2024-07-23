import requests
from typing import Any, Dict, List, Optional
from langchain_core.embeddings import Embeddings
from typing import Any, List
from langchain_core.runnables import run_in_executor


class APIClient:
    def __init__(self, api_url: str):
        self.api_url = api_url

    def call_method(self, model_id: str, method: str, args: List[Any], kwargs: Dict[str, Any]) -> Any:
        url = f"{self.api_url}/execute_embedding_method/"
        payload = {
            "model_id": model_id,
            "method_name": method,
            "args": args,
            "kwargs": kwargs
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()["result"]

    def get_attribute(self, model_id: str, attribute: str) -> Any:
        url = f"{self.api_url}/get_embedding_attribute/"
        payload = {
            "model_id": model_id,
            "attribute_name": attribute
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()["attribute"]


class APIEmbeddings(Embeddings):
    def __init__(self, model_id: str, api_client: APIClient):
        self.model_id = model_id
        self.api_client = api_client

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self.api_client.call_method(self.model_id, "embed_documents", [texts], {})

    def embed_query(self, text: str) -> List[float]:
        return self.api_client.call_method(self.model_id, "embed_query", [text], {})

    async def aembed_documents(self, texts: List[str]) -> List[List[float]]:
        return await run_in_executor(None, self.embed_documents, texts)

    async def aembed_query(self, text: str) -> List[float]:
        return await run_in_executor(None, self.embed_query, text)