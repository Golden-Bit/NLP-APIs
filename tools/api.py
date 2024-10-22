import json
import os
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Path, Body, APIRouter
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from pymongo import MongoClient
from tools.utilities.tool_manager import ToolManager, ToolConfig

router = APIRouter()

# Configurazione della connessione a MongoDB
MONGO_CONNECTION_STRING = os.getenv('MONGO_CONNECTION_STRING', 'localhost')
client = MongoClient(MONGO_CONNECTION_STRING)
db = client['tool_db']
collection = db['tool_configs']
tool_manager = ToolManager(collection)


class ToolRequest(BaseModel):
    config_id: str = Field(..., example="example_tool_config", title="Config ID", description="The unique ID of the tool configuration.")
    tool_id: str = Field(None, example="123e4567-e89b-12d3-a456-426614174000", title="Tool ID", description="The unique ID of the tool instance.")


class ExecuteMethodRequest(BaseModel):
    tool_id: str = Field(..., example="123e4567-e89b-12d3-a456-426614174000", title="Tool ID", description="The unique ID of the tool instance.")
    method: str = Field(..., example="method_name", title="Method", description="The name of the method to execute.")
    args: Optional[List[Any]] = Field(default_factory=list, example=[], title="Arguments", description="The positional arguments for the method (if any).")
    kwargs: Optional[Dict[str, Any]] = Field(default_factory=dict, example={}, title="Keyword Arguments", description="The keyword arguments for the method (if any).")


class GetAttributeRequest(BaseModel):
    tool_id: str = Field(..., example="123e4567-e89b-12d3-a456-426614174000", title="Tool ID", description="The unique ID of the tool instance.")
    attribute: str = Field(..., example="attribute_name", title="Attribute", description="The name of the attribute to get.")


@router.post("/add_tool_config/", response_description="Add a new tool configuration")
async def add_tool_config(tool_config: ToolConfig = Body(..., example={
    "config_id": "example_tool_config",
    "tool_class": "OpenAITool",
    "tool_kwargs": {"api_key": "your_api_key"},
    #"available_tools": ["OpenAITool", "SQLDatabase", "PythonREPL"]
})):
    """
    Add a new tool configuration to the database.

    - **tool_config**: The tool configuration to add.
    """
    try:
        result = tool_manager.add_tool_config(tool_config)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/update_tool_config/{config_id}", response_description="Update an existing tool configuration")
async def update_tool_config(config_id: str = Path(..., example="example_tool_config", title="Config ID", description="The ID of the tool configuration to update."),
                             tool_config: ToolConfig = Body(..., example={
                                 "config_id": "example_tool_config",
                                 "tool_class": "OpenAITool",
                                 "tool_kwargs": {"api_key": "your_new_api_key"},
                                 #"available_tools": ["OpenAITool", "SQLDatabase", "PythonREPL"]
                             })):
    """
    Update an existing tool configuration in the database.

    - **config_id**: The ID of the tool configuration to update.
    - **tool_config**: The updated tool configuration.
    """
    try:
        result = tool_manager.update_tool_config(config_id, tool_config)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/delete_tool_config/{config_id}", response_description="Delete a tool configuration")
async def delete_tool_config(config_id: str = Path(..., example="example_tool_config", title="Config ID", description="The ID of the tool configuration to delete.")):
    """
    Delete a tool configuration from the database.

    - **config_id**: The ID of the tool configuration to delete.
    """
    try:
        result = tool_manager.delete_tool_config(config_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/get_tool_config/{config_id}", response_description="Retrieve a tool configuration")
async def get_tool_config(config_id: str = Path(..., example="example_tool_config", title="Config ID", description="The ID of the tool configuration to retrieve.")):
    """
    Retrieve a tool configuration from the database.

    - **config_id**: The ID of the tool configuration to retrieve.
    """
    try:
        result = tool_manager.get_tool_config(config_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/list_tool_configs/", response_description="List all tool configurations")
async def list_tool_configs():
    """
    List all tool configurations from the database.
    """
    try:
        result = tool_manager.list_tool_configs()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/instantiate_tool/", response_description="Instantiate a tool based on its configuration")
async def instantiate_tool(request: ToolRequest):
    """
    Instantiate a tool based on its configuration.

    - **request**: Contains the tool configuration ID.
    """
    try:
        tool = tool_manager.instantiate_tool(request.config_id)

        return tool
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/remove_tool_instance/", response_description="Remove a tool instance")
async def remove_tool_instance(request: ToolRequest):
    """
    Remove a tool instance.

    - **request**: Contains the tool instance ID.
    """
    try:
        result = tool_manager.remove_tool_instance(request.tool_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/get_tool_instance/{tool_id}", response_description="Get the JSON representation of a tool instance")
async def get_tool_instance(tool_id: str = Path(..., example="123e4567-e89b-12d3-a456-426614174000", title="Tool ID", description="The unique ID of the tool instance.")):
    """
    Get the JSON representation of a tool instance.

    - **tool_id**: The unique ID of the tool instance.
    """
    try:
        tool_instance = tool_manager.instantiated_tools.get(tool_id)
        if tool_instance is None:
            raise ValueError("Tool instance ID does not exist")
        return tool_instance.to_json() #json.loads(json.dumps(tool_instance, default=lambda o: o.__dict__, indent=2))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/list_tool_instances/", response_description="List all tool instance IDs")
async def list_tool_instances():
    """
    List all tool instance IDs.
    """
    try:
        result = tool_manager.list_tool_instances()
        return result
    except ValueError as e:
        return HTTPException(status_code=400, detail=str(e))


@router.post("/execute_tool_method/", response_description="Execute a method of a tool instance")
async def execute_tool_method(request: ExecuteMethodRequest):
    """
    Execute a method of a tool instance.

    - **tool_id**: The unique ID of the tool instance.
    - **method**: The name of the method to execute.
    - **args**: The positional arguments for the method (if any).
    - **kwargs**: The keyword arguments for the method (if any).
    """
    tool_id = request.tool_id
    method_name = request.method
    args = request.args
    kwargs = request.kwargs

    try:
        tool_instance = tool_manager.instantiated_tools.get(tool_id)
        if tool_instance is None:
            raise ValueError("Tool instance ID does not exist")

        if not hasattr(tool_instance, method_name):
            raise ValueError(f"Method '{method_name}' does not exist on tool instance")

        method = getattr(tool_instance, method_name)

        if callable(method):
            result = method(*args, **kwargs)
            return {"result": result}
        else:
            raise ValueError(f"'{method_name}' is not a callable method")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/get_tool_attribute/", response_description="Get an attribute of a tool instance")
async def get_tool_attribute(request: GetAttributeRequest):
    """
    Get an attribute of a tool instance.

    - **tool_id**: The unique ID of the tool instance.
    - **attribute**: The name of the attribute to get.
    """
    tool_id = request.tool_id
    attribute_name = request.attribute

    try:
        tool_instance = tool_manager.instantiated_tools.get(tool_id)
        if tool_instance is None:
            raise ValueError("Tool instance ID does not exist")

        if not hasattr(tool_instance, attribute_name):
            raise ValueError(f"Attribute '{attribute_name}' does not exist on tool instance")

        attribute = getattr(tool_instance, attribute_name)
        return {"attribute": attribute}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    app = FastAPI()

    app.include_router(router, prefix="/tools", tags=["tools"])

    uvicorn.run(app, host="127.0.0.1", port=8108)
