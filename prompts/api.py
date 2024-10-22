import os
from fastapi import FastAPI, HTTPException, Path, Body, APIRouter
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from pymongo import MongoClient
from prompts.utilities.prompt_manager import PromptManager, PromptConfig, ChatPromptConfig

router = APIRouter()

# Configurazione della connessione a MongoDB
MONGO_CONNECTION_STRING = os.getenv('MONGO_CONNECTION_STRING', 'localhost')
client = MongoClient(MONGO_CONNECTION_STRING)
db = client['prompt_db']
collection = db['prompt_configs']

prompt_manager = PromptManager(collection)



class ExecutePromptMethodRequest(BaseModel):
    config_id: str = Field(..., example="example_prompt_config", title="Config ID", description="The unique ID of the prompt configuration.")
    method_name: str = Field(..., example="some_method", title="Method Name", description="The name of the method to call on the prompt.")
    args: Optional[List[Any]] = Field(default_factory=list, example=[], title="Arguments", description="The positional arguments for the method (if any).")
    kwargs: Optional[Dict[str, Any]] = Field(default_factory=dict, example={"param1": "value1", "param2": "value2"}, title="Keyword Arguments", description="The keyword arguments for the method (if any).")


class GetPromptAttributeRequest(BaseModel):
    config_id: str = Field(..., example="example_prompt_config", title="Config ID", description="The unique ID of the prompt configuration.")
    attribute_name: str = Field(..., example="attribute_name", title="Attribute Name", description="The name of the attribute to get.")


class ExecuteChatPromptMethodRequest(BaseModel):
    config_id: str = Field(..., example="example_chat_prompt_config", title="Config ID", description="The unique ID of the chat prompt configuration.")
    method_name: str = Field(..., example="some_method", title="Method Name", description="The name of the method to call on the chat prompt.")
    args: Optional[List[Any]] = Field(default_factory=list, example=[], title="Arguments", description="The positional arguments for the method (if any).")
    kwargs: Optional[Dict[str, Any]] = Field(default_factory=dict, example={"param1": "value1", "param2": "value2"}, title="Keyword Arguments", description="The keyword arguments for the method (if any).")


class GetChatPromptAttributeRequest(BaseModel):
    config_id: str = Field(..., example="example_chat_prompt_config", title="Config ID", description="The unique ID of the chat prompt configuration.")
    attribute_name: str = Field(..., example="attribute_name", title="Attribute Name", description="The name of the attribute to get.")


class PromptRequest(BaseModel):
    config_id: str = Field(..., example="example_prompt_config", title="Config ID", description="The unique ID of the prompt configuration.")
    variables: Dict[str, Any] = Field(..., example={"adjective": "funny", "content": "chickens"}, title="Variables", description="The variables to format the prompt template.")
    is_partial: bool = Field(False, example=False, title="Partial", description="Whether to perform partial formatting.")
    is_format: bool = Field(False, example=False, title="Format", description="Whether to perform full formatting.")


class ChatPromptRequest(BaseModel):
    config_id: str = Field(..., example="example_chat_prompt_config", title="Config ID", description="The unique ID of the chat prompt configuration.")
    variables: Dict[str, Any] = Field(..., example={"name": "Bob", "user_input": "What is your name?"}, title="Variables", description="The variables to format the chat prompt template.")
    is_partial: bool = Field(False, example=False, title="Partial", description="Whether to perform partial formatting.")
    is_format: bool = Field(False, example=False, title="Format", description="Whether to perform full formatting.")

@router.post("/add_prompt_config/", response_description="Add a new prompt configuration")
async def add_prompt_config(prompt_config: PromptConfig = Body(..., example={
    "config_id": "example_prompt_config",
    "template": "Tell me a {adjective} joke about {content}.",
    "type": "string",
    "variables": ["adjective", "content"]
})):
    """
    Add a new prompt configuration to the database.

    - **prompt_config**: The prompt configuration to add.
    """
    try:
        result = prompt_manager.add_prompt_config(prompt_config)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/add_chat_prompt_config/", response_description="Add a new chat prompt configuration")
async def add_chat_prompt_config(chat_prompt_config: ChatPromptConfig = Body(..., example={
    "config_id": "example_chat_prompt_config",
    "messages": [
        {"role": "system", "content": "You are a helpful AI bot. Your name is {name}."},
        {"role": "human", "content": "Hello, how are you doing?"},
        {"role": "ai", "content": "I'm doing well, thanks!"},
        {"role": "human", "content": "{user_input}"}
    ],
    "variables": ["name", "user_input"]
})):
    """
    Add a new chat prompt configuration to the database.

    - **chat_prompt_config**: The chat prompt configuration to add.
    """
    try:
        result = prompt_manager.add_chat_prompt_config(chat_prompt_config)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/update_prompt_config/{config_id}", response_description="Update an existing prompt configuration")
async def update_prompt_config(config_id: str = Path(..., example="example_prompt_config", title="Config ID", description="The ID of the prompt configuration to update."),
                               prompt_config: PromptConfig = Body(..., example={
                                   "config_id": "example_prompt_config",
                                   "template": "Tell me a {adjective} story about {content}.",
                                   "type": "string",
                                   "variables": ["adjective", "content"]
                               })):
    """
    Update an existing prompt configuration in the database.

    - **config_id**: The ID of the prompt configuration to update.
    - **prompt_config**: The updated prompt configuration.
    """
    try:
        result = prompt_manager.update_prompt_config(config_id, prompt_config)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/update_chat_prompt_config/{config_id}", response_description="Update an existing chat prompt configuration")
async def update_chat_prompt_config(config_id: str = Path(..., example="example_chat_prompt_config", title="Config ID", description="The ID of the chat prompt configuration to update."),
                                    chat_prompt_config: ChatPromptConfig = Body(..., example={
                                        "config_id": "example_chat_prompt_config",
                                        "messages": [
                                            {"role": "system", "content": "You are a helpful AI bot. Your name is {name}."},
                                            {"role": "human", "content": "Hello, how are you doing?"},
                                            {"role": "ai", "content": "I'm doing well, thanks!"},
                                            {"role": "human", "content": "{user_input}"}
                                        ],
                                        "variables": ["name", "user_input"]
                                    })):
    """
    Update an existing chat prompt configuration in the database.

    - **config_id**: The ID of the chat prompt configuration to update.
    - **chat_prompt_config**: The updated chat prompt configuration.
    """
    try:
        result = prompt_manager.update_chat_prompt_config(config_id, chat_prompt_config)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/delete_prompt_config/{config_id}", response_description="Delete a prompt configuration")
async def delete_prompt_config(config_id: str = Path(..., example="example_prompt_config", title="Config ID", description="The ID of the prompt configuration to delete.")):
    """
    Delete a prompt configuration from the database.

    - **config_id**: The ID of the prompt configuration to delete.
    """
    try:
        result = prompt_manager.delete_prompt_config(config_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/delete_chat_prompt_config/{config_id}", response_description="Delete a chat prompt configuration")
async def delete_chat_prompt_config(config_id: str = Path(..., example="example_chat_prompt_config", title="Config ID", description="The ID of the chat prompt configuration to delete.")):
    """
    Delete a chat prompt configuration from the database.

    - **config_id**: The ID of the chat prompt configuration to delete.
    """
    try:
        result = prompt_manager.delete_chat_prompt_config(config_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/get_prompt_config/{config_id}", response_description="Retrieve a prompt configuration")
async def get_prompt_config(config_id: str = Path(..., example="example_prompt_config", title="Config ID", description="The ID of the prompt configuration to retrieve.")):
    """
    Retrieve a prompt configuration from the database.

    - **config_id**: The ID of the prompt configuration to retrieve.
    """
    try:
        result = prompt_manager.get_prompt_config(config_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/get_chat_prompt_config/{config_id}", response_description="Retrieve a chat prompt configuration")
async def get_chat_prompt_config(config_id: str = Path(..., example="example_chat_prompt_config", title="Config ID", description="The ID of the chat prompt configuration to retrieve.")):
    """
    Retrieve a chat prompt configuration from the database.

    - **config_id**: The ID of the chat prompt configuration to retrieve.
    """
    try:
        result = prompt_manager.get_chat_prompt_config(config_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/get_prompt/", response_description="Instantiate a prompt based on its configuration and variables")
async def get_prompt(request: PromptRequest):
    """
    Instantiate a prompt based on its configuration and provided variables.

    - **request**: Contains the prompt configuration ID, variables to format the prompt, whether to perform partial formatting, and whether to perform full formatting.
    """
    try:
        result = prompt_manager.get_prompt(request.config_id, request.variables, request.is_partial, request.is_format)
        return {"prompt": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/get_chat_prompt/", response_description="Instantiate a chat prompt based on its configuration and variables")
async def get_chat_prompt(request: ChatPromptRequest):
    """
    Instantiate a chat prompt based on its configuration and provided variables.

    - **request**: Contains the chat prompt configuration ID, variables to format the chat prompt, whether to perform partial formatting, and whether to perform full formatting.
    """
    try:
        result = prompt_manager.get_chat_prompt(request.config_id, request.variables, request.is_partial, request.is_format)
        return {"chat_prompt": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/list_prompt_configs/", response_description="List all prompt configurations")
async def list_prompt_configs():
    """
    List all prompt configurations from the database.
    """
    try:
        result = prompt_manager.list_prompt_configs()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/list_chat_prompt_configs/", response_description="List all chat prompt configurations")
async def list_chat_prompt_configs():
    """
    List all chat prompt configurations from the database.
    """
    try:
        result = prompt_manager.list_chat_prompt_configs()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/execute_prompt_method/", response_description="Execute a method of a prompt instance")
async def execute_prompt_method(request: ExecutePromptMethodRequest):
    """
    Execute a method of a prompt instance.

    - **config_id**: The unique ID of the prompt configuration.
    - **method_name**: The name of the method to execute.
    - **args**: The positional arguments for the method (if any).
    - **kwargs**: The keyword arguments for the method (if any).
    """
    try:
        prompt_instance = prompt_manager.get_prompt(request.config_id, {}, is_partial=False, is_format=False)
        if not hasattr(prompt_instance, request.method_name):
            raise ValueError(f"Method '{request.method_name}' does not exist on prompt instance")

        method = getattr(prompt_instance, request.method_name)
        if callable(method):
            result = method(*request.args, **request.kwargs)
            return {"result": result}
        else:
            raise ValueError(f"'{request.method_name}' is not a callable method")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/get_prompt_attribute/", response_description="Get an attribute of a prompt instance")
async def get_prompt_attribute(request: GetPromptAttributeRequest):
    """
    Get an attribute of a prompt instance.

    - **config_id**: The unique ID of the prompt configuration.
    - **attribute_name**: The name of the attribute to get.
    """
    try:
        prompt_instance = prompt_manager.get_prompt(request.config_id, {}, False)
        if not hasattr(prompt_instance, request.attribute_name):
            raise ValueError(f"Attribute '{request.attribute_name}' does not exist on prompt instance")

        attribute = getattr(prompt_instance, request.attribute_name)
        return {"attribute": attribute}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/execute_chat_prompt_method/", response_description="Execute a method of a chat prompt instance")
async def execute_chat_prompt_method(request: ExecuteChatPromptMethodRequest):
    """
    Execute a method of a chat prompt instance.

    - **config_id**: The unique ID of the chat prompt configuration.
    - **method_name**: The name of the method to execute.
    - **args**: The positional arguments for the method (if any).
    - **kwargs**: The keyword arguments for the method (if any).
    """
    try:
        chat_prompt_instance = prompt_manager.get_chat_prompt(request.config_id, {}, is_partial=False, is_format=False)
        if not hasattr(chat_prompt_instance, request.method_name):
            raise ValueError(f"Method '{request.method_name}' does not exist on chat prompt instance")

        method = getattr(chat_prompt_instance, request.method_name)
        if callable(method):
            result = method(*request.args, **request.kwargs)
            return {"result": result}
        else:
            raise ValueError(f"'{request.method_name}' is not a callable method")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/get_chat_prompt_attribute/", response_description="Get an attribute of a chat prompt instance")
async def get_chat_prompt_attribute(request: GetChatPromptAttributeRequest):
    """
    Get an attribute of a chat prompt instance.

    - **config_id**: The unique ID of the chat prompt configuration.
    - **attribute_name**: The name of the attribute to get.
    """
    try:
        chat_prompt_instance = prompt_manager.get_chat_prompt(request.config_id, {}, False)
        if not hasattr(chat_prompt_instance, request.attribute_name):
            raise ValueError(f"Attribute '{request.attribute_name}' does not exist on chat prompt instance")

        attribute = getattr(chat_prompt_instance, request.attribute_name)
        return {"attribute": attribute}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    app = FastAPI()

    app.include_router(router, prefix="/prompts", tags=["prompts"])

    uvicorn.run(app, host="127.0.0.1", port=8107)
