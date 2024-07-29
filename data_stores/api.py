from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException, Form, Query, APIRouter
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from data_stores.utilities.storage import FileStorage
import json
import os
import mimetypes
from PyPDF2 import PdfFileReader
from io import BytesIO
from docx import Document as DocxDocument

router = APIRouter()

# Initialize the root path for storing files
#root_path = Path.cwd() / "workspace" / "data_stores" / "data"
#root_path = Path(str(Path.cwd()).replace("chains", "data_stores")) / "data"
root_path = Path(str(Path.cwd())) / "data_stores" / "data"
file_storage = FileStorage(root_path)


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
    custom_metadata: Optional[Dict[str, Any]] = Field(None, description="Any custom metadata associated with the file.",
                                                      example={"author": "John Doe", "project": "AI Research"})

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
                                                      description="Any custom metadata associated with the directory.",
                                                      example={"department": "Research", "category": "AI"})

    class Config:
        schema_extra = {
            "example": {
                "path": "documents/research/",
                "custom_metadata": {"department": "Research", "category": "AI"}
            }
        }


@router.post("/create_directory", response_model=DirectoryMetadata,
          responses={400: {"description": "Bad Request"}, 500: {"description": "Internal Server Error"}})
async def create_directory(
        directory: str = Form(..., description="The path to the directory to create."),
        description: Optional[str] = Form(None, description="Custom description for the directory."),
        extra_metadata: Optional[str] = Form(None, description="Extra metadata for the directory in JSON format.")
):
    """
    Create a directory on the server. This endpoint creates a directory at the specified path and attaches any provided custom metadata.
    """
    dir_path = root_path / directory
    if not dir_path.exists():
        dir_path.mkdir(parents=True, exist_ok=True)

    custom_metadata = {"description": description} if description else {}
    if extra_metadata:
        custom_metadata.update(json.loads(extra_metadata))
    file_storage.save_directory_metadata(directory, custom_metadata)
    return DirectoryMetadata(path=directory, custom_metadata=custom_metadata)


@router.delete("/delete_directory/{directory_id:path}",
            responses={404: {"description": "Directory Not Found"}, 400: {"description": "Bad Request"},
                       500: {"description": "Internal Server Error"}})
async def delete_directory(directory_id: str):
    """
    Delete a directory and its metadata. This endpoint removes a specified directory from the server along with
    any associated metadata. If the directory does not exist, a 404 error is returned.
    """
    dir_path = root_path / directory_id
    if not dir_path.exists() or not dir_path.is_dir():
        raise HTTPException(status_code=404, detail="Directory not found")

    # Remove the directory and all its contents
    for item in dir_path.glob("**/*"):
        if item.is_file():
            item.unlink()
        elif item.is_dir():
            item.rmdir()

    dir_path.rmdir()
    file_storage.delete_directory_metadata(directory_id)
    return {"detail": "Directory deleted successfully"}


@router.post("/upload", response_model=FileMetadata,
          responses={400: {"description": "Bad Request"}, 500: {"description": "Internal Server Error"}})
async def upload_file(
        file: UploadFile = File(..., description="The file to upload."),
        subdir: Optional[str] = Form(None, description="The subdirectory to save the file in."),
        file_description: Optional[str] = Form(None, description="Custom description for the file."),
        extra_metadata: Optional[str] = Form(None, description="Extra metadata for the file in JSON format.")
):
    """
    Upload a file to the server. The file can be saved in a specific subdirectory and custom metadata can be added.
    This endpoint reads the content of the uploaded file, saves it to the specified or default location,
    and attaches any provided custom metadata. The metadata of the uploaded file is then returned.
    """
    if subdir:
        file_path = os.path.join(subdir, file.filename)
    else:
        file_path = file.filename

    # Normalize the file path
    file_path = file_path.replace("\\", "/")

    content = await file.read()
    custom_metadata = {"file_description": file_description} if file_description else {}
    if extra_metadata:
        custom_metadata.update(json.loads(extra_metadata))
    file_storage.save_file(file_path, content, custom_metadata)
    metadata = file_storage.get_file_metadata(file_path)
    return metadata


@router.post("/upload/multiple", response_model=Dict[str, List[str]],
          responses={400: {"description": "Bad Request"}, 500: {"description": "Internal Server Error"}})
async def upload_multiple_files(
        files: List[UploadFile] = File(..., description="The list of files to upload."),
        subdir: Optional[str] = Form(None, description="The subdirectory to save the files in."),
        file_description: Optional[str] = Form(None, description="Custom description for the files."),
        extra_metadata: Optional[str] = Form(None, description="Extra metadata for the files in JSON format.")
):
    """
    Upload multiple files to the server. Files can be saved in a specific subdirectory and custom metadata can be added.
    This endpoint processes a list of uploaded files, saves each one to the specified or default location,
    and attaches any provided custom metadata. The paths of the uploaded files are then returned.
    """
    ids = []
    for file in files:
        if subdir:
            file_path = os.path.join(subdir, file.filename)
        else:
            file_path = file.filename

        # Normalize the file path
        file_path = file_path.replace("\\", "/")

        content = await file.read()
        custom_metadata = {"file_description": file_description} if file_description else {}
        if extra_metadata:
            custom_metadata.update(json.loads(extra_metadata))
        file_storage.save_file(file_path, content, custom_metadata)
        ids.append(file_path)
    return {"file_ids": ids}


@router.put("/update/{file_id:path}", response_model=FileMetadata,
         responses={404: {"description": "File Not Found"}, 400: {"description": "Bad Request"},
                    500: {"description": "Internal Server Error"}})
async def update_file(
        file_id: str,
        file: UploadFile = File(..., description="The new file content."),
        file_description: Optional[str] = Form(None, description="Custom description for the file."),
        extra_metadata: Optional[str] = Form(None, description="Extra metadata for the file in JSON format.")
):
    """
    Update an existing file and its custom metadata. This endpoint replaces the content of an existing file
    with new content and updates the associated metadata. If the file does not exist, a 404 error is returned.
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


@router.post("/file/metadata",
          response_model=FileMetadata,
          responses={
              400: {"description": "Bad Request"},
              404: {"description": "File Not Found"},
              500: {"description": "Internal Server Error"}
          })
async def save_file_metadata(
        file_id: str = Form(..., description="The path to the file."),
        file_description: Optional[str] = Form(None, description="Custom description for the file."),
        extra_metadata: Optional[str] = Form(None, description="Extra metadata for the file in JSON format.")
):
    """
    Save metadata for a file. This endpoint attaches custom metadata to a specified file
    and saves it on the server. The metadata of the file is then returned.
    """
    if not file_storage.get_file(file_id):
        raise HTTPException(status_code=404, detail="File not found")

    custom_metadata = {"file_description": file_description} if file_description else {}
    if extra_metadata:
        custom_metadata.update(json.loads(extra_metadata))
    file_storage.save_file_metadata(file_id, custom_metadata)
    metadata = file_storage.get_file_metadata(file_id)
    return metadata


@router.delete("/delete/{file_id:path}",
            responses={404: {"description": "File Not Found"}, 400: {"description": "Bad Request"},
                       500: {"description": "Internal Server Error"}})
async def delete_file(file_id: str):
    """
    Delete a file and its metadata. This endpoint removes a specified file from the server along with
    any associated metadata. If the file does not exist, a 404 error is returned.
    """
    if not file_storage.get_file(file_id):
        raise HTTPException(status_code=404, detail="File not found")
    file_storage.delete_file(file_id)
    return {"detail": "File deleted successfully"}


@router.get("/file/{file_id:path}", response_class=FileResponse,
         responses={404: {"description": "File Not Found"}, 400: {"description": "Bad Request"},
                    500: {"description": "Internal Server Error"}})
async def get_file(file_id: str):
    """
    Retrieve a file from the server. This endpoint returns the content of a specified file.
    If the file does not exist, a 404 error is returned.
    """
    content = file_storage.get_file(file_id)
    if not content:
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path=os.path.join(file_storage.store.root_path, file_id), filename=file_id)


@router.get("/files", response_model=List[FileMetadata],
         responses={400: {"description": "Bad Request"}, 500: {"description": "Internal Server Error"}})
async def list_files(
        subdir: Optional[str] = Query(None, description="The subdirectory to list files from.")
):
    """
    List all files on the server. This endpoint returns metadata for all files stored on the server.
    Optionally, it can list files from a specific subdirectory.
    """
    files = file_storage.list_files(subdir)
    metadata_list = [file_storage.get_file_metadata(file) for file in files]
    return metadata_list


@router.get("/metadata/{file_id:path}", response_model=FileMetadata,
         responses={404: {"description": "File Not Found"}, 400: {"description": "Bad Request"},
                    500: {"description": "Internal Server Error"}})
async def get_file_metadata(file_id: str):
    """
    Retrieve metadata for a specific file. This endpoint returns the metadata of a specified file.
    If the file does not exist, a 404 error is returned.
    """
    metadata = file_storage.get_file_metadata(file_id)
    if not metadata:
        raise HTTPException(status_code=404, detail="File not found")
    return metadata


@router.get("/versions/{file_id:path}",
         responses={404: {"description": "File Not Found"}, 400: {"description": "Bad Request"},
                    500: {"description": "Internal Server Error"}})
async def get_file_versions(file_id: str):
    """
    Retrieve versions of a file. This endpoint returns a list of all versions of a specified file.
    Note: Versioning is not implemented yet and this endpoint currently returns a placeholder message.
    """
    return {"detail": "Versioning not implemented yet"}


@router.get("/directories", response_model=List[DirectoryMetadata],
         responses={400: {"description": "Bad Request"}, 500: {"description": "Internal Server Error"}})
async def list_directories():
    """
    List all directories in the storage. This endpoint returns metadata for all directories stored on the server.
    """
    directories = file_storage.list_directories()
    metadata_list = [DirectoryMetadata(path=dir, custom_metadata=file_storage.get_directory_metadata(dir)) for dir in
                     directories]
    return metadata_list


@router.post("/directory/metadata",
          response_model=DirectoryMetadata,
          responses={
              400: {"description": "Bad Request"},
              500: {"description": "Internal Server Error"}
          })
async def save_directory_metadata(
        directory: str = Form(
            ...,
            description="The directory path."),
        description: Optional[str] = Form(
            None,
            description="Custom description for the directory."),
        extra_metadata: Optional[str] = Form(
            None,
            description="Extra metadata for the directory in JSON format.")
):
    """
    Save metadata for a directory. This endpoint attaches custom metadata to a specified directory
    and saves it on the server. The metadata of the directory is then returned.
    """
    custom_metadata = {"description": description} if description else {}
    if extra_metadata:
        custom_metadata.update(json.loads(extra_metadata))
    file_storage.save_directory_metadata(directory, custom_metadata)
    return DirectoryMetadata(path=directory, custom_metadata=custom_metadata)


@router.get("/search/files",
         response_model=List[FileMetadata],
         responses={
             400: {"description": "Bad Request"},
             500: {"description": "Internal Server Error"}
         })
async def search_files(
        query: str = Query(
            ...,
            description="The search query."),
        subdir: Optional[str] = Query(
            None,
            description="The subdirectory to search within.")
):
    """
    Search for files based on a query. This endpoint returns metadata for files that match the search query.
    Optionally, it can search within a specific subdirectory.
    """
    files = file_storage.search_files(query, subdir)
    metadata_list = [file_storage.get_file_metadata(file) for file in files]
    return metadata_list


@router.get("/filter/files",
         response_model=List[FileMetadata],
         responses={
             400: {"description": "Bad Request"},
             500: {"description": "Internal Server Error"}
         })
async def filter_files(
        mime_type: Optional[str] = Query(
            None,
            description="The MIME type to filter by."),
        min_size: Optional[int] = Query(
            None,
            description="The minimum file size in bytes."),
        max_size: Optional[int] = Query(
            None,
            description="The maximum file size in bytes.")
):
    """
    Filter files based on MIME type and size. This endpoint returns metadata for files that match the specified filters.
    """
    files = file_storage.filter_files(mime_type, min_size, max_size)
    metadata_list = [file_storage.get_file_metadata(file) for file in files]
    return metadata_list


@router.get("/view/{file_id:path}", response_class=HTMLResponse,
         responses={404: {"description": "File Not Found"}, 400: {"description": "Bad Request"},
                    500: {"description": "Internal Server Error"}})
async def view_file(file_id: str):
    """
    View a file in its readable representation. This endpoint returns the content of a specified file in a readable format.
    If the file does not exist, a 404 error is returned.
    """
    file_path = os.path.join(file_storage.store.root_path, file_id)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type:
        mime_type = "application/octet-stream"

    if mime_type in ["text/plain", "application/pdf", "application/msword",
                     "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        with open(file_path, "rb") as file:
            content = file.read()
        if mime_type == "application/pdf":
            pdf_reader = PdfFileReader(BytesIO(content))
            text_content = ""
            for page_num in range(pdf_reader.getNumPages()):
                text_content += pdf_reader.getPage(page_num).extract_text()

            html_content = f"<html><body><pre>{text_content}</pre></body></html>"
        elif mime_type in ["application/msword",
                           "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
            doc = DocxDocument(BytesIO(content))
            text_content = "\n".join([para.text for para in doc.paragraphs])
            html_content = f"<html><body><pre>{text_content}</pre></body></html>"
        else:
            html_content = f"<html><body><pre>{content.decode('utf-8')}</pre></body></html>"

        return HTMLResponse(content=html_content)
    else:
        raise HTTPException(status_code=400, detail="File type not supported for viewing")


@router.get("/download/{file_id:path}",
         response_class=FileResponse,
         responses={
             404: {"description": "File Not Found"},
             400: {"description": "Bad Request"},
             500: {"description": "Internal Server Error"}})
async def download_file(file_id: str):
    """
    Download a file from the server. This endpoint returns the specified file for download.
    If the file does not exist, a 404 error is returned.
    """
    file_path = os.path.join(file_storage.store.root_path, file_id)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        path=file_path,
        filename=os.path.basename(file_path),
        headers={"Content-Disposition": f"attachment; filename={os.path.basename(file_path)}"})


if __name__ == "__main__":
    import uvicorn

    app = FastAPI()

    app.include_router(router, prefix="/data_stores", tags=["data_stores"])

    uvicorn.run(app, host="127.0.0.1", port=8100)
