import json
import uuid
from typing import List, Dict, Any
from langchain_community.tools.sql_database.tool import (
    InfoSQLDatabaseTool,
    BaseSQLDatabaseTool,
    ListSQLDatabaseTool,
    QuerySQLCheckerTool,
    InfoSQLDatabaseTool,
    QuerySQLDataBaseTool
)
from langchain_experimental.tools import (PythonREPLTool, PythonAstREPLTool)
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from pydantic import BaseModel, Field
import os
from pymongo import MongoClient
from pydantic import BaseModel
from typing import List, Dict, Any


class ToolConfig(BaseModel):
    config_id: str = Field(..., example="example_tool_config", title="Config ID", description="The unique ID of the tool configuration.")
    tool_class: str = Field(..., example="OpenAITool", title="Tool Class", description="The class of the tool (e.g., 'OpenAITool').")
    tool_kwargs: Dict[str, Any] = Field(..., example={"api_key": "your_api_key"}, title="Tool Arguments", description="The arguments required to initialize the tool.")
    tool_id: str = Field(None, example="123e4567-e89b-12d3-a456-426614174000", title="Tool ID", description="The unique ID of the tool instance.")


class ToolManager:
    def __init__(self, db_collection):
        self.collection = db_collection
        self.available_tools = {
            "PythonREPLTool": PythonREPLTool,
            "PythonAstREPLTool": PythonAstREPLTool,
        }
        self.instantiated_tools = {}

    def add_tool_config(self, tool_config: ToolConfig):
        config = tool_config.dict()
        if self.collection.find_one({"_id": config['config_id']}):
            raise ValueError("Tool Config ID already exists")
        config['_id'] = config['config_id']
        self.collection.insert_one(config)
        return {"message": "Tool Config added successfully"}

    def update_tool_config(self, config_id: str, tool_config: ToolConfig):
        config = tool_config.dict()
        if not self.collection.find_one({"_id": config_id}):
            raise ValueError("Tool Config ID does not exist")
        self.collection.update_one({"_id": config_id}, {"$set": config})
        return {"message": "Tool Config updated successfully"}

    def delete_tool_config(self, config_id: str):
        result = self.collection.delete_one({"_id": config_id})
        if result.deleted_count == 0:
            raise ValueError("Tool Config ID does not exist")
        return {"message": "Tool Config deleted successfully"}

    def get_tool_config(self, config_id: str):
        config = self.collection.find_one({"_id": config_id})
        if not config:
            raise ValueError("Tool Config ID does not exist")
        return config

    def list_tool_configs(self):
        configs = self.collection.find({})
        return [config for config in configs]

    def instantiate_tool(self, config_id: str):
        config = self.get_tool_config(config_id)
        tool_class = config['tool_class']
        tool_kwargs = config['tool_kwargs']
        tool_id = config.get('tool_id', str(uuid.uuid4()))
        if tool_class not in self.available_tools:
            raise ValueError("Tool class not available")
        tool = self.available_tools[tool_class](**tool_kwargs)
        self.instantiated_tools[tool_id] = tool
        return {"tool_id": tool_id, "tool_instance_schema": tool.to_json()}

    def remove_tool_instance(self, tool_id: str):
        if tool_id in self.instantiated_tools:
            del self.instantiated_tools[tool_id]
            return {"message": "Tool instance removed successfully"}
        else:
            raise ValueError("Tool instance ID does not exist")

    def list_tool_instances(self):
        return list(self.instantiated_tools.keys())

    def get_tool(self, tool_id: str):
        return self.instantiated_tools[tool_id]


if __name__ == "__main__":
    p_repl = PythonREPLTool()
    print(p_repl.__repr__())
    print(json.dumps(p_repl.to_json(), indent=2))
