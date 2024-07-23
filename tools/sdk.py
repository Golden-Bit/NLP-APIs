import requests
from typing import Any, Dict, List, Optional
from pydantic import BaseModel
from langchain_core.tools import BaseTool


class APIClient:
    def __init__(self, api_url: str):
        self.api_url = api_url

    def call_method(self, tool_id: str, method: str, args: List[Any], kwargs: Dict[str, Any]) -> Any:
        url = f"{self.api_url}/execute_tool_method/"
        payload = {
            "tool_id": tool_id,
            "method": method,
            "args": args,
            "kwargs": kwargs
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()["result"]

    def get_attribute(self, tool_id: str, attribute: str) -> Any:
        url = f"{self.api_url}/get_tool_attribute/"
        payload = {
            "tool_id": tool_id,
            "attribute": attribute
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()["attribute"]

    def add_tool_config(self, tool_config: Dict[str, Any]) -> Any:
        url = f"{self.api_url}/add_tool_config/"
        response = requests.post(url, json=tool_config)
        response.raise_for_status()
        return response.json()

    def update_tool_config(self, config_id: str, tool_config: Dict[str, Any]) -> Any:
        url = f"{self.api_url}/update_tool_config/{config_id}"
        response = requests.put(url, json=tool_config)
        response.raise_for_status()
        return response.json()

    def delete_tool_config(self, config_id: str) -> Any:
        url = f"{self.api_url}/delete_tool_config/{config_id}"
        response = requests.delete(url)
        response.raise_for_status()
        return response.json()

    def get_tool_config(self, config_id: str) -> Any:
        url = f"{self.api_url}/get_tool_config/{config_id}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def list_tool_configs(self) -> Any:
        url = f"{self.api_url}/list_tool_configs/"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def instantiate_tool(self, config_id: str) -> Any:
        url = f"{self.api_url}/instantiate_tool/"
        payload = {"config_id": config_id}
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()

    def remove_tool_instance(self, tool_id: str) -> Any:
        url = f"{self.api_url}/remove_tool_instance/"
        payload = {"tool_id": tool_id}
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()

    def get_tool_instance(self, tool_id: str) -> Any:
        url = f"{self.api_url}/get_tool_instance/{tool_id}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def list_tool_instances(self) -> Any:
        url = f"{self.api_url}/list_tool_instances/"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()


class APITool(BaseTool):
    def __init__(self, tool_id: str, api_client: APIClient, **kwargs):
        super().__init__(**kwargs)
        self.tool_id = tool_id
        self.api_client = api_client

    def _run(self, method: str, args: List[Any] = [], kwargs: Dict[str, Any] = {}) -> Any:
        return self.api_client.call_method(self.tool_id, method, args, kwargs)

    async def _arun(self, method: str, args: List[Any] = [], kwargs: Dict[str, Any] = {}) -> Any:
        # For simplicity, using synchronous call in async method. In production, you might want to use an async HTTP client.
        return self._run(method, args, kwargs)

    def get_attribute(self, attribute: str) -> Any:
        return self.api_client.get_attribute(self.tool_id, attribute)

    @property
    def description(self) -> str:
        return self.get_attribute("description")

    @property
    def name(self) -> str:
        return self.get_attribute("name")

    @property
    def args_schema(self) -> BaseModel:
        # Assuming the args schema is returned as a JSON schema from the attribute call
        schema = self.get_attribute("args_schema")
        return BaseModel.parse_obj(schema)

