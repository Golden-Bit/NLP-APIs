import os

from fastapi import FastAPI, HTTPException, Query, Path, Body, APIRouter
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from langchain_core.documents import Document
from pymongo import MongoClient, UpdateOne
import uuid

router = APIRouter()

# MongoDB connection configuration
MONGO_CONNECTION_STRING = os.getenv('MONGO_CONNECTION_STRING', 'localhost')
client = MongoClient(MONGO_CONNECTION_STRING)
db_name = "document_store"
metadata_collection_name = "collections_metadata"


def create_indexes():
    """Create indexes to improve search and filter performance."""
    db = client[db_name]
    collections = db.list_collection_names()
    for collection_name in collections:
        collection = db[collection_name]
        try:
            collection.create_index("metadata.id")
            collection.create_index("metadata.title")
            collection.create_index("page_content")
        except Exception as e:
            print(f"Error creating index on collection {collection_name}: {e}")


# Create indexes on startup
create_indexes()


class DocumentModel(BaseModel):
    page_content: str = Field(..., description="The content of the document.",
                              example="This is the content of the document.")
    metadata: Dict[str, Any] = Field({}, description="Metadata associated with the document.",
                                     example={"author": "John Doe", "category": "Research"})
    type: str = Field("Document", description="The type of the document.", example="Document")

    @staticmethod
    def from_langchain_document(doc: Document) -> 'DocumentModel':
        """Create a DocumentModel from a LangChain Document."""
        return DocumentModel(
            page_content=doc.page_content,
            metadata=doc.metadata,
            type=doc.type
        )

    def to_langchain_document(self) -> Document:
        """Convert DocumentModel to a LangChain Document."""
        return Document(
            page_content=self.page_content,
            metadata=self.metadata,
            type=self.type
        )


from typing import Dict

class CollectionMetadataModel(BaseModel):
    collection_name: str = Field(None, description="The name of the collection.", example="example_collection")
    description: Optional[str] = Field(None, description="Description of the collection.",
                                       example="This collection contains research documents.")
    created_at: Optional[str] = Field(None, description="The creation date of the collection.",
                                      example="2023-01-01T00:00:00Z")
    custom_metadata: Optional[Dict[str, Any]] = Field(None, description="Custom metadata for the collection.")

    @staticmethod
    def from_dict(data: dict) -> 'CollectionMetadataModel':
        return CollectionMetadataModel(**data)


def get_collection(collection_name: str):
    """Get a MongoDB collection based on the provided name.

    Args:
        collection_name (str): The name of the collection.

    Returns:
        Collection: The MongoDB collection.
    """
    return client[db_name][collection_name]


def get_metadata_collection():
    """Get the MongoDB collection for storing collections metadata.

    Returns:
        Collection: The MongoDB collection for metadata.
    """
    return client[db_name][metadata_collection_name]


@router.post("/documents/{collection_name}/", response_model=DocumentModel)
async def create_document(
        collection_name: str = Path(..., description="The name of the collection.", example="example_collection"),
        doc: DocumentModel = Body(..., description="The document to create.",
                                  example={"page_content": "This is the content of the document.",
                                           "metadata": {"author": "John Doe", "category": "Research"},
                                           "type": "Document"})
):
    """
    Create a new document in the specified collection.

    This endpoint allows the creation of a new document in a given MongoDB collection.
    The document's content and metadata are provided in the request body.

    Returns the created document with an added unique ID in its metadata.
    """
    collection = get_collection(collection_name)
    document = doc.to_langchain_document()

    key = doc.metadata.get("id", str(uuid.uuid4()))
    doc.metadata.update({"doc_store_id": key})
    document.metadata.update({"doc_store_id": key, "doc_store_collection": collection_name})

    collection.update_one(
        {"_id": key}, {"$set": {
            "value": {"page_content": document.page_content, "metadata": document.metadata, "type": document.type}}},
        upsert=True
    )

    return doc


@router.get("/documents/{collection_name}/{doc_id}", response_model=DocumentModel)
async def get_document(
        collection_name: str = Path(..., description="The name of the collection.", example="example_collection"),
        doc_id: str = Path(..., description="The ID of the document to retrieve.",
                           example="abcd1234-efgh-5678-ijkl-9012mnop3456")
):
    """
    Retrieve a document by its ID from the specified collection.

    This endpoint fetches a document from a given MongoDB collection using the document's ID.
    If the document is found, it is returned with its content and metadata. Otherwise, a 404 error is raised.
    """
    collection = get_collection(collection_name)
    result = collection.find_one({"_id": doc_id})
    if not result:
        raise HTTPException(status_code=404, detail="Document not found")
    doc = Document(**result["value"])
    return DocumentModel.from_langchain_document(doc)


@router.delete("/documents/{collection_name}/{doc_id}")
async def delete_document(
        collection_name: str = Path(..., description="The name of the collection.", example="example_collection"),
        doc_id: str = Path(..., description="The ID of the document to delete.",
                           example="abcd1234-efgh-5678-ijkl-9012mnop3456")
):
    """
    Delete a document by its ID from the specified collection.

    This endpoint deletes a document from a given MongoDB collection using the document's ID.
    Returns a confirmation message upon successful deletion.
    """
    collection = get_collection(collection_name)
    collection.delete_one({"_id": doc_id})
    return {"detail": "Document deleted successfully"}


@router.put("/documents/{collection_name}/{doc_id}", response_model=DocumentModel)
async def update_document(
        collection_name: str = Path(..., description="The name of the collection.", example="example_collection"),
        doc_id: str = Path(..., description="The ID of the document to update.",
                           example="abcd1234-efgh-5678-ijkl-9012mnop3456"),
        doc: DocumentModel = Body(..., description="The updated document data.",
                                  example={"page_content": "This is the updated content of the document.",
                                           "metadata": {"author": "John Doe", "category": "Research"},
                                           "type": "Document"})
):
    """
    Update an existing document by its ID in the specified collection.

    This endpoint updates the content and metadata of an existing document in a given MongoDB collection.
    If the document is found and updated, the new document data is returned. Otherwise, a 404 error is raised.
    """
    collection = get_collection(collection_name)
    existing_doc = collection.find_one({"_id": doc_id})
    if not existing_doc:
        raise HTTPException(status_code=404, detail="Document not found")

    updated_document = doc.to_langchain_document()
    collection.update_one(
        {"_id": doc_id}, {"$set": {
            "value": {"page_content": updated_document.page_content, "metadata": updated_document.metadata,
                      "type": updated_document.type}}}
    )
    return doc


@router.get("/documents/{collection_name}/", response_model=List[DocumentModel])
async def list_documents(
        collection_name: str = Path(..., description="The name of the collection.", example="example_collection"),
        prefix: Optional[str] = Query(None, description="Prefix to filter documents.", example="prefix_"),
        skip: int = Query(0, ge=0, description="Number of documents to skip.", example=0),
        limit: int = Query(10, ge=1, description="Maximum number of documents to return.", example=10)
):
    """
    List documents in the specified collection with pagination.

    This endpoint lists documents from a given MongoDB collection, with optional prefix filtering.
    Pagination is supported via `skip` and `limit` query parameters.
    """
    collection = get_collection(collection_name)
    query = {"_id": {"$regex": f"^{prefix}"}} if prefix else {}
    result = collection.find(query).skip(skip).limit(limit)
    documents = [Document(**doc["value"]) for doc in result]
    return [DocumentModel.from_langchain_document(doc) for doc in documents]


@router.get("/search/{collection_name}/", response_model=List[DocumentModel])
async def search_documents(
        collection_name: str = Path(..., description="The name of the collection.", example="example_collection"),
        query: str = Query(..., description="The search query.", example="search_term"),
        skip: int = Query(0, ge=0, description="Number of documents to skip.", example=0),
        limit: int = Query(10, ge=1, description="Maximum number of documents to return.", example=10)
):
    """
    Search for documents by query in the specified collection with pagination.

    This endpoint searches for documents in a given MongoDB collection using a query string.
    The search is performed on the document's content and metadata. Pagination is supported via `skip` and `limit` query parameters.
    """
    collection = get_collection(collection_name)
    regex = {"$regex": query, "$options": "i"}
    search_query = {
        "$or": [
            {"page_content": regex},
            {"metadata.title": regex},
            {"metadata.id": regex}
        ]
    }
    result = collection.find(search_query).skip(skip).limit(limit)
    documents = [Document(**doc["value"]) for doc in result]
    return [DocumentModel.from_langchain_document(doc) for doc in documents]


@router.post("/collections/{collection_name}/metadata", response_model=CollectionMetadataModel)
async def create_collection_metadata(
        collection_name: str = Path(..., description="The name of the collection.", example="example_collection"),
        metadata: CollectionMetadataModel = Body(..., description="Metadata for the collection.")
):
    """
    Create or update metadata for a specified collection.

    This endpoint allows the creation or update of metadata for a given MongoDB collection.
    The metadata includes a description, creation date, and custom metadata.
    """
    metadata_collection = get_metadata_collection()
    metadata_data = metadata.dict()
    metadata_data["collection_name"] = collection_name
    metadata_collection.update_one(
        {"collection_name": collection_name}, {"$set": metadata_data}, upsert=True
    )
    return metadata


@router.put("/collections/{collection_name}/metadata", response_model=CollectionMetadataModel)
async def update_collection_metadata(
        collection_name: str = Path(..., description="The name of the collection.", example="example_collection"),
        metadata: CollectionMetadataModel = Body(..., description="Updated metadata for the collection.")
):
    """
    Update metadata for a specified collection.

    This endpoint allows updating metadata for a given MongoDB collection.
    The metadata includes a description, creation date, and custom metadata.
    """
    metadata_collection = get_metadata_collection()
    existing_metadata = metadata_collection.find_one({"collection_name": collection_name})
    if not existing_metadata:
        raise HTTPException(status_code=404, detail="Collection metadata not found")

    # Update only fields that are provided in the request
    update_data = {}
    if metadata.description:
        update_data["description"] = metadata.description
    if metadata.created_at:
        update_data["created_at"] = metadata.created_at
    if metadata.custom_metadata:
        update_data["custom_metadata"] = metadata.custom_metadata

    metadata_collection.update_one(
        {"collection_name": collection_name}, {"$set": update_data}
    )

    updated_metadata = metadata_collection.find_one({"collection_name": collection_name})
    return CollectionMetadataModel.from_dict(updated_metadata)


@router.get("/collections/metadata", response_model=List[CollectionMetadataModel])
async def list_collections_metadata():
    """
    List all collections and their metadata.

    This endpoint retrieves and returns a list of all collections in the MongoDB database along with their metadata.
    """
    metadata_collection = get_metadata_collection()
    metadata_list = list(metadata_collection.find({}, {"_id": 0}))
    return metadata_list


if __name__ == "__main__":
    import uvicorn

    app = FastAPI()

    app.include_router(router, prefix="/document_stores", tags=["document_stores"])

    uvicorn.run(app, host="127.0.0.1", port=8102)
