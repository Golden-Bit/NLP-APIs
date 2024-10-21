from gcs_data_storage.utilities.storage import GCSFileStorage
from fastapi import FastAPI, UploadFile, File, HTTPException, Form, Query, APIRouter
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import json
import mimetypes
import os
from io import BytesIO
from PyPDF2 import PdfFileReader
from docx import Document as DocxDocument

router = APIRouter()

# Initialize GCS storage
bucket_name = "your-bucket-name"
service_account_json = "path-to-service-account.json"
file_storage = GCSFileStorage(bucket_name, service_account_json)


class FileMetadata(BaseModel):
    """
    Pydantic model for file metadata.
    """
    name: str = Field(..., description="The name of the file.")
    size: int = Field(..., description="The size of the file in bytes.")
    modified_time: str = Field(..., description="The last modified time of the file in ISO 8601 format.")
    created_time: str = Field(..., description="The creation time of the file in ISO 8601 format.")
    path: str = Field(..., description="The relative path to the file in the storage.")
    mime_type: Optional[str] = Field(None, description="The MIME type of the file, if available.")
    custom_metadata: Optional[Dict[str, Any]] = Field(None, description="Custom metadata associated with the file.")

    class Config:
        schema_extra = {
            "example": {
                "name": "example.txt",
                "size": 1024,
                "modified_time": "2023-06-26T12:00:00Z",
                "created_time": "2023-06-26T10:00:00Z",
                "path": "documents/example.txt",
                "mime_type": "text/plain",
                "custom_metadata": {"author": "John Doe", "project": "AI Research"}
            }
        }


class DirectoryMetadata(BaseModel):
    """
    Pydantic model for directory metadata.
    """
    path: str = Field(..., description="The path to the directory in the storage.")
    custom_metadata: Optional[Dict[str, Any]] = Field(None,
                                                      description="Any custom metadata associated with the directory.")

    class Config:
        schema_extra = {
            "example": {
                "path": "documents/research/",
                "custom_metadata": {"department": "Research", "category": "AI"}
            }
        }


@router.post("/create_directory", response_model=DirectoryMetadata)
async def create_directory(
        directory: str = Form(..., description="The path to the directory to create."),
        description: Optional[str] = Form(None, description="Custom description for the directory."),
        extra_metadata: Optional[str] = Form(None, description="Extra metadata for the directory in JSON format.")
):
    """
    Create a directory in GCS.
    """
    custom_metadata = {"description": description} if description else {}
    if extra_metadata:
        custom_metadata.update(json.loads(extra_metadata))
    file_storage.save_directory_metadata(directory, custom_metadata)
    return DirectoryMetadata(path=directory, custom_metadata=custom_metadata)


@router.delete("/delete_directory/{directory_id:path}")
async def delete_directory(directory_id: str):
    """
    Delete a directory and its metadata from GCS.
    """
    file_storage.delete_directory_metadata(directory_id)
    return {"detail": "Directory deleted successfully"}


@router.post("/upload", response_model=FileMetadata)
async def upload_file(
        file: UploadFile = File(...),
        subdir: Optional[str] = Form(None),
        file_description: Optional[str] = Form(None),
        extra_metadata: Optional[str] = Form(None)
):
    """
    Upload a file to GCS.
    """
    file_path = os.path.join(subdir, file.filename) if subdir else file.filename
    file_path = file_path.replace("\\", "/")

    content = await file.read()
    custom_metadata = {"file_description": file_description} if file_description else {}
    if extra_metadata:
        custom_metadata.update(json.loads(extra_metadata))

    file_storage.save_file(file_path, content, custom_metadata)
    metadata = file_storage.get_file_metadata(file_path)
    return metadata


@router.post("/upload/multiple", response_model=Dict[str, List[str]])
async def upload_multiple_files(
        files: List[UploadFile] = File(...),
        subdir: Optional[str] = Form(None),
        file_description: Optional[str] = Form(None),
        extra_metadata: Optional[str] = Form(None)
):
    """
    Upload multiple files to GCS.
    """
    ids = []
    for file in files:
        file_path = os.path.join(subdir, file.filename) if subdir else file.filename
        file_path = file_path.replace("\\", "/")

        content = await file.read()
        custom_metadata = {"file_description": file_description} if file_description else {}
        if extra_metadata:
            custom_metadata.update(json.loads(extra_metadata))

        file_storage.save_file(file_path, content, custom_metadata)
        ids.append(file_path)
    return {"file_ids": ids}


@router.put("/update/{file_id:path}", response_model=FileMetadata)
async def update_file(
        file_id: str,
        file: UploadFile = File(...),
        file_description: Optional[str] = Form(None),
        extra_metadata: Optional[str] = Form(None)
):
    """
    Update an existing file in GCS.
    """
    content = await file.read()
    if not file_storage.get_file(file_id):
        raise HTTPException(status_code=404, detail="File not found")

    custom_metadata = {"file_description": file_description} if file_description else {}
    if extra_metadata:
        custom_metadata.update(json.loads(extra_metadata))

    file_storage.update_file(file_id, content, custom_metadata)
    metadata = file_storage.get_file_metadata(file_id)
    return metadata


@router.delete("/delete/{file_id:path}")
async def delete_file(file_id: str):
    """
    Delete a file and its metadata from GCS.
    """
    if not file_storage.get_file(file_id):
        raise HTTPException(status_code=404, detail="File not found")
    file_storage.delete_file(file_id)
    return {"detail": "File deleted successfully"}


@router.get("/file/{file_id:path}", response_class=FileResponse)
async def get_file(file_id: str):
    """
    Retrieve a file from GCS.
    """
    content = file_storage.get_file(file_id)
    if not content:
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(path=os.path.join("temp", file_id), filename=file_id)


@router.get("/metadata/{file_id:path}", response_model=FileMetadata)
async def get_file_metadata(file_id: str):
    """
    Retrieve metadata for a file in GCS.
    """
    metadata = file_storage.get_file_metadata(file_id)
    if not metadata:
        raise HTTPException(status_code=404, detail="File not found")
    return metadata


@router.get("/files", response_model=List[FileMetadata])
async def list_files(subdir: Optional[str] = Query(None)):
    """
    List all files in GCS.
    """
    files = file_storage.list_files(subdir)
    metadata_list = [file_storage.get_file_metadata(file) for file in files]
    return metadata_list


if __name__ == "__main__":
    import uvicorn

    app = FastAPI()
    app.include_router(router, prefix="/data_stores", tags=["data_stores"])
    uvicorn.run(app, host="127.0.0.1", port=8100)
