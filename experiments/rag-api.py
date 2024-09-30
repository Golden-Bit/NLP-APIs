import json

from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form, Query
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import httpx
import uuid

app = FastAPI()

BASE_URL = "http://34.140.110.56:8100"

# Models for handling requests and responses
class ContextMetadata(BaseModel):
    path: str
    custom_metadata: Optional[Dict[str, Any]] = None

class FileUploadResponse(BaseModel):
    file_id: str
    contexts: List[str]

# Helper function to communicate with the existing API
async def create_context_on_server(context_path: str, metadata: Optional[Dict[str, Any]] = None):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/data_stores/create_directory",
            data={
                "directory": context_path,
                "extra_metadata": metadata and json.dumps(metadata)
            }
        )
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json())
        return response.json()

async def delete_context_on_server(context_path: str):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{BASE_URL}/data_stores/delete_directory/{context_path}")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json())
        return response.json()

async def list_contexts_from_server():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/data_stores/directories")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json())
        return response.json()


async def upload_file_to_contexts_(file: UploadFile, contexts: List[str],
                                  file_metadata: Optional[Dict[str, Any]] = None):
    file_uuid = str(uuid.uuid4())  # Generate a UUID for the file
    file_content = await file.read()  # Read the file content once and reuse it

    contexts = contexts[0].split(',')

    async with httpx.AsyncClient() as client:
        responses = []
        # Sequentially upload the file to each context
        for context in contexts:
            # Ensure that each context is handled separately and not concatenated
            data = {
                "subdir": context,  # Here, context is passed as a single string, not a concatenation
                "extra_metadata": json.dumps({"file_uuid": file_uuid, **(file_metadata or {})}),
            }
            files = {"file": (file.filename, file_content, file.content_type)}

            # Make the POST request to upload the file to the current context
            response = await client.post(f"{BASE_URL}/data_stores/upload", data=data, files=files)

            # Log and handle errors
            if response.status_code != 200:
                print(
                    f"Error uploading to {context}. Status Code: {response.status_code}. Response content: {response.content}")

                try:
                    error_detail = response.json()
                except ValueError:
                    raise HTTPException(status_code=response.status_code, detail=f"Error: {response.text}")

                raise HTTPException(status_code=response.status_code, detail=error_detail)

            # Collect response data for successful uploads
            try:
                responses.append(response.json())
            except ValueError:
                raise HTTPException(status_code=500, detail="Received invalid JSON response from the server")

        # Return the collected responses with file UUID and associated contexts
        return {"file_id": file_uuid, "contexts": contexts}


async def upload_file_to_contexts(file: UploadFile,
                                  contexts: List[str],
                                  file_metadata: Optional[Dict[str, Any]] = None):

    file_uuid = str(uuid.uuid4())  # Generate a UUID for the file
    file_content = await file.read()  # Read the file content once and reuse it

    contexts = contexts[0].split(',')

    async with httpx.AsyncClient() as client:
        responses = []
        # Sequentially upload the file to each context
        for context in contexts:
            # Upload the file
            data = {
                "subdir": context,
                "extra_metadata": json.dumps({"file_uuid": file_uuid, **(file_metadata or {})}),
            }
            files = {"file": (file.filename, file_content, file.content_type)}

            # Make the POST request to upload the file to the current context
            response = await client.post(f"{BASE_URL}/data_stores/upload", data=data, files=files)

            if response.status_code != 200:
                print(
                    f"Error uploading to {context}. Status Code: {response.status_code}. Response content: {response.content}")
                try:
                    error_detail = response.json()
                except ValueError:
                    raise HTTPException(status_code=response.status_code, detail=f"Error: {response.text}")

                raise HTTPException(status_code=response.status_code, detail=error_detail)

            # Collect response data for successful uploads
            try:
                upload_response = response.json()
                responses.append(upload_response)
            except ValueError:
                raise HTTPException(status_code=500, detail="Received invalid JSON response from the server")

            # Configure the loader for the uploaded file
            loader_config_id = f"{context}_{file.filename}_loader"
            doc_store_collection_name = f"{context}_{file.filename}_collection"

            loader_config_data = {
                "config_id": loader_config_id,
                "path": f"data_stores/data/{context}",
                "loader_map": {
                  f"{file.filename}": "PyMuPDFLoader"
                },
                "loader_kwargs_map": {
                  f"{file.filename}": {"extract_images": True}
                },
                "metadata_map": {
                  f"{file.filename}": {
                    "source_context": f"{context}"
                  }
                },
                "default_metadata": {
                   "source_context": f"{context}"
                },
                "recursive": True,
                "max_depth": 5,
                "silent_errors": True,
                "load_hidden": True,
                "show_progress": True,
                "use_multithreading": True,
                "max_concurrency": 8,
                "exclude": [
                  "*.tmp",
                  "*.log"
                ],
                "sample_size": 10,
                "randomize_sample": True,
                "sample_seed": 42,
                "output_store_map": {
                  f"{file.filename}": {
                    "collection_name": doc_store_collection_name
                  }
                },
                "default_output_store": {
                  "collection_name": doc_store_collection_name
                }
              }

            # Configure the loader on the original API
            loader_response = await client.post(f"{BASE_URL}/document_loaders/configure_loader", json=loader_config_data)
            if loader_response.status_code != 200 and loader_response.status_code != 400:
                raise HTTPException(status_code=loader_response.status_code, detail=loader_response.json())

            # Apply the loader to process the document
            load_response = await client.post(f"{BASE_URL}/document_loaders/load_documents/{loader_config_id}")
            if load_response.status_code != 200:
                raise HTTPException(status_code=load_response.status_code, detail=load_response.json())

            # Collect document processing results
            #processed_docs = load_response.json()

            ### Configure the Vector Store ###

            vector_store_config_id = f"{context}_vector_store_config"
            vector_store_id = f"{context}_vector_store"

            vector_store_config = {
                "config_id": vector_store_config_id,
                "store_id": vector_store_id,
                "vector_store_class": "Chroma",  # Example: using Chroma vector store, modify as necessary
                "params": {
                    "persist_directory": f"vector_stores/{context}"
                },
                "embeddings_model_class": "OpenAIEmbeddings",
                "embeddings_params": {
                    "api_key": "API_KEY"  # Replace with actual API key or environment variable
                },
                "description": f"Vector store for context {context}",
                "custom_metadata": {
                    "source_context": context
                }
            }

            # Configure the vector store
            vector_store_response = await client.post(
                f"{BASE_URL}/vector_stores/vector_store/configure", json=vector_store_config)
            if vector_store_response.status_code != 200 and vector_store_response.status_code != 400:
                raise HTTPException(status_code=vector_store_response.status_code, detail=vector_store_response.json())

            #vector_store_config_id = vector_store_response.json()["config_id"]

            ### Load the Vector Store ###
            load_vector_response = await client.post(f"{BASE_URL}/vector_stores/vector_store/load/{vector_store_config_id}")
            if load_vector_response.status_code != 200 and load_vector_response.status_code != 400:
                raise HTTPException(status_code=load_vector_response.status_code, detail=load_vector_response.json())

            ### Add Documents from the Document Store to the Vector Store ###
            # Use the document collection name associated with the context
            add_docs_response = await client.post(
                f"{BASE_URL}/vector_stores/vector_store/add_documents_from_store/{vector_store_id}",
                params={"document_collection": doc_store_collection_name})
            if add_docs_response.status_code != 200:
                raise HTTPException(status_code=add_docs_response.status_code, detail=add_docs_response.json())

            print(add_docs_response.json())

        # Return the collected responses with file UUID and associated contexts
        return {"file_id": file_uuid, "contexts": contexts}


# Create a new context (directory)
@app.post("/contexts", response_model=ContextMetadata)
async def create_context(context_name: str = Form(...), description: Optional[str] = Form(None)):
    metadata = {"description": description} if description else None
    result = await create_context_on_server(context_name, metadata)
    return result

# Delete an existing context (directory)
@app.delete("/contexts/{context_name}", response_model=Dict[str, Any])
async def delete_context(context_name: str):
    result = await delete_context_on_server(context_name)
    return result

# List all available contexts
@app.get("/contexts", response_model=List[ContextMetadata])
async def list_contexts():
    result = await list_contexts_from_server()
    return result

# Upload a file to multiple contexts
@app.post("/upload", response_model=FileUploadResponse)
async def upload_file_to_multiple_contexts(
        file: UploadFile = File(...),
        contexts: List[str] = Form(...),
        description: Optional[str] = Form(None)
):
    file_metadata = {"description": description} if description else None
    result = await upload_file_to_contexts(file, contexts, file_metadata)
    return result


# Helper function to list files by context
async def list_files_in_context(contexts: Optional[List[str]] = None):
    async with httpx.AsyncClient() as client:
        if contexts:
            # If contexts are provided, filter files by those contexts
            files = []
            for context in contexts:
                response = await client.get(f"{BASE_URL}/data_stores/files", params={"subdir": context})
                if response.status_code != 200:
                    raise HTTPException(status_code=response.status_code, detail=response.json())
                files.extend(response.json())
            return files
        else:
            # No context specified, list all files across all contexts
            response = await client.get(f"{BASE_URL}/data_stores/files")
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail=response.json())
            return response.json()


# Helper function to delete files by UUID
async def delete_file_by_id(file_id: str):
    async with httpx.AsyncClient() as client:
        # List all contexts to find where the file exists
        response = await client.get(f"{BASE_URL}/data_stores/files")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json())

        # Delete the file from all contexts where the UUID matches
        files = response.json()
        for file in files:
            if file['custom_metadata'].get('file_uuid') == file_id:
                path = file['path']
                delete_response = await client.delete(f"{BASE_URL}/data_stores/delete/{path}")
                if delete_response.status_code != 200:
                    raise HTTPException(status_code=delete_response.status_code, detail=delete_response.json())
        return {"detail": f"File with ID {file_id} deleted from all contexts"}


# Helper function to delete file by path
async def delete_file_by_path(file_path: str):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{BASE_URL}/delete/data_stores/{file_path}")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json())
        return {"detail": f"File at path {file_path} deleted successfully"}


# Endpoint to list files by specific context(s)
@app.get("/files", response_model=List[Dict[str, Any]])
async def list_files(contexts: Optional[List[str]] = Query(None)):
    """
    List files for specific contexts. If no contexts are provided, list all files.
    """
    result = await list_files_in_context(contexts)
    return result


# Endpoint to delete files by either UUID (deletes from all contexts) or path (deletes from a specific context)
@app.delete("/files")
async def delete_file(file_id: Optional[str] = Query(None), file_path: Optional[str] = Query(None)):
    """
    Delete a file by either its UUID (from all contexts) or its path (from a specific context).
    """
    if file_id:
        # Delete by UUID from all contexts
        result = await delete_file_by_id(file_id)
    elif file_path:
        # Delete by path from a specific context
        result = await delete_file_by_path(file_path)
    else:
        raise HTTPException(status_code=400, detail="Either file_id or file_path must be provided")

    return result