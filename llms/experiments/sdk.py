import requests
from typing import Any, Dict, List, Optional
from langchain_core.callbacks import BaseCallbackManager
from typing import Any, Dict, List, Optional, Type

from langchain_core.language_models import BaseLLM


class APIClient:
    def __init__(self, api_url: str):
        self.api_url = api_url

    def call_method(self, model_id: str, method: str, args: List[Any], kwargs: Dict[str, Any]) -> Any:
        url = f"{self.api_url}/model_method/{model_id}"
        payload = {
            "method_name": method,
            "kwargs": kwargs
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()["result"]

    def get_attribute(self, model_id: str, attribute: str) -> Any:
        url = f"{self.api_url}/get_model_attribute/"
        payload = {
            "model_id": model_id,
            "attribute_name": attribute
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()["attribute"]


class APILanguageModel(BaseLLM):
    def __init__(self, model_id: str, api_client: APIClient, **kwargs):
        super().__init__(**kwargs)
        self.model_id = model_id
        self.api_client = api_client

    def _run(self, method: str, args: List[Any] = [], kwargs: Dict[str, Any] = {}) -> Any:
        return self.api_client.call_method(self.model_id, method, args, kwargs)

    async def _arun(self, method: str, args: List[Any] = [], kwargs: Dict[str, Any] = {}) -> Any:
        return self._run(method, args, kwargs)

    def get_attribute(self, attribute: str) -> Any:
        return self.api_client.get_attribute(self.model_id, attribute)

    @property
    def _llm_type(self) -> str:
        return self.get_attribute("_llm_type")

    def _call(self, prompt: str, stop: Optional[List[str]] = None, run_manager: Optional[BaseCallbackManager] = None, **kwargs: Any) -> str:
        return self._run("generate", args=[prompt], kwargs=kwargs)

    async def _acall(self, prompt: str, stop: Optional[List[str]] = None, run_manager: Optional[BaseCallbackManager] = None, **kwargs: Any) -> str:
        return await self._arun("generate", args=[prompt], kwargs=kwargs)
