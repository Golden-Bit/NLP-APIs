import json
import os
from typing import Dict, Any, Optional

from fastapi import FastAPI, APIRouter, HTTPException, Path, Body
from langchain_core.callbacks import StreamingStdOutCallbackHandler
from pydantic import BaseModel, Field
import uuid

from starlette.responses import StreamingResponse
from starlette.websockets import WebSocket

from llms.utilities.model_manager import ModelManager
from pymongo import MongoClient

# MongoDB connection setup
MONGO_CONNECTION_STRING = os.getenv('MONGO_CONNECTION_STRING', 'localhost')
client = MongoClient(MONGO_CONNECTION_STRING)
db = client['model_config_db']
collection = db['model_configs']

model_manager = ModelManager()

# FastAPI router setup
router = APIRouter()


class ExecuteMethodRequest(BaseModel):
    model_id: str = Field(..., example="example_model", title="Model ID", description="The ID of the model.")
    method_name: str = Field(..., example="generate", title="Method Name", description="The name of the method to call on the model.")
    args: Optional[list] = Field(default_factory=list, example=[], title="Arguments", description="The positional arguments for the method (if any).")
    kwargs: Optional[Dict[str, Any]] = Field(default_factory=dict, example={}, title="Keyword Arguments", description="The keyword arguments for the method (if any).")


class GetAttributeRequest(BaseModel):
    model_id: str = Field(..., example="example_model", title="Model ID", description="The ID of the model.")
    attribute_name: str = Field(..., example="attribute_name", title="Attribute Name", description="The name of the attribute to get.")


class ModelConfigRequest(BaseModel):
    config_id: str = Field(..., example="example_configuration", title="Config ID", description="The unique ID of the model configuration.")
    model_id: str = Field(..., example="example_model", title="Model ID", description="The unique ID of the model.")
    #model_name: str = Field(..., example="gpt-3", title="Model Name", description="The name of the model.")
    model_type: str = Field(..., example="openai", title="Model Type",
                            description="The type of the model (e.g., 'openai', 'vllm').")
    model_kwargs: dict = Field(default_factory=dict, example={"temperature": 0.7}, title="Model Kwargs",
                               description="Additional keyword arguments for model initialization.")


class InferenceRequest(BaseModel):
    model_id: str = Field(..., example="example_model", title="Model ID",
                          description="The ID of the model to use for inference.")
    prompt: str = Field(..., example="What is the capital of France?", title="Prompt",
                        description="The input prompt for the model.")
    inference_kwargs: dict = Field(default_factory=dict, example={"max_tokens": 50}, title="Inference Kwargs",
                                   description="Additional keyword arguments for inference.")


class StreamingInferenceRequest(BaseModel):
    model_id: str = Field(..., example="example_model", title="Model ID",
                          description="The ID of the model to use for inference.")
    prompt: str = Field(..., example="What is the capital of France?", title="Prompt",
                        description="The input prompt for the model.")
    inference_kwargs: dict = Field(default_factory=dict, example={"max_tokens": 50}, title="Inference Kwargs",
                                   description="Additional keyword arguments for inference.")
    stream_only_content: bool = Field(False, example=False, title="Stream Only Content",
                                      description="Flag used to stream only directly content or full json output.")


# New class for method execution requests
class MethodRequest(BaseModel):
    method_name: str = Field(..., example="generate", title="Method Name",
                             description="The name of the method to call on the model.")
    kwargs: Dict[str, Any] = Field(default_factory=dict, example={"max_tokens": 50}, title="Method Kwargs",
                                   description="Additional keyword arguments for the method.")


@router.post("/configure_model/")
async def configure_model(request: ModelConfigRequest):
    """
    Configures a new model and stores its configuration.
    """

    config = request.dict()

    config_id = config["config_id"]
    model_id = config["model_id"]

    if config_id is None:
        config_id = str(uuid.uuid4())
    if model_id is None:
        model_id = str(uuid.uuid4())

    if collection.find_one({"_id": config_id}):
        raise HTTPException(status_code=400, detail="Configuration ID already exists")

    #config_id = str(uuid.uuid4())
    #config = request.dict()
    config["_id"] = config_id
    config["model_id"] = model_id
    collection.insert_one(config)
    return {"config_id": config_id}


@router.post("/load_model/{config_id}")
def load_model(
        config_id: str = Path(..., example="abcd1234-efgh-5678-ijkl-9012mnop3456", title="Config ID",
                              description="The configuration ID of the model to load.")
):
    """
    Loads a model based on its configuration ID.
    """
    try:
        model_manager.load_model(config_id)
        return {"message": "Model loaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/unload_model/{model_id}")
async def unload_model(
        model_id: str = Path(..., example="example_model", title="Model ID",
                             description="The ID of the model to unload.")
):
    """
    Unloads a model from memory.
    """
    model_manager.unload_model(model_id)
    return {"message": "Model unloaded successfully"}


@router.post("/inference/")
async def inference(request: InferenceRequest):
    """
    Performs inference using a loaded model.
    """
    model = model_manager.get_model(request.model_id)
    if model is None:
        raise HTTPException(status_code=404, detail="Model not found")
    response = model.invoke(request.prompt, **request.inference_kwargs)
    return {"response": response}


@router.post("/streaming_inference/")
async def streaming_inference(request: StreamingInferenceRequest):

    """
    Performs streaming inference using a loaded model.
    """

    async def generate_response(model: Any,
                                prompt: str,
                                stream_only_content: bool = False,
                                inference_kwargs: Optional[Dict[str, Any]] = None):

        inference_kwargs = inference_kwargs if inference_kwargs else {}
        inference_kwargs["input"] = prompt
        async for chunk in model.astream(**inference_kwargs):

            if stream_only_content:
                yield chunk.content
            else:
                chunk = chunk.to_json()
                yield json.dumps(chunk)

    model = model_manager.get_model(request.model_id)

    if model is None:
        raise HTTPException(status_code=404, detail="Model not found")

    #model.streaming = True
    #model.callbacks = [StreamingStdOutCallbackHandler()]

    prompt = request.prompt
    stream_only_content = request.stream_only_content
    inference_kwargs = request.inference_kwargs

    return StreamingResponse(generate_response(model, prompt, stream_only_content, inference_kwargs), media_type="application/json")


@router.post("/model_method/{model_id}")  # New endpoint for method execution
async def execute_model_method(
        model_id: str = Path(..., example="example_model", title="Model ID", description="The ID of the model."),
        request: MethodRequest = Body(...)
):
    """
    Executes a specific method on a loaded model.
    """
    model = model_manager.get_model(model_id)
    if model is None:
        raise HTTPException(status_code=404, detail="Model not found")

    if not hasattr(model, request.method_name):
        raise HTTPException(status_code=400, detail=f"Method {request.method_name} not found on model {model_id}")

    method = getattr(model, request.method_name)
    result = method(**request.kwargs)

    return {"detail": f"Method {request.method_name} executed successfully on model {model_id}", "result": result}


@router.post("/get_model_attribute/", response_description="Get an attribute of a model instance")
async def get_model_attribute(request: GetAttributeRequest):
    """
    Get an attribute of a model instance.

    - **model_id**: The unique ID of the model instance.
    - **attribute_name**: The name of the attribute to get.
    """
    model_id = request.model_id
    attribute_name = request.attribute_name

    try:
        model_instance = model_manager.get_model(model_id)
        if model_instance is None:
            raise ValueError("Model instance ID does not exist")

        if not hasattr(model_instance, attribute_name):
            raise ValueError(f"Attribute '{attribute_name}' does not exist on model instance")

        attribute = getattr(model_instance, attribute_name)
        return {"attribute": attribute}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/configurations/")
async def list_configurations():
    """
    Lists all stored model configurations.
    """
    configs = collection.find({})
    return [
        {
            "config_id": config["_id"],
            "model_id": config["model_id"],
            #"model_name": config["model_name"],
            "model_type": config["model_type"],
            "model_kwargs": config.get("model_kwargs", {})
        } for config in configs
    ]


@router.get("/configuration/{config_id}")
async def get_configuration(
        config_id: str = Path(..., example="abcd1234-efgh-5678-ijkl-9012mnop3456", title="Config ID",
                              description="The configuration ID to retrieve.")
):
    """
    Retrieves a specific model configuration.
    """
    config = collection.find_one({"_id": config_id})
    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")
    return config


@router.delete("/configuration/{config_id}")
async def delete_configuration(
        config_id: str = Path(..., example="abcd1234-efgh-5678-ijkl-9012mnop3456", title="Config ID",
                              description="The configuration ID to delete.")
):
    """
    Deletes a specific model configuration.
    """
    result = collection.delete_one({"_id": config_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Configuration not found")
    return {"detail": "Configuration deleted successfully"}


@router.get("/loaded_models/")
async def list_loaded_models():
    """
    Lists all currently loaded models.
    """
    return model_manager.list_loaded_models()


if __name__ == "__main__":
    import uvicorn

    app = FastAPI()

    app.include_router(router, prefix="/llms", tags=["llms"])

    uvicorn.run(app, host="127.0.0.1", port=8106)
