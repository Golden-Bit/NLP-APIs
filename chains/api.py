import json

from fastapi import FastAPI, HTTPException, Path, Body, APIRouter
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from pymongo import MongoClient
from chains.utilities.chain_manager import ChainManager
from fastapi.responses import StreamingResponse
from data_stores.api import router as router_1
from document_loaders.api import router as router_2
from document_stores.api import router as router_3
from document_transformers.api import router as router_4
from embedding_models.api import router as router_5
from vector_stores.api import router as router_6
from llms.api import router as router_7
from prompts.api import router as router_8
from tools.api import router as router_9


router = APIRouter()

client = MongoClient('mongodb://localhost:27017/')
db = client['chain_db']
collection = db['chain_configs']
chain_manager = ChainManager(collection)

class ChainConfigRequest(BaseModel):
    chain_type: str = Field(..., example="qa_chain", title="Chain Type", description="The chain's type to configure.")
    config_id: str = Field(..., example="example_chain_config", title="Config ID", description="The unique ID of the chain configuration.")
    chain_id: str = Field(..., example="example_chain", title="Chain ID", description="The unique ID of the chain.")
    prompt_id: str = Field(..., example="example_prompt", title="Prompt ID", description="The unique ID of the prompt.")
    llm_id: str = Field(..., example="example_llm", title="LLM ID", description="The unique ID of the LLM.")
    vectorstore_id: str = Field(..., example="example_vectorstore", title="Vectorstore ID", description="The unique ID of the vectorstore.")


class ExecuteChainRequest(BaseModel):
    chain_id: str = Field(..., example="example_chain", title="Chain ID", description="The unique ID of the chain to execute.")
    query: Dict[str, Any] = Field(..., example={"input": "What is my name?", "chat_history": [["user", "hello, my name is mario!"], ["assistant", "hello, how are you mario?"]]}, title="Query", description="The input query for the chain.")


@router.post("/configure_chain/", response_model=dict)
async def configure_chain(request: ChainConfigRequest):
    """
    Configure a new chain and store its configuration.

    This endpoint allows you to configure a new chain by specifying the configuration ID, chain ID, prompt ID, LLM ID, and vectorstore ID.
    The configuration is then stored in MongoDB.

    - **request**: A JSON object containing the configuration details.

    Returns:
    - **config_id**: The ID of the newly created configuration.
    """
    try:
        result = chain_manager.configure_chain(request.dict())
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/update_chain_config/{config_id}", response_model=dict)
async def update_chain_config(config_id: str, request: ChainConfigRequest):
    """
    Update an existing chain configuration.

    This endpoint updates the configuration of an existing chain by specifying the configuration ID, chain ID, prompt ID, LLM ID, and vectorstore ID.

    - **config_id**: The ID of the configuration to update.
    - **request**: A JSON object containing the updated configuration details.

    Returns:
    - **config_id**: The ID of the updated configuration.
    """
    try:
        result = chain_manager.update_chain_config(config_id, request.dict())
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/delete_chain_config/{config_id}", response_model=dict)
async def delete_chain_config(config_id: str = Path(..., description="The unique ID of the chain configuration to delete.")):
    """
    Delete a specific chain configuration.

    This endpoint deletes the configuration details of a specific chain using the configuration ID.

    - **config_id**: The unique ID of the chain configuration to delete.

    Returns:
    - A confirmation message upon successful deletion.
    """
    try:
        result = chain_manager.delete_chain_config(config_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/load_chain/{config_id}", response_model=dict)
async def load_chain(config_id: str = Path(..., description="The unique ID of the chain configuration to load.")):
    """
    Load a chain into memory based on its configuration ID.

    This endpoint loads a chain into memory using the specified configuration ID. If the chain is already loaded, an error is returned.

    - **config_id**: The unique ID of the chain configuration to load.

    Returns:
    - A confirmation message upon successful loading.
    """
    try:
        result = chain_manager.load_chain(config_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/unload_chain/{chain_id}", response_model=dict)
async def unload_chain(chain_id: str = Path(..., description="The unique ID of the chain to unload.")):
    """
    Unload a chain from memory.

    This endpoint unloads a chain from memory using the specified chain ID. If the chain is not found, an error is returned.

    - **chain_id**: The unique ID of the chain to unload.

    Returns:
    - A confirmation message upon successful unloading.
    """
    try:
        result = chain_manager.unload_chain(chain_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/list_loaded_chains/", response_model=List[str])
async def list_loaded_chains():
    """
    List all currently loaded chains.

    This endpoint retrieves and returns a list of all currently loaded chains.

    Returns:
    - A list of chain IDs for the currently loaded chains.
    """
    return chain_manager.list_loaded_chains()

@router.get("/list_chain_configs/", response_model=List[Dict[str, Any]])
async def list_chain_configs():
    """
    List all chain configurations.

    This endpoint retrieves and returns a list of all chain configurations stored in MongoDB.

    Returns:
    - A list of chain configurations.
    """
    try:
        configs = chain_manager.list_chain_configs()
        return configs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/chain_config/{config_id}", response_model=Dict[str, Any])
async def get_chain_config(config_id: str = Path(..., description="The unique ID of the chain configuration to retrieve.")):
    """
    Retrieve a specific chain configuration.

    This endpoint retrieves the configuration details of a specific chain using the configuration ID.

    - **config_id**: The unique ID of the chain configuration to retrieve.

    Returns:
    - The configuration details of the specified chain.
    """
    try:
        config = chain_manager.get_chain_config(config_id)
        return config
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/execute_chain/", response_model=dict)
async def execute_chain(request: ExecuteChainRequest):
    """
    Execute a specific chain.

    This endpoint executes a loaded chain using the provided query.

    - **request**: A JSON object containing the chain ID and query.

    Returns:
    - The result of the chain execution.
    """
    try:
        chain = chain_manager.get_chain(request.chain_id)
        result = chain.invoke(request.query)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/stream_chain")
async def stream_chain(request: ExecuteChainRequest):

    async def generate_response(chain: Any, query: Dict[str, Any], stream_only_content: bool = False):

        async for chunk in chain.astream(query):

            try:
                chunk = json.dumps(chunk, indent=2)
            except Exception as e:
                #print(e)
                print(chunk)
                chunk = {"error": "output object not serializable"}
                chunk = json.dumps(chunk, indent=2)
            yield chunk

    try:
        body = request
        chain = chain_manager.get_chain(body.chain_id)
        query = body.query
        return StreamingResponse(generate_response(chain, query), media_type="application/json")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    app = FastAPI()

    app.include_router(router_1, prefix="/data_stores", tags=["data_stores"])
    app.include_router(router_2, prefix="/document_loaders", tags=["document_loaders"])
    app.include_router(router_3, prefix="/document_stores", tags=["document_stores"])
    app.include_router(router_4, prefix="/document_transformers", tags=["document_transformers"])
    app.include_router(router_5, prefix="/embedding_models", tags=["embedding_models"])
    app.include_router(router_6, prefix="/vector_stores", tags=["vector_stores"])
    app.include_router(router_7, prefix="/llms", tags=["llms"])
    app.include_router(router_8, prefix="/prompts", tags=["prompts"])
    app.include_router(router_9, prefix="/tools", tags=["tools"])

    app.include_router(router, prefix="/chains", tags=["chains"])

    uvicorn.run(app, host="0.0.0.0", port=8100)
