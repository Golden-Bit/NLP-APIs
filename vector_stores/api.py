import os

from fastapi import FastAPI, HTTPException, Path, Body, Query, APIRouter
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Tuple
from pymongo import MongoClient
import uuid
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma, ElasticsearchStore, ElasticVectorSearch, FAISS
from langchain_community.embeddings import OpenAIEmbeddings, HuggingFaceEmbeddings

router = APIRouter()

# MongoDB connection configuration
MONGO_CONNECTION_STRING = os.getenv('MONGO_CONNECTION_STRING', 'localhost')
client = MongoClient(MONGO_CONNECTION_STRING)
db_name = "vector_store"
collection_name = "vector_store_configs"
vector_store_collection = client[db_name][collection_name]

document_db_name = "document_store"  # Database name for documents
document_collection_name = "documents"  # Default collection name for documents

# In-memory storage for vector stores and embeddings
vector_stores = {}
embeddings_models = {}

# Mapping of available vector store classes
VECTOR_STORE_CLASSES = {
    "Chroma": Chroma,
    "ElasticsearchStore": ElasticsearchStore,
    "ElasticVectorSearch": ElasticVectorSearch,
    "FAISS": FAISS
}

# Mapping of available embeddings models
EMBEDDINGS_MODELS = {
    "OpenAIEmbeddings": OpenAIEmbeddings,
    "HuggingFaceEmbeddings": HuggingFaceEmbeddings,
}


class ExecuteMethodRequest(BaseModel):
    store_id: str = Field(..., example="abcd1234-efgh-5678-ijkl-9012mnop3456", title="Store ID", description="The unique ID of the vector store instance.")
    method_name: str = Field(..., example="persist", title="Method Name", description="The name of the method to call on the vector store.")
    args: Optional[List[Any]] = Field(default_factory=list, example=[], title="Arguments", description="The positional arguments for the method (if any).")
    kwargs: Optional[Dict[str, Any]] = Field(default_factory=dict, example={"param1": "value1", "param2": "value2"}, title="Keyword Arguments", description="The keyword arguments for the method (if any).")


class GetAttributeRequest(BaseModel):
    store_id: str = Field(..., example="abcd1234-efgh-5678-ijkl-9012mnop3456", title="Store ID", description="The unique ID of the vector store instance.")
    attribute_name: str = Field(..., example="attribute_name", title="Attribute Name", description="The name of the attribute to get.")


class VectorStoreConfigModel(BaseModel):
    """Pydantic model for vector store configuration."""
    config_id: Optional[str] = Field(None, description="The unique ID for the vector store configuration.",
                                     example="abcd1234-efgh-5678-ijkl-9012mnop3456")
    store_id: Optional[str] = Field(None, description="The unique ID for the vector store instance.",
                                    example="abcd1234-efgh-5678-ijkl-9012mnop3456")
    vector_store_class: str = Field(..., description="The class of the vector store.", example="Chroma")
    params: Dict[str, Any] = Field(..., description="Configuration parameters for the vector store.",
                                   example={"param1": "value1", "param2": "value2"})
    embeddings_model_class: Optional[str] = Field(None, description="The class of the embeddings model.",
                                                  example="OpenAIEmbeddings")
    embeddings_params: Optional[Dict[str, Any]] = Field(None,
                                                        description="Configuration parameters for the embeddings model.",
                                                        example={"api_key": "your_openai_api_key"})
    description: Optional[str] = Field(None, description="A description of the vector store configuration.",
                                       example="This is a Chroma vector store configuration for project X.")
    custom_metadata: Optional[Dict[str, Any]] = Field(None, description="Custom metadata for the configuration.",
                                                      example={"project": "Project X", "owner": "John Doe"})


class MethodRequestModel(BaseModel):
    """Pydantic model for a method request."""
    method_name: str = Field(..., description="The name of the method to call.", example="persist")
    kwargs: Dict[str, Any] = Field(default_factory=dict, description="Keyword arguments for the method.",
                                   example={"param1": "value1", "param2": "value2"})


class DocumentModel(BaseModel):
    """Pydantic model for documents."""
    page_content: str = Field(..., description="The content of the document.",
                              example="This is the content of the document.")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Metadata associated with the document.",
                                     example={"author": "John Doe"})

    @staticmethod
    def from_langchain_document(doc: Document) -> 'DocumentModel':
        """Create a DocumentModel from a LangChain Document."""
        return DocumentModel(
            page_content=doc.page_content,
            metadata=doc.metadata
        )

    def to_langchain_document(self) -> Document:
        """Convert DocumentModel to a LangChain Document."""
        return Document(
            page_content=self.page_content,
            metadata=self.metadata
        )


class SearchRequestModel(BaseModel):
    """Pydantic model for a search request."""
    query: str = Field(..., description="The search query.", example="example query")
    search_type: str = Field(..., description="The type of search to perform. Supported types: 'similarity', 'mmr', 'similarity_score_threshold'", example="similarity")
    search_kwargs: Dict[str, Any] = Field(default_factory=dict, description="Additional keyword arguments for the search method.", example={"k": 4})


class FilterRequestModel(BaseModel):
    """Pydantic model for a filter request."""
    filter: Dict[str, Any] = Field(..., description="The filter criteria for retrieving documents.", example={"author": "John Doe"})
    skip: Optional[int] = Field(0, description="The number of documents to skip.", example=0)
    limit: Optional[int] = Field(10, description="The maximum number of documents to return.", example=10)


def get_vector_store_collection():
    """Get the MongoDB collection for storing vector store configurations.

    Returns:
        Collection: The MongoDB collection for vector store configurations.
    """
    return client[db_name][collection_name]


def get_document_collection(collection_name: str):
    """Get the MongoDB collection for storing documents.

    Args:
        collection_name (str): The name of the collection.

    Returns:
        Collection: The MongoDB collection for documents.
    """
    return client[document_db_name][collection_name]


@router.post("/vector_store/configure", response_model=VectorStoreConfigModel)
async def configure_vector_store(
    config_id: Optional[str] = Body(None, description="The unique ID for the vector store configuration.",
                                    example="abcd1234-efgh-5678-ijkl-9012mnop3456"),
    store_id: Optional[str] = Body(None, description="The unique ID for the vector store instance.",
                                   example="abcd1234-efgh-5678-ijkl-9012mnop3456"),
    vector_store_class: str = Body(..., description="The class of the vector store.", example="Chroma"),
    params: Dict[str, Any] = Body(..., description="Configuration parameters for the vector store.",
                                  example={"param1": "value1", "param2": "value2"}),
    embeddings_model_class: Optional[str] = Body(None, description="The class of the embeddings model.",
                                                 example="OpenAIEmbeddings"),
    embeddings_params: Optional[Dict[str, Any]] = Body(None, description="Configuration parameters for the embeddings model.",
                                                       example={"api_key": "your_openai_api_key"}),
    description: Optional[str] = Body(None, description="A description of the vector store configuration.",
                                      example="This is a Chroma vector store configuration for project X."),
    custom_metadata: Optional[Dict[str, Any]] = Body(None, description="Custom metadata for the configuration.",
                                                     example={"project": "Project X", "owner": "John Doe"})
):
    """
    Configure a vector store.

    This endpoint allows the user to configure a vector store by specifying the class, parameters, and optional embeddings model.
    The configuration is saved in MongoDB with a unique ID. If a configuration with the same config_id already exists, an error is returned.

    Returns the created configuration.
    """
    if config_id is None:
        config_id = str(uuid.uuid4())
    if store_id is None:
        store_id = str(uuid.uuid4())

    if vector_store_collection.find_one({"_id": config_id}):
        raise HTTPException(status_code=400, detail="Configuration ID already exists")

    config = {
        "config_id": config_id,
        "store_id": store_id,
        "vector_store_class": vector_store_class,
        "params": params,
        "embeddings_model_class": embeddings_model_class,
        "embeddings_params": embeddings_params,
        "description": description,
        "custom_metadata": custom_metadata
    }

    vector_store_collection.insert_one({"_id": config_id, "config": config})
    return VectorStoreConfigModel(**config)


@router.delete("/vector_store/configure/{config_id}", response_model=dict)
async def delete_vector_store_config(
    config_id: str = Path(..., description="The unique ID of the vector store configuration to delete.", example="abcd1234-efgh-5678-ijkl-9012mnop3456")
):
    """
    Delete a vector store configuration.

    This endpoint deletes a specified vector store configuration from MongoDB.

    Returns a confirmation message upon successful deletion.
    """
    result = vector_store_collection.delete_one({"_id": config_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Configuration not found")
    return {"detail": "Configuration deleted successfully"}


@router.put("/vector_store/configure/{config_id}", response_model=VectorStoreConfigModel)
async def update_vector_store_config(
    config_id: str = Path(..., description="The unique ID of the vector store configuration to update.", example="abcd1234-efgh-5678-ijkl-9012mnop3456"),
    store_id: Optional[str] = Body(None, description="The unique ID for the vector store instance.", example="abcd1234-efgh-5678-ijkl-9012mnop3456"),
    vector_store_class: str = Body(..., description="The class of the vector store.", example="Chroma"),
    params: Dict[str, Any] = Body(..., description="Configuration parameters for the vector store.", example={"param1": "new_value1", "param2": "new_value2"}),
    embeddings_model_class: Optional[str] = Body(None, description="The class of the embeddings model.", example="OpenAIEmbeddings"),
    embeddings_params: Optional[Dict[str, Any]] = Body(None, description="Configuration parameters for the embeddings model.", example={"api_key": "new_api_key"}),
    description: Optional[str] = Body(None, description="A description of the vector store configuration.", example="Updated description for project X."),
    custom_metadata: Optional[Dict[str, Any]] = Body(None, description="Custom metadata for the configuration.", example={"project": "Updated Project X", "owner": "Jane Doe"})
):
    """
    Update a vector store configuration.

    This endpoint updates the configuration of an existing vector store in MongoDB.

    Returns the updated configuration.
    """
    existing_config = vector_store_collection.find_one({"_id": config_id})
    if not existing_config:
        raise HTTPException(status_code=404, detail="Configuration not found")

    if store_id is None:
        store_id = existing_config["config"]["store_id"]

    updated_config = {
        "config_id": config_id,
        "store_id": store_id,
        "vector_store_class": vector_store_class,
        "params": params,
        "embeddings_model_class": embeddings_model_class,
        "embeddings_params": embeddings_params,
        "description": description,
        "custom_metadata": custom_metadata
    }

    vector_store_collection.update_one({"_id": config_id}, {"$set": {"config": updated_config}})
    return VectorStoreConfigModel(**updated_config)


@router.get("/vector_store/configurations", response_model=List[VectorStoreConfigModel])
async def list_vector_store_configs():
    """
    List all vector store configurations.

    This endpoint retrieves and returns a list of all vector store configurations stored in MongoDB.
    """
    configs = list(vector_store_collection.find({}, {"_id": 0, "config": 1}))
    return [VectorStoreConfigModel(**config["config"]) for config in configs]


@router.post("/vector_store/load/{config_id}", response_model=dict)
def load_vector_store(
    config_id: str = Path(..., description="The unique ID of the vector store configuration to load.", example="abcd1234-efgh-5678-ijkl-9012mnop3456")
):
    """
    Load a vector store into memory.

    This endpoint loads a vector store into memory using the specified configuration ID. If a store with the same store_id already exists in memory, an error is returned.

    Returns a confirmation message upon successful loading.
    """
    config = vector_store_collection.find_one({"_id": config_id})
    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")

    store_id = config["config"]["store_id"]
    if store_id in vector_stores:
        raise HTTPException(status_code=400, detail="Store ID already exists in memory")

    vector_store_class = config["config"]["vector_store_class"]
    if vector_store_class not in VECTOR_STORE_CLASSES:
        raise HTTPException(status_code=400, detail=f"Vector store class {vector_store_class} not supported")

    vector_store_params = config["config"]["params"]

    # Load embeddings model if specified
    # TODO:
    #  - [ ] load embedding models from model_manager class
    embeddings_model = None
    if config["config"].get("embeddings_model_class"):
        embeddings_model_class = config["config"]["embeddings_model_class"]
        if embeddings_model_class not in EMBEDDINGS_MODELS:
            raise HTTPException(status_code=400,
                                detail=f"Embeddings model class {embeddings_model_class} not supported")

        embeddings_params = config["config"].get("embeddings_params", {})
        embeddings_model = EMBEDDINGS_MODELS[embeddings_model_class](**embeddings_params)

    # Initialize the vector store
    vector_store_instance = VECTOR_STORE_CLASSES[vector_store_class](**vector_store_params, embedding_function=embeddings_model)
    vector_stores[store_id] = vector_store_instance

    return {"detail": f"Vector store {store_id} loaded successfully"}


@router.post("/vector_store/offload/{store_id}", response_model=dict)
async def offload_vector_store(
    store_id: str = Path(..., description="The unique ID of the vector store to offload from memory.", example="abcd1234-efgh-5678-ijkl-9012mnop3456")
):
    """
    Offload a vector store from memory.

    This endpoint offloads a vector store from memory using the specified store ID.

    Returns a confirmation message upon successful offloading.
    """
    if store_id not in vector_stores:
        raise HTTPException(status_code=404, detail="Vector store not found in memory")

    # Offload the vector store
    del vector_stores[store_id]
    return {"detail": f"Vector store {store_id} offloaded successfully"}


@router.get("/vector_store/loaded_store_ids", response_model=List[str])
async def get_loaded_store_ids():
    """
    Get IDs of currently loaded vector stores.

    This endpoint returns a list of IDs for vector stores currently loaded in memory.
    """
    return list(vector_stores.keys())


@router.post("/vector_store/documents/{store_id}", response_model=dict)
async def add_documents_to_vector_store(
    store_id: str = Path(..., description="The unique ID of the vector store instance.", example="abcd1234-efgh-5678-ijkl-9012mnop3456"),
    documents: List[DocumentModel] = Body(..., description="The documents to add to the vector store.", example=[
        {"page_content": "Document content", "metadata": {"author": "John Doe"}}])
):
    """
    Add documents to a vector store.

    This endpoint adds documents to a vector store specified by the store ID.

    Returns a confirmation message upon successful addition.
    """
    if store_id not in vector_stores:
        raise HTTPException(status_code=404, detail="Vector store not found in memory")

    vector_store_instance = vector_stores[store_id]
    langchain_docs = [doc.to_langchain_document() for doc in documents]

    # Add documents to vector store
    vector_store_instance.add_documents(langchain_docs)

    return {"detail": f"Documents added to vector store {store_id} successfully"}


@router.post("/vector_store/texts/{store_id}", response_model=dict)
async def add_texts_to_vector_store(
    store_id: str = Path(..., description="The unique ID of the vector store instance.", example="abcd1234-efgh-5678-ijkl-9012mnop3456"),
    texts: List[str] = Body(..., description="The texts to add to the vector store.", example=["Text content 1", "Text content 2"]),
    metadatas: Optional[List[Dict[str, Any]]] = Body(None, description="Optional metadatas associated with the texts.", example=[{"author": "John Doe"}, {"author": "Jane Doe"}])
):
    """
    Add texts to a vector store.

    This endpoint adds texts and optional metadata to a vector store specified by the store ID.

    Returns a confirmation message upon successful addition.
    """
    if store_id not in vector_stores:
        raise HTTPException(status_code=404, detail="Vector store not found in memory")

    vector_store_instance = vector_stores[store_id]

    # Add texts to vector store
    vector_store_instance.add_texts(texts, metadatas)

    return {"detail": f"Texts added to vector store {store_id} successfully"}


@router.delete("/vector_store/documents/{store_id}", response_model=dict)
async def remove_documents_from_vector_store(
    store_id: str = Path(..., description="The unique ID of the vector store instance.", example="abcd1234-efgh-5678-ijkl-9012mnop3456"),
    ids: List[str] = Body(..., description="The IDs of the documents to remove from the vector store.", example=["id1", "id2"])
):
    """
    Remove documents from a vector store.

    This endpoint removes documents from a vector store specified by the store ID.

    Returns a confirmation message upon successful removal.
    """
    if store_id not in vector_stores:
        raise HTTPException(status_code=404, detail="Vector store not found in memory")

    vector_store_instance = vector_stores[store_id]

    # Remove documents from vector store
    vector_store_instance.delete(ids)

    return {"detail": f"Documents removed from vector store {store_id} successfully"}


@router.post("/vector_store/method/{store_id}", response_model=dict)
async def execute_vector_store_method(
    store_id: str = Path(..., description="The unique ID of the vector store instance.", example="abcd1234-efgh-5678-ijkl-9012mnop3456"),
    method_name: str = Body(..., description="The name of the method to call.", example="persist"),
    kwargs: Dict[str, Any] = Body(default_factory=dict, description="Keyword arguments for the method.", example={"param1": "value1", "param2": "value2"})
):
    """
    Execute a specific method on a vector store.

    This endpoint allows executing a specific method with provided kwargs on the vector store specified by the store ID.

    Returns the result of the method execution.
    """
    if store_id not in vector_stores:
        raise HTTPException(status_code=404, detail="Vector store not found in memory")

    vector_store_instance = vector_stores[store_id]

    if not hasattr(vector_store_instance, method_name):
        raise HTTPException(status_code=400, detail=f"Method {method_name} not found in vector store class {type(vector_store_instance).__name__}")

    method = getattr(vector_store_instance, method_name)
    result = method(**kwargs)

    return {"detail": f"Method {method_name} executed successfully on vector store {store_id}", "result": result}


@router.post("/vector_store/add_documents_from_store/{store_id}", response_model=dict)
async def add_documents_from_document_store(
    store_id: str = Path(..., description="The unique ID of the vector store instance.", example="abcd1234-efgh-5678-ijkl-9012mnop3456"),
    document_collection: str = Query(..., description="The name of the document collection in the document store.", example="my_document_collection")
):
    """
    Add documents to a vector store from a document store collection.

    This endpoint retrieves documents from a specified document collection in the document store and adds them to the vector store specified by the store ID.

    Returns a confirmation message upon successful addition.
    """
    if store_id not in vector_stores:
        raise HTTPException(status_code=404, detail="Vector store not found in memory")

    vector_store_instance = vector_stores[store_id]
    document_collection_instance = get_document_collection(document_collection)

    documents_cursor = document_collection_instance.find()

    documents = [DocumentModel(page_content=doc["value"]["page_content"], metadata=doc["value"]["metadata"]).to_langchain_document() for doc in documents_cursor]

    # Add documents to vector store
    vector_store_instance.add_documents(documents)

    return {"detail": f"Documents from collection {document_collection} added to vector store {store_id} successfully"}


@router.put("/vector_store/documents/{store_id}/{document_id}", response_model=dict)
async def update_document_in_vector_store(
    store_id: str = Path(..., description="The unique ID of the vector store instance.", example="abcd1234-efgh-5678-ijkl-9012mnop3456"),
    document_id: str = Path(..., description="The unique ID of the document to update.", example="doc1234"),
    document: DocumentModel = Body(..., description="The updated document data.")
):
    """
    Update a document in a vector store.

    This endpoint updates a document in a vector store specified by the store ID and document ID.

    Returns a confirmation message upon successful update.
    """
    if store_id not in vector_stores:
        raise HTTPException(status_code=404, detail="Vector store not found in memory")

    vector_store_instance = vector_stores[store_id]

    # Update document in vector store
    updated_document = document.to_langchain_document()
    vector_store_instance.update_document(document_id, updated_document)

    return {"detail": f"Document {document_id} updated in vector store {store_id} successfully"}


@router.post("/vector_store/search/{store_id}", response_model=List[DocumentModel | Tuple[DocumentModel, float]])
async def search_vector_store(
    store_id: str = Path(..., description="The unique ID of the vector store instance.", example="abcd1234-efgh-5678-ijkl-9012mnop3456"),
    query: str = Body(..., description="The search query.", example="example query"),
    search_type: str = Body(..., description="The type of search to perform. Supported types: 'similarity', 'mmr', 'similarity_score_threshold'", example="similarity"),
    search_kwargs: Dict[str, Any] = Body(default_factory=dict, description="Additional keyword arguments for the search method.", example={"k": 4})
):
    """
    Search a vector store.

    This endpoint allows searching a vector store using the specified search type and query.

    Returns a list of documents that match the search criteria.
    """
    if store_id not in vector_stores:
        raise HTTPException(status_code=404, detail="Vector store not found in memory")

    vector_store_instance = vector_stores[store_id]

    if search_type not in ["similarity", "mmr", "similarity_score_threshold"]:
        raise HTTPException(status_code=400, detail="Unsupported search type. Supported types are: 'similarity', 'mmr', 'similarity_score_threshold'")

    if search_type == "similarity":
        results = vector_store_instance.similarity_search(query, **search_kwargs)
    elif search_type == "mmr":
        results = vector_store_instance.max_marginal_relevance_search(query, **search_kwargs)
    elif search_type == "similarity_score_threshold":
        results = vector_store_instance.similarity_search_with_relevance_scores(query, **search_kwargs)
        return [(DocumentModel.from_langchain_document(result[0]), result[1]) for result in results]

    return [DocumentModel.from_langchain_document(result) for result in results]


@router.post("/vector_store/retrieve/{store_id}", response_model=List[DocumentModel | Tuple[DocumentModel, float]])
async def vector_store_as_retriever(
        store_id: str = Path(..., description="The unique ID of the vector store instance.",
                             example="abcd1234-efgh-5678-ijkl-9012mnop3456"),
        query: str = Body(..., description="The search query.", example="example query"),
        search_type: Optional[str] = Body("similarity",
                                          description="The type of search to perform. Supported types: 'similarity', 'mmr', 'similarity_score_threshold'",
                                          example="similarity"),
        search_kwargs: Dict[str, Any] = Body(default_factory=dict,
                                             description="Additional keyword arguments for the search method.",
                                             example={"k": 4})
):
    """
    Retrieve documents from a vector store using the retriever method.

    This endpoint allows retrieving documents from a vector store using the specified search query.

    Returns a list of documents that match the search criteria.
    """
    if store_id not in vector_stores:
        raise HTTPException(status_code=404, detail="Vector store not found in memory")

    vector_store_instance = vector_stores[store_id]

    # Ensure the vector store has the as_retriever method
    if not hasattr(vector_store_instance, "as_retriever"):
        raise HTTPException(status_code=400,
                            detail=f"Vector store class {type(vector_store_instance).__name__} does not support retriever method")

    # Initialize the retriever with the provided search type and search kwargs
    retriever = vector_store_instance.as_retriever(search_type=search_type, search_kwargs=search_kwargs)

    # Perform the retrieval
    #results = retriever.retrieve(query)
    results = retriever.invoke(input=query)

    #if search_type == "similarity_score_threshold":
    #    return [(DocumentModel.from_langchain_document(result[0]), result[1]) for result in results]

    return [DocumentModel.from_langchain_document(result) for result in results]


@router.post("/vector_store/filter/{store_id}", response_model=List[DocumentModel])
async def filter_vector_store(
    store_id: str = Path(..., description="The unique ID of the vector store instance.", example="abcd1234-efgh-5678-ijkl-9012mnop3456"),
    filter: Dict[str, Any] = Body(..., description="The filter criteria for retrieving documents.", example={"author": "John Doe"}),
    skip: int = Query(0, description="The number of documents to skip.", example=0),
    limit: int = Query(10, description="The maximum number of documents to return.", example=10)
):
    """
    Filter documents in a vector store.

    This endpoint retrieves documents from a vector store that match the specified filter criteria.

    Returns a list of documents that match the filter criteria.
    """
    if store_id not in vector_stores:
        raise HTTPException(status_code=404, detail="Vector store not found in memory")

    vector_store_instance = vector_stores[store_id]

    # Assuming vector_store_instance has a method to filter documents based on metadata
    if not hasattr(vector_store_instance, "filter_documents"):
        raise HTTPException(status_code=400, detail=f"Vector store class {type(vector_store_instance).__name__} does not support filtering")

    results = vector_store_instance.filter_documents(filter, skip=skip, limit=limit)
    return [DocumentModel.from_langchain_document(doc) for doc in results]


@router.post("/vector_store/method/", response_description="Execute a method of a vector store instance")
async def execute_vector_store_method(request: ExecuteMethodRequest):
    """
    Execute a method of a vector store instance.

    - **store_id**: The unique ID of the vector store instance.
    - **method_name**: The name of the method to execute.
    - **args**: The positional arguments for the method (if any).
    - **kwargs**: The keyword arguments for the method (if any).
    """
    store_id = request.store_id
    method_name = request.method_name
    args = request.args
    kwargs = request.kwargs

    try:
        vector_store_instance = vector_stores.get(store_id)
        if vector_store_instance is None:
            raise ValueError("Vector store instance ID does not exist")

        if not hasattr(vector_store_instance, method_name):
            raise ValueError(f"Method '{method_name}' does not exist on vector store instance")

        method = getattr(vector_store_instance, method_name)

        if callable(method):
            result = method(*args, **kwargs)
            return {"result": result}
        else:
            raise ValueError(f"'{method_name}' is not a callable method")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/vector_store/attribute/", response_description="Get an attribute of a vector store instance")
async def get_vector_store_attribute(request: GetAttributeRequest):
    """
    Get an attribute of a vector store instance.

    - **store_id**: The unique ID of the vector store instance.
    - **attribute_name**: The name of the attribute to get.
    """
    store_id = request.store_id
    attribute_name = request.attribute_name

    try:
        vector_store_instance = vector_stores.get(store_id)
        if vector_store_instance is None:
            raise ValueError("Vector store instance ID does not exist")

        if not hasattr(vector_store_instance, attribute_name):
            raise ValueError(f"Attribute '{attribute_name}' does not exist on vector store instance")

        attribute = getattr(vector_store_instance, attribute_name)
        return {"attribute": attribute}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    app = FastAPI()

    app.include_router(router, prefix="/vector_stores", tags=["vector_stores"])

    uvicorn.run(app, host="127.0.0.1", port=8105)
