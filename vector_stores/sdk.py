import requests
from typing import List, Dict, Any, Optional, Tuple
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStore


class APIVectorStore(VectorStore):
    def __init__(self, store_id: str, api_url: str):
        self.store_id = store_id
        self.api_url = api_url

    def _call_method(self, method_name: str, **kwargs: Any) -> Any:
        url = f"{self.api_url}/vector_store/method/{self.store_id}"
        data = {
            "method_name": method_name,
            "kwargs": kwargs
        }
        response = requests.post(url, json=data)
        if response.status_code != 200:
            raise ValueError(f"Error calling method {method_name}: {response.text}")
        return response.json()["result"]

    def _get_attribute(self, attribute_name: str) -> Any:
        url = f"{self.api_url}/vector_store/attribute"
        data = {
            "store_id": self.store_id,
            "attribute_name": attribute_name
        }
        response = requests.post(url, json=data)
        if response.status_code != 200:
            raise ValueError(f"Error getting attribute {attribute_name}: {response.text}")
        return response.json()["attribute"]

    def add_texts(self, texts: List[str], metadatas: Optional[List[Dict[str, Any]]] = None, **kwargs: Any) -> List[str]:
        return self._call_method("add_texts", texts=texts, metadatas=metadatas, **kwargs)

    def similarity_search(self, query: str, k: int = 4, **kwargs: Any) -> List[Document]:
        results = self._call_method("similarity_search", query=query, k=k, **kwargs)
        return [Document(**result) for result in results]

    def max_marginal_relevance_search(self, query: str, k: int = 4, fetch_k: int = 20, lambda_mult: float = 0.5, **kwargs: Any) -> List[Document]:
        results = self._call_method("max_marginal_relevance_search", query=query, k=k, fetch_k=fetch_k, lambda_mult=lambda_mult, **kwargs)
        return [Document(**result) for result in results]

    def delete(self, ids: Optional[List[str]] = None, **kwargs: Any) -> Optional[bool]:
        return self._call_method("delete", ids=ids, **kwargs)

    #@property
    #def embeddings(self) -> Optional[Embeddings]:
    #    embeddings_class = self._get_attribute("embeddings_model_class")
    #    if embeddings_class:
    #        return EMBEDDINGS_MODELS[embeddings_class]()
    #    return None

    def get_by_ids(self, ids: List[str]) -> List[Document]:
        results = self._call_method("get_by_ids", ids=ids)
        return [Document(**result) for result in results]

    def add_documents(self, documents: List[Document], **kwargs: Any) -> List[str]:
        return self._call_method("add_documents", documents=[doc.dict() for doc in documents], **kwargs)

    def similarity_search_with_relevance_scores(self, query: str, k: int = 4, **kwargs: Any) -> List[Tuple[Document, float]]:
        results = self._call_method("similarity_search_with_relevance_scores", query=query, k=k, **kwargs)
        return [(Document(**result[0]), result[1]) for result in results]

    async def asimilarity_search(self, query: str, k: int = 4, **kwargs: Any) -> List[Document]:
        results = self._call_method("similarity_search", query=query, k=k, **kwargs)
        return [Document(**result) for result in results]

    async def asimilarity_search_with_relevance_scores(self, query: str, k: int = 4, **kwargs: Any) -> List[Tuple[Document, float]]:
        results = self._call_method("similarity_search_with_relevance_scores", query=query, k=k, **kwargs)
        return [(Document(**result[0]), result[1]) for result in results]

    async def amax_marginal_relevance_search(self, query: str, k: int = 4, fetch_k: int = 20, lambda_mult: float = 0.5, **kwargs: Any) -> List[Document]:
        results = self._call_method("max_marginal_relevance_search", query=query, k=k, fetch_k=fetch_k, lambda_mult=lambda_mult, **kwargs)
        return [Document(**result) for result in results]

    async def aadd_documents(self, documents: List[Document], **kwargs: Any) -> List[str]:
        return self._call_method("add_documents", documents=[doc.dict() for doc in documents], **kwargs)

    async def aget_by_ids(self, ids: List[str]) -> List[Document]:
        results = self._call_method("get_by_ids", ids=ids)
        return [Document(**result) for result in results]
