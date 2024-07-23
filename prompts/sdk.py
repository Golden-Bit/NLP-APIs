import requests
from typing import Any, Dict, List, Optional


class APIClient:
    def __init__(self, api_url: str):
        self.api_url = api_url

    def call_method(self, config_id: str, method: str, args: List[Any], kwargs: Dict[str, Any], is_chat: bool = False) -> Any:
        url = f"{self.api_url}/execute_{'chat_' if is_chat else ''}prompt_method/"
        payload = {
            "config_id": config_id,
            "method_name": method,
            "args": args,
            "kwargs": kwargs
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()["result"]

    def get_attribute(self, config_id: str, attribute: str, is_chat: bool = False) -> Any:
        url = f"{self.api_url}/get_{'chat_' if is_chat else ''}prompt_attribute/"
        payload = {
            "config_id": config_id,
            "attribute_name": attribute
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()["attribute"]


from langchain_core.prompts import PromptTemplate, ChatPromptTemplate

class APIPrompt(PromptTemplate):
    def __init__(self, config_id: str, api_client: APIClient, **kwargs):
        super().__init__(**kwargs)
        self.config_id = config_id
        self.api_client = api_client

    def _run(self, method: str, args: List[Any] = [], kwargs: Dict[str, Any] = {}) -> Any:
        return self.api_client.call_method(self.config_id, method, args, kwargs)

    async def _arun(self, method: str, args: List[Any] = [], kwargs: Dict[str, Any] = {}) -> Any:
        # For simplicity, using synchronous call in async method. In production, you might want to use an async HTTP client.
        return self._run(method, args, kwargs)

    def get_attribute(self, attribute: str) -> Any:
        return self.api_client.get_attribute(self.config_id, attribute)

    @property
    def template(self) -> str:
        return self.get_attribute("template")

    @property
    def input_variables(self) -> List[str]:
        return self.get_attribute("input_variables")

    def format(self, **kwargs: Any) -> str:
        return self._run("format", args=[], kwargs=kwargs)


class APIChatPrompt(ChatPromptTemplate):
    def __init__(self, config_id: str, api_client: APIClient, **kwargs):
        super().__init__(**kwargs)
        self.config_id = config_id
        self.api_client = api_client

    def _run(self, method: str, args: List[Any] = [], kwargs: Dict[str, Any] = {}) -> Any:
        return self.api_client.call_method(self.config_id, method, args, kwargs, is_chat=True)

    async def _arun(self, method: str, args: List[Any] = [], kwargs: Dict[str, Any] = {}) -> Any:
        # For simplicity, using synchronous call in async method. In production, you might want to use an async HTTP client.
        return self._run(method, args, kwargs)

    def get_attribute(self, attribute: str) -> Any:
        return self.api_client.get_attribute(self.config_id, attribute, is_chat=True)

    @property
    def messages(self) -> List[Dict[str, Any]]:
        return self.get_attribute("messages")

    @property
    def input_variables(self) -> List[str]:
        return self.get_attribute("input_variables")

    def format_messages(self, **kwargs: Any) -> List[Dict[str, Any]]:
        return self._run("format_messages", args=[], kwargs=kwargs)
