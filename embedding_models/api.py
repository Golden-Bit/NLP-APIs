import os

from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from fastapi import FastAPI, HTTPException, Path, Body, APIRouter
from pymongo import MongoClient
import uuid
from embedding_models.utilities.model_manager import EmbeddingModelManager
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings

router = APIRouter()

MONGO_CONNECTION_STRING = os.getenv('MONGO_CONNECTION_STRING', 'localhost')
client = MongoClient(MONGO_CONNECTION_STRING)
db = client['embedding_model_db']
collection = db['embedding_model_configs']
embedding_manager = EmbeddingModelManager(collection)


class EmbeddingConfigRequest(BaseModel):
    config_id: str = Field(..., example="example_embedding_config", title="Config ID",
                           description="The unique ID of the embedding configuration.")
    model_id: str = Field(..., example="example_model", title="Model ID",
                          description="The unique ID of the embedding model.")
    model_class: str = Field(..., example="HuggingFaceEmbeddings", title="Model Class",
                             description="The class of the embedding model (e.g., 'HuggingFaceEmbeddings', 'OpenAIEmbeddings').")
    model_kwargs: Dict[str, Any] = Field(default_factory=dict, example={"model_name": "distilbert-base-uncased"},
                                         title="Model Kwargs",
                                         description="Additional keyword arguments for model initialization.")


class InferenceRequest(BaseModel):
    model_id: str = Field(..., example="example_model", title="Model ID",
                          description="The ID of the embedding model to use for inference.")
    texts: List[str] = Field(..., example=["Hello world", "How are you?"], title="Texts",
                             description="The texts to generate embeddings for.")
    inference_kwargs: Dict[str, Any] = Field(default_factory=dict, example={}, title="Inference Kwargs",
                                             description="Additional keyword arguments for inference.")


class ExecuteMethodRequest(BaseModel):
    model_id: str = Field(..., example="example_model", title="Model ID", description="The ID of the embedding model.")
    method_name: str = Field(..., example="generate", title="Method Name",
                             description="The name of the method to call on the embedding model.")
    args: Optional[list] = Field(default_factory=list, example=[], title="Arguments",
                                 description="The positional arguments for the method (if any).")
    kwargs: Optional[Dict[str, Any]] = Field(default_factory=dict, example={}, title="Keyword Arguments",
                                             description="The keyword arguments for the method (if any).")


class GetAttributeRequest(BaseModel):
    model_id: str = Field(..., example="example_model", title="Model ID", description="The ID of the embedding model.")
    attribute_name: str = Field(..., example="attribute_name", title="Attribute Name",
                                description="The name of the attribute to get.")


@router.post("/configure_embedding_model/", response_model=dict)
async def configure_embedding_model(request: EmbeddingConfigRequest):
    """
    Configures a new embedding model and stores its configuration.

    This endpoint allows you to configure a new embedding model by specifying the configuration ID, model ID, model class, and additional keyword arguments for model initialization. The configuration is then stored in MongoDB.

    - **request**: A JSON object containing the configuration details.

    Returns:
    - **config_id**: The ID of the newly created configuration.
    """
    config_id = request.config_id
    if collection.find_one({"_id": config_id}):
        raise HTTPException(status_code=400, detail="Configuration ID already exists")

    config = request.dict()
    config["_id"] = config_id
    collection.insert_one(config)
    return {"config_id": config_id}


@router.post("/load_embedding_model/{config_id}", response_model=dict)
async def load_embedding_model(
        config_id: str = Path(..., description="The unique ID of the embedding model configuration to load.")):
    """
    Loads an embedding model based on its configuration ID.

    This endpoint loads an embedding model into memory using the specified configuration ID. If the model is already loaded, an error is returned.

    - **config_id**: The unique ID of the embedding model configuration to load.

    Returns:
    - A confirmation message upon successful loading.
    """
    try:
        embedding_manager.load_model(config_id)
        return {"message": "Model loaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/unload_embedding_model/{model_id}", response_model=dict)
async def unload_embedding_model(
        model_id: str = Path(..., description="The unique ID of the embedding model to unload.")):
    """
    Unloads an embedding model from memory.

    This endpoint unloads an embedding model from memory using the specified model ID. If the model is not found, an error is returned.

    - **model_id**: The unique ID of the embedding model to unload.

    Returns:
    - A confirmation message upon successful unloading.
    """
    try:
        embedding_manager.unload_model(model_id)
        return {"message": "Model unloaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/embedding_inference/", response_model=dict)
async def embedding_inference(request: InferenceRequest):
    """
    Performs inference using a loaded embedding model.

    This endpoint generates embeddings for the provided texts using a specified embedding model and additional inference keyword arguments.

    - **request**: A JSON object containing the model ID, texts, and additional keyword arguments for inference.

    Returns:
    - The generated embeddings.
    """
    try:
        model = embedding_manager.get_model(request.model_id)
        embeddings = model.embed(request.texts, **request.inference_kwargs)
        return {"embeddings": embeddings}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/list_loaded_embedding_models/", response_model=List[str])
async def list_loaded_embedding_models():
    """
    Lists all currently loaded embedding models.

    This endpoint retrieves and returns a list of all currently loaded embedding models.

    Returns:
    - A list of model IDs for the currently loaded embedding models.
    """
    return embedding_manager.list_loaded_models()


@router.get("/embedding_model_config/{config_id}", response_model=Dict[str, Any])
async def get_embedding_model_config(
        config_id: str = Path(..., description="The unique ID of the embedding model configuration to retrieve.")):
    """
    Retrieves a specific embedding model configuration.

    This endpoint retrieves the configuration details of a specific embedding model using the configuration ID.

    - **config_id**: The unique ID of the embedding model configuration to retrieve.

    Returns:
    - The configuration details of the specified embedding model.
    """
    config = collection.find_one({"_id": config_id})
    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")
    return config


@router.delete("/embedding_model_config/{config_id}", response_model=dict)
async def delete_embedding_model_config(
        config_id: str = Path(..., description="The unique ID of the embedding model configuration to delete.")):
    """
    Deletes a specific embedding model configuration.

    This endpoint deletes the configuration details of a specific embedding model using the configuration ID.

    - **config_id**: The unique ID of the embedding model configuration to delete.

    Returns:
    - A confirmation message upon successful deletion.
    """
    result = collection.delete_one({"_id": config_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Configuration not found")
    return {"detail": "Configuration deleted successfully"}


@router.post("/execute_embedding_method/", response_description="Execute a method of an embedding model instance")
async def execute_embedding_method(request: ExecuteMethodRequest):
    """
    Execute a method of an embedding model instance.

    This endpoint executes a specified method on a loaded embedding model instance using the provided arguments and keyword arguments.

    - **request**: A JSON object containing the model ID, method name, positional arguments, and keyword arguments.

    Returns:
    - The result of the method execution.
    """
    try:
        embedding_instance = embedding_manager.get_model(request.model_id)
        if not hasattr(embedding_instance, request.method_name):
            raise ValueError(f"Method '{request.method_name}' does not exist on embedding model instance")

        method = getattr(embedding_instance, request.method_name)
        if callable(method):
            result = method(*request.args, **request.kwargs)
            return {"result": result}
        else:
            raise ValueError(f"'{request.method_name}' is not a callable method")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/get_embedding_attribute/", response_description="Get an attribute of an embedding model instance")
async def get_embedding_attribute(request: GetAttributeRequest):
    """
    Get an attribute of an embedding model instance.

    This endpoint retrieves the value of a specified attribute from a loaded embedding model instance.

    - **request**: A JSON object containing the model ID and attribute name.

    Returns:
    - The value of the specified attribute.
    """
    try:
        embedding_instance = embedding_manager.get_model(request.model_id)
        if not hasattr(embedding_instance, request.attribute_name):
            raise ValueError(f"Attribute '{request.attribute_name}' does not exist on embedding model instance")

        attribute = getattr(embedding_instance, request.attribute_name)
        return {"attribute": attribute}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    app = FastAPI()

    app.include_router(router, prefix="/embedding_models", tags=["embedding_models"])

    uvicorn.run(app, host="127.0.0.1", port=8104)