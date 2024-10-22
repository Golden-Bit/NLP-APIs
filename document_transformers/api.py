import os

from fastapi import FastAPI, HTTPException, Path, Body, Query, APIRouter
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Union
import uuid
from pymongo import MongoClient
from langchain_core.documents import Document
from langchain_core.documents.transformers import BaseDocumentTransformer

from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter, TokenTextSplitter

from document_transformers.utilities.document_transformer_map import DocumentTransformerMap

router = APIRouter()

# MongoDB connection configuration
MONGO_CONNECTION_STRING = os.getenv('MONGO_CONNECTION_STRING', 'localhost')
mongo_client = MongoClient(MONGO_CONNECTION_STRING)
mongo_db_name = "transformers"
transformer_collection_name = "transformer_configs"
transformer_map_collection_name = "transformer_map_configs"

# In-memory storage for configurations (for demonstration purposes)
transformer_configs = {}

available_transformers = {
    "CharacterTextSplitter": CharacterTextSplitter,
    "RecursiveCharacterTextSplitter": RecursiveCharacterTextSplitter,
    "TokenTextSplitter": TokenTextSplitter
}

class TransformerConfig(BaseModel):
    """Pydantic model for transformer configuration."""
    config_id: Optional[str] = Field(None, description="The unique ID for the transformer configuration.")
    transformer: str = Field("CharacterTextSplitter", description="The transformer class name.")
    kwargs: Dict[str, Any] = Field({"chunk_size": 1, "chunk_overlap": 0, "separator": " "},
                                   description="Keyword arguments for the transformer.")
    add_prefix_to_id: Optional[str] = Field(None, description="Prefix to add to the document ID.")
    add_suffix_to_id: Optional[str] = Field(None, description="Suffix to add to the document ID.")
    add_split_index_to_id: bool = Field(True, description="Whether to add split index to the document ID.")
    output_store: Optional[Dict[str, Any]] = Field(None, description="Output store configuration.")
    description: Optional[str] = Field(None, description="Description of the transformer configuration.")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Metadata associated with the transformer configuration.")
    add_metadata_to_docs: Dict[str, Any] = Field({}, description="Metadata to add to documents.")

class TransformerMapConfig(BaseModel):
    """Pydantic model for transformer map configuration."""
    config_id: Optional[str] = Field(None, description="The unique ID for the transformer map configuration.")
    transformer_map: Dict[str, Union[TransformerConfig, str]] = Field({}, description="Mapping of queries to transformer configurations.")
    default_transformer: Optional[str] = Field("CharacterTextSplitter", description="The default transformer class name.")
    default_kwargs: Dict[str, Any] = Field({"chunk_size": 1000, "chunk_overlap": 200}, description="Default keyword arguments for the transformer.")
    default_add_prefix_to_id: Optional[str] = Field(None, description="Default prefix to add to the document ID.")
    default_add_suffix_to_id: Optional[str] = Field(None, description="Default suffix to add to the document ID.")
    default_add_split_index_to_id: bool = Field(True, description="Whether to add default split index to the document ID.")
    default_add_metadata_to_docs: Dict[str, Any] = Field({"default_key": "default_value"}, description="Default metadata to add to documents.")
    default_output_store: Optional[Dict[str, Any]] = Field(None, description="Default output store configuration.")
    description: Optional[str] = Field(None, description="Description of the transformer map configuration.")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Metadata associated with the transformer map configuration.")

class DocumentModel(BaseModel):
    """Pydantic model for documents."""
    page_content: str = Field("This is the content of the document.", description="The content of the document.")
    metadata: Dict[str, Any] = Field({"author": "John Doe", "category": "Research"}, description="Metadata associated with the document.")

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
            metadata=self.metadata,
        )

class SearchConfig(BaseModel):
    """Pydantic model for searching transformer configurations."""
    transformer: Optional[str] = Field(None, description="Transformer type to filter configurations.")
    add_prefix_to_id: Optional[str] = Field(None, description="Prefix to filter configurations.")
    add_suffix_to_id: Optional[str] = Field(None, description="Suffix to filter configurations.")
    add_split_index_to_id: Optional[bool] = Field(None, description="Whether to filter by split index addition.")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Metadata to filter configurations.")
    skip: Optional[int] = Field(0, description="Number of records to skip.")
    limit: Optional[int] = Field(None, description="Maximum number of records to return.")

def save_document_to_store(collection_name: str, document: DocumentModel):
    """
    Save a document to the MongoDB document store.

    Args:
        collection_name (str): The name of the collection.
        document (DocumentModel): The document to save.

    Returns:
        str: A unique ID linked to the saved document.
    """
    collection = mongo_client["document_store"][collection_name]
    key = document.metadata.get("id", str(uuid.uuid4()))
    document.metadata.update({"doc_store_id": key, "doc_store_collection": collection_name})
    collection.update_one(
        {"_id": key}, {"$set": {
            "page_content": document.page_content,
            "metadata": document.metadata
        }},
        upsert=True
    )
    return key

def load_documents_from_store(collection_name: str) -> List[Document]:
    """
    Load documents from the MongoDB document store.

    Args:
        collection_name (str): The name of the collection.

    Returns:
        List[Document]: A list of documents loaded from the store.
    """
    collection = mongo_client["document_store"][collection_name]
    documents = []
    for doc in collection.find():
        doc_data = doc['value']
        documents.append(Document(
            page_content=doc_data["page_content"],
            metadata=doc_data["metadata"]
        ))
    return documents

def get_transformer_class(name: str) -> type:
    """Retrieve the transformer class based on its name."""
    return available_transformers.get(name)

# Transformer Config Endpoints
@router.post("/configure_transformer", response_model=str)
async def configure_transformer(
        config_id: Optional[str] = Body(None, description="The unique ID for the transformer configuration. If not provided, a new ID will be generated."),
        transformer: str = Body(..., description="The transformer class name."),
        kwargs: Dict[str, Any] = Body(..., description="Keyword arguments for the transformer."),
        add_prefix_to_id: Optional[str] = Body(None, description="Prefix to add to the document ID."),
        add_suffix_to_id: Optional[str] = Body(None, description="Suffix to add to the document ID."),
        add_split_index_to_id: bool = Body(True, description="Whether to add split index to the document ID."),
        output_store: Optional[Dict[str, Any]] = Body(None, description="Output store configuration."),
        description: Optional[str] = Body(None, description="Description of the transformer configuration."),
        metadata: Optional[Dict[str, Any]] = Body(None, description="Metadata associated with the transformer configuration."),
        add_metadata_to_docs: Dict[str, Any] = Body({}, description="Metadata to add to documents.")
):
    """
    Configure a Transformer with specified parameters.

    This endpoint allows the user to set up a Transformer by specifying
    various parameters including the transformer class, keyword arguments, ID prefix/suffix,
    output store configurations, description, and metadata. It returns a unique configuration ID for the transformer.

    If `config_id` is provided, the endpoint will check if a configuration with the same ID already exists.
    If it does, an error will be returned.
    """
    try:
        if config_id and mongo_client[mongo_db_name][transformer_collection_name].find_one({"config_id": config_id}):
            raise HTTPException(status_code=400, detail=f"Configuration with ID {config_id} already exists.")

        if not config_id:
            config_id = str(uuid.uuid4())

        transformer_config = TransformerConfig(
            config_id=config_id,
            transformer=transformer,
            kwargs=kwargs,
            add_prefix_to_id=add_prefix_to_id,
            add_suffix_to_id=add_suffix_to_id,
            add_split_index_to_id=add_split_index_to_id,
            output_store=output_store,
            description=description,
            metadata=metadata,
            add_metadata_to_docs=add_metadata_to_docs
        )

        # Save configuration to MongoDB
        mongo_client[mongo_db_name][transformer_collection_name].insert_one(transformer_config.dict())

        return config_id
    except KeyError:
        raise HTTPException(status_code=400, detail="Transformer not found.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/list_transformer_configs", response_model=List[TransformerConfig])
async def list_transformer_configs(skip: int = Query(0, description="Number of records to skip"), limit: Optional[int] = Query(0, description="Maximum number of records to return")):
    """
    List all existing transformer configurations.

    This endpoint retrieves and returns all existing transformer configurations stored in the MongoDB.
    It is useful for viewing all available configurations.
    """
    configs = mongo_client[mongo_db_name][transformer_collection_name].find().skip(skip).limit(limit)
    return [TransformerConfig(**config) for config in configs]

@router.get("/get_transformer_config/{config_id}", response_model=TransformerConfig)
async def get_transformer_config(
        config_id: str = Path(..., description="The unique ID of the transformer configuration to retrieve.")
):
    """
    Retrieve a transformer configuration by its ID.

    This endpoint retrieves a specific transformer configuration from the MongoDB using its unique ID.
    """
    config = mongo_client[mongo_db_name][transformer_collection_name].find_one({"config_id": config_id})
    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")
    return TransformerConfig(**config)

@router.post("/search_transformer_configs", response_model=List[TransformerConfig])
async def search_transformer_configs(search_params: SearchConfig = Body(...)):
    """
    Search for transformer configurations based on advanced criteria.

    This endpoint allows the user to search for existing transformer configurations based on specified criteria such as
    transformer type, prefix, suffix, split index addition, and metadata.
    """
    query = {}
    if search_params.transformer:
        query["transformer"] = search_params.transformer
    if search_params.add_prefix_to_id:
        query["add_prefix_to_id"] = search_params.add_prefix_to_id
    if search_params.add_suffix_to_id:
        query["add_suffix_to_id"] = search_params.add_suffix_to_id
    if search_params.add_split_index_to_id is not None:
        query["add_split_index_to_id"] = search_params.add_split_index_to_id
    if search_params.metadata:
        for key, value in search_params.metadata.items():
            query[f"metadata.{key}"] = value

    configs = mongo_client[mongo_db_name][transformer_collection_name].find(query).skip(search_params.skip).limit(search_params.limit)
    return [TransformerConfig(**config) for config in configs]

@router.delete("/delete_transformer_config/{config_id}", response_model=dict)
async def delete_transformer_config(
        config_id: str = Path(..., description="The unique ID of the transformer configuration to delete.")
):
    """
    Delete a transformer configuration.

    This endpoint deletes a specified transformer configuration from the MongoDB.
    """
    result = mongo_client[mongo_db_name][transformer_collection_name].delete_one({"config_id": config_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Configuration not found")
    return {"detail": "Configuration deleted successfully"}

# Transformer Map Config Endpoints
@router.post("/configure_transformer_map", response_model=str)
async def configure_transformer_map(
        config_id: Optional[str] = Body(None, description="The unique ID for the transformer map configuration. If not provided, a new ID will be generated."),
        transformer_map: Dict[str, Union[TransformerConfig, str]] = Body(..., description="Mapping of queries to transformer configurations."),
        default_transformer: Optional[str] = Body("CharacterTextSplitter", description="The default transformer class name."),
        default_kwargs: Dict[str, Any] = Body(..., description="Default keyword arguments for the transformer."),
        default_add_prefix_to_id: Optional[str] = Body(None, description="Default prefix to add to the document ID."),
        default_add_suffix_to_id: Optional[str] = Body(None, description="Default suffix to add to the document ID."),
        default_add_split_index_to_id: bool = Body(True, description="Whether to add default split index to the document ID."),
        default_add_metadata_to_docs: Dict[str, Any] = Body(..., description="Default metadata to add to documents."),
        default_output_store: Optional[Dict[str, Any]] = Body(None, description="Default output store configuration."),
        description: Optional[str] = Body(None, description="Description of the transformer map configuration."),
        metadata: Optional[Dict[str, Any]] = Body(None, description="Metadata associated with the transformer map configuration.")
):
    """
    Configure a DocumentTransformerMap with specified parameters.

    This endpoint allows the user to set up a DocumentTransformerMap by specifying
    various parameters including the transformer map, default transformer, keyword arguments, ID prefix/suffix,
    output store configurations, description, and metadata. It returns a unique configuration ID for the transformer map.

    If `config_id` is provided, the endpoint will check if a configuration with the same ID already exists.
    If it does, an error will be returned.
    """
    try:
        if config_id and mongo_client[mongo_db_name][transformer_map_collection_name].find_one({"config_id": config_id}):
            raise HTTPException(status_code=400, detail=f"Configuration with ID {config_id} already exists.")

        if not config_id:
            config_id = str(uuid.uuid4())

        resolved_transformer_map = {}
        for query, config in transformer_map.items():
            if isinstance(config, str):
                transformer_config = mongo_client[mongo_db_name][transformer_collection_name].find_one({"config_id": config})
                if not transformer_config:
                    raise HTTPException(status_code=404, detail=f"Transformer configuration with ID {config} not found.")
                resolved_transformer_map[query] = TransformerConfig(**transformer_config)
            else:
                resolved_transformer_map[query] = TransformerConfig(
                    transformer=config.transformer,
                    kwargs=config.kwargs,
                    add_prefix_to_id=config.add_prefix_to_id,
                    add_suffix_to_id=config.add_suffix_to_id,
                    add_split_index_to_id=config.add_split_index_to_id,
                    output_store=config.output_store,
                    description=config.description,
                    metadata=config.metadata,
                    add_metadata_to_docs=config.add_metadata_to_docs
                )

        transformer_map_config = TransformerMapConfig(
            config_id=config_id,
            transformer_map=resolved_transformer_map,
            default_transformer=default_transformer if default_transformer else None,
            default_kwargs=default_kwargs,
            default_add_prefix_to_id=default_add_prefix_to_id,
            default_add_suffix_to_id=default_add_suffix_to_id,
            default_add_split_index_to_id=default_add_split_index_to_id,
            default_add_metadata_to_docs=default_add_metadata_to_docs,
            default_output_store=default_output_store,
            description=description,
            metadata=metadata
        )

        mongo_client[mongo_db_name][transformer_map_collection_name].insert_one(transformer_map_config.dict())

        return config_id
    except KeyError:
        raise HTTPException(status_code=400, detail="Transformer not found.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/get_transformer_map_config/{config_id}", response_model=TransformerMapConfig)
async def get_transformer_map_config(
        config_id: str = Path(..., description="The unique ID of the transformer map configuration to retrieve.")
):
    """
    Retrieve a transformer map configuration by its ID.

    This endpoint retrieves a specific transformer map configuration from the MongoDB using its unique ID.
    """
    config = mongo_client[mongo_db_name][transformer_map_collection_name].find_one({"config_id": config_id})
    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")
    return TransformerMapConfig(**config)

@router.post("/transform_documents/{config_id}", response_model=List[DocumentModel])
async def transform_documents(
        config_id: str = Path(..., description="The unique ID of the transformer map configuration."),
        documents: List[DocumentModel] = Body(..., description="List of documents to be transformed.")
):
    """
    Transform documents using a configured transformer map.

    This endpoint transforms documents using a pre-configured transformer map, identified by a unique configuration ID.
    The documents are transformed and returned along with their metadata. If configured, documents are also stored
    in the MongoDB document store.
    """
    config = mongo_client[mongo_db_name][transformer_map_collection_name].find_one({"config_id": config_id})
    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")

    transformer_map_config = TransformerMapConfig(**config)

    # Convert transformer names to class instances
    for query, transformer_config in transformer_map_config.transformer_map.items():
        transformer_config.transformer = get_transformer_class(transformer_config.transformer)

    default_transformer_class = get_transformer_class(transformer_map_config.default_transformer)

    transformer = DocumentTransformerMap(
        transformer_map=transformer_map_config.transformer_map,
        default_transformer=default_transformer_class,
        default_kwargs=transformer_map_config.default_kwargs,
        default_add_prefix_to_id=transformer_map_config.default_add_prefix_to_id,
        default_add_suffix_to_id=transformer_map_config.default_add_suffix_to_id,
        default_add_split_index_to_id=transformer_map_config.default_add_split_index_to_id,
        default_add_metadata_to_docs=transformer_map_config.default_add_metadata_to_docs,
        default_output_store=transformer_map_config.default_output_store
    )

    langchain_docs = [doc.to_langchain_document() for doc in documents]

    for transformer_config in transformer_map_config.transformer_map.values():
        if transformer_config.output_store:
            collection_name = transformer_config.output_store.get("collection_name")
            if collection_name:
                store_docs = load_documents_from_store(collection_name)
                langchain_docs.extend(store_docs)

    transformed_docs = transformer.transform_documents(langchain_docs)
    document_models = [DocumentModel.from_langchain_document(doc) for doc in transformed_docs]

    for transformer_config in transformer_map_config.transformer_map.values():
        if transformer_config.output_store:
            collection_name = transformer_config.output_store.get("collection_name")
            if collection_name:
                for doc_model in document_models:
                    save_document_to_store(collection_name, doc_model)

    return document_models

@router.post("/transform_documents_from_store/{config_id}", response_model=List[DocumentModel])
async def transform_documents_from_store(
        config_id: str = Path(..., description="The unique ID of the transformer map configuration."),
        input_store: Dict[str, Any] = Body(..., description="Input store configuration.")
):
    """
    Transform documents directly from a specified MongoDB collection using a configured transformer map.

    This endpoint loads documents from a specified MongoDB collection and transforms them using a pre-configured
    transformer map, identified by a unique configuration ID. The documents are transformed and returned along with
    their metadata. If configured, documents are also stored in the MongoDB document store.
    """
    config = mongo_client[mongo_db_name][transformer_map_collection_name].find_one({"config_id": config_id})
    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")

    transformer_map_config = TransformerMapConfig(**config)

    # Convert transformer names to class instances
    for query, transformer_config in transformer_map_config.transformer_map.items():
        transformer_config.transformer = get_transformer_class(transformer_config.transformer)

    default_transformer_class = get_transformer_class(transformer_map_config.default_transformer)

    transformer = DocumentTransformerMap(
        transformer_map=transformer_map_config.transformer_map,
        default_transformer=default_transformer_class,
        default_kwargs=transformer_map_config.default_kwargs,
        default_add_prefix_to_id=transformer_map_config.default_add_prefix_to_id,
        default_add_suffix_to_id=transformer_map_config.default_add_suffix_to_id,
        default_add_split_index_to_id=transformer_map_config.default_add_split_index_to_id,
        default_add_metadata_to_docs=transformer_map_config.default_add_metadata_to_docs,
        default_output_store=transformer_map_config.default_output_store
    )

    collection_name = input_store.get("collection_name")
    if not collection_name:
        raise HTTPException(status_code=400, detail="Invalid input store configuration")

    langchain_docs = load_documents_from_store(collection_name)

    transformed_docs = transformer.transform_documents(langchain_docs)
    document_models = [DocumentModel.from_langchain_document(doc) for doc in transformed_docs]

    for transformer_config in transformer_map_config.transformer_map.values():
        if transformer_config.output_store:
            collection_name = transformer_config.output_store.get("collection_name")
            if collection_name:
                for doc_model in document_models:
                    save_document_to_store(collection_name, doc_model)

    return document_models

@router.get("/list_transformer_map_configs", response_model=List[TransformerMapConfig])
async def list_transformer_map_configs(skip: int = Query(0, description="Number of records to skip"), limit: Optional[int] = Query(0, description="Maximum number of records to return")):
    """
    List all existing transformer map configurations.

    This endpoint retrieves and returns all existing transformer map configurations stored in the MongoDB.
    It is useful for viewing all available configurations.
    """
    configs = mongo_client[mongo_db_name][transformer_map_collection_name].find().skip(skip).limit(limit)
    return [TransformerMapConfig(**config) for config in configs]

@router.post("/search_transformer_map_configs", response_model=List[TransformerMapConfig])
async def search_transformer_map_configs(search_params: SearchConfig = Body(...)):
    """
    Search for transformer map configurations based on advanced criteria.

    This endpoint allows the user to search for existing transformer map configurations based on specified criteria such as
    transformer type, prefix, suffix, split index addition, and metadata.
    """
    query = {}
    if search_params.transformer:
        query["default_transformer"] = search_params.transformer
    if search_params.add_prefix_to_id:
        query["default_add_prefix_to_id"] = search_params.add_prefix_to_id
    if search_params.add_suffix_to_id:
        query["default_add_suffix_to_id"] = search_params.add_suffix_to_id
    if search_params.add_split_index_to_id is not None:
        query["default_add_split_index_to_id"] = search_params.add_split_index_to_id
    if search_params.metadata:
        for key, value in search_params.metadata.items():
            query[f"metadata.{key}"] = value

    configs = mongo_client[mongo_db_name][transformer_map_collection_name].find(query).skip(search_params.skip).limit(search_params.limit)
    return [TransformerMapConfig(**config) for config in configs]

@router.delete("/delete_transformer_map_config/{config_id}", response_model=dict)
async def delete_transformer_map_config(
        config_id: str = Path(..., description="The unique ID of the transformer map configuration to delete.")
):
    """
    Delete a transformer map configuration.

    This endpoint deletes a specified transformer map configuration from the MongoDB.
    """
    result = mongo_client[mongo_db_name][transformer_map_collection_name].delete_one({"config_id": config_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Configuration not found")
    return {"detail": "Configuration deleted successfully"}

if __name__ == "__main__":
    import uvicorn

    app = FastAPI()

    app.include_router(router, prefix="/document_transformers", tags=["document_transformers"])

    uvicorn.run(app, host="127.0.0.1", port=8103)
