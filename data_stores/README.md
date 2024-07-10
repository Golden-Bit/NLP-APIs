
# API Documentation for File Management System

## Overview

This API provides a comprehensive system for managing files and directories. It includes functionalities for uploading, downloading, updating, deleting files, managing metadata, and viewing files in different formats. The API is built using FastAPI and integrates with a file storage utility for handling file operations.

## Base URL

```
http://localhost:8100
```

## Endpoints

### 1. Create Directory

#### `POST /create_directory`

Creates a directory on the server and attaches custom metadata if provided.

**Request Parameters:**
- `directory` (form): The path to the directory to create.
- `description` (form, optional): Custom description for the directory.
- `extra_metadata` (form, optional): Extra metadata for the directory in JSON format.

**Response:**
- 200 OK: Returns the metadata of the created directory.
- 400 Bad Request: Invalid input.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X POST "http://localhost:8100/create_directory" -F "directory=documents/research" -F "description=Research documents" -F 'extra_metadata={"department":"Research","category":"AI"}'
```

**Example Response:**

```json
{
  "path": "documents/research",
  "custom_metadata": {
    "description": "Research documents",
    "department": "Research",
    "category": "AI"
  }
}
```

### 2. Delete Directory

#### `DELETE /delete_directory/{directory_id:path}`

Deletes a directory and its metadata.

**Path Parameters:**
- `directory_id` (path): The path to the directory to delete.

**Response:**
- 200 OK: Directory deleted successfully.
- 404 Not Found: Directory not found.
- 400 Bad Request: Invalid input.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X DELETE "http://localhost:8100/delete_directory/documents/research"
```

**Example Response:**

```json
{
  "detail": "Directory deleted successfully"
}
```

### 3. Upload File

#### `POST /upload`

Uploads a file to the server and attaches custom metadata if provided.

**Request Parameters:**
- `file` (form): The file to upload.
- `subdir` (form, optional): The subdirectory to save the file in.
- `file_description` (form, optional): Custom description for the file.
- `extra_metadata` (form, optional): Extra metadata for the file in JSON format.

**Response:**
- 200 OK: Returns the metadata of the uploaded file.
- 400 Bad Request: Invalid input.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X POST "http://localhost:8100/upload" -F "file=@example.txt" -F "subdir=documents" -F 'extra_metadata={"author":"John Doe","project":"AI Research"}'
```

**Example Response:**

```json
{
  "name": "example.txt",
  "size": 1024,
  "modified_time": "2023-06-26T12:00:00Z",
  "created_time": "2023-06-26T10:00:00Z",
  "path": "documents/example.txt",
  "mime_type": "text/plain",
  "custom_metadata": {
    "author": "John Doe",
    "project": "AI Research"
  }
}
```

### 4. Upload Multiple Files

#### `POST /upload/multiple`

Uploads multiple files to the server and attaches custom metadata if provided.

**Request Parameters:**
- `files` (form): The list of files to upload.
- `subdir` (form, optional): The subdirectory to save the files in.
- `file_description` (form, optional): Custom description for the files.
- `extra_metadata` (form, optional): Extra metadata for the files in JSON format.

**Response:**
- 200 OK: Returns the paths of the uploaded files.
- 400 Bad Request: Invalid input.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X POST "http://localhost:8100/upload/multiple" -F "files=@example1.txt" -F "files=@example2.txt" -F "subdir=documents" -F 'extra_metadata={"author":"John Doe","project":"AI Research"}'
```

**Example Response:**

```json
{
  "file_ids": [
    "documents/example1.txt",
    "documents/example2.txt"
  ]
}
```

### 5. Update File

#### `PUT /update/{file_id:path}`

Updates an existing file and its custom metadata.

**Path Parameters:**
- `file_id` (path): The ID of the file to update.

**Request Parameters:**
- `file` (form): The new file content.
- `file_description` (form, optional): Custom description for the file.
- `extra_metadata` (form, optional): Extra metadata for the file in JSON format.

**Response:**
- 200 OK: Returns the metadata of the updated file.
- 404 Not Found: File not found.
- 400 Bad Request: Invalid input.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X PUT "http://localhost:8100/update/documents/example.txt" -F "file=@new_example.txt" -F 'extra_metadata={"author":"Jane Doe","project":"New Research"}'
```

**Example Response:**

```json
{
  "name": "example.txt",
  "size": 2048,
  "modified_time": "2023-06-27T12:00:00Z",
  "created_time": "2023-06-26T10:00:00Z",
  "path": "documents/example.txt",
  "mime_type": "text/plain",
  "custom_metadata": {
    "author": "Jane Doe",
    "project": "New Research"
  }
}
```

### 6. Save File Metadata

#### `POST /file/metadata`

Saves custom metadata for a specified file.

**Request Parameters:**
- `file_id` (form): The path to the file.
- `file_description` (form, optional): Custom description for the file.
- `extra_metadata` (form, optional): Extra metadata for the file in JSON format.

**Response:**
- 200 OK: Returns the metadata of the file.
- 404 Not Found: File not found.
- 400 Bad Request: Invalid input.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X POST "http://localhost:8100/file/metadata" -F "file_id=documents/example.txt" -F 'extra_metadata={"author":"John Doe","project":"AI Research"}'
```

**Example Response:**

```json
{
  "name": "example.txt",
  "size": 1024,
  "modified_time": "2023-06-26T12:00:00Z",
  "created_time": "2023-06-26T10:00:00Z",
  "path": "documents/example.txt",
  "mime_type": "text/plain",
  "custom_metadata": {
    "author": "John Doe",
    "project": "AI Research"
  }
}
```

### 7. Delete File

#### `DELETE /delete/{file_id:path}`

Deletes a specified file and its metadata.

**Path Parameters:**
- `file_id` (path): The ID of the file to delete.

**Response:**
- 200 OK: File deleted successfully.
- 404 Not Found: File not found.
- 400 Bad Request: Invalid input.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X DELETE "http://localhost:8100/delete/documents/example.txt"
```

**Example Response:**

```json
{
  "detail": "File deleted successfully"
}
```

### 8. Retrieve File

#### `GET /file/{file_id:path}`

Retrieves the content of a specified file.

**Path Parameters:**
- `file_id` (path): The ID of the file to retrieve.

**Response:**
- 200 OK: Returns the content of the file.
- 404 Not Found: File not found.
- 400 Bad Request: Invalid input.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X GET "http://localhost:8100/file/documents/example.txt"
```

**Example Response:**

Returns the file content as a binary stream.

### 9. List Files

#### `GET /files`

Lists all files on the server or in a specific subdirectory.

**Query Parameters:**
- `subdir` (query, optional): The subdirectory to list files from.

**Response:**
- 200 OK: Returns a list of file metadata.
- 400 Bad Request: Invalid input.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X GET "http://localhost:8100/files?subdir=documents"
```

**Example Response:**

```json
[
  {
    "name": "example.txt",
    "size": 1024,
    "modified_time": "2023-06-26T12:00:00Z",
    "created_time": "2023-06-26T10:00:00Z",
    "path": "documents/example.txt",
    "mime_type": "text/plain

",
    "custom_metadata": {
      "author": "John Doe",
      "project": "AI Research"
    }
  }
]
```

### 10. Retrieve File Metadata

#### `GET /metadata/{file_id:path}`

Retrieves the metadata of a specified file.

**Path Parameters:**
- `file_id` (path): The ID of the file to retrieve metadata for.

**Response:**
- 200 OK: Returns the file metadata.
- 404 Not Found: File not found.
- 400 Bad Request: Invalid input.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X GET "http://localhost:8100/metadata/documents/example.txt"
```

**Example Response:**

```json
{
  "name": "example.txt",
  "size": 1024,
  "modified_time": "2023-06-26T12:00:00Z",
  "created_time": "2023-06-26T10:00:00Z",
  "path": "documents/example.txt",
  "mime_type": "text/plain",
  "custom_metadata": {
    "author": "John Doe",
    "project": "AI Research"
  }
}
```

### 11. Retrieve File Versions

#### `GET /versions/{file_id:path}`

Retrieves all versions of a specified file. (Note: Versioning is not yet implemented.)

**Path Parameters:**
- `file_id` (path): The ID of the file to retrieve versions for.

**Response:**
- 200 OK: Returns a placeholder message indicating versioning is not implemented.
- 404 Not Found: File not found.
- 400 Bad Request: Invalid input.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X GET "http://localhost:8100/versions/documents/example.txt"
```

**Example Response:**

```json
{
  "detail": "Versioning not implemented yet"
}
```

### 12. List Directories

#### `GET /directories`

Lists all directories in the storage.

**Response:**
- 200 OK: Returns a list of directory metadata.
- 400 Bad Request: Invalid input.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X GET "http://localhost:8100/directories"
```

**Example Response:**

```json
[
  {
    "path": "documents/research",
    "custom_metadata": {
      "department": "Research",
      "category": "AI"
    }
  }
]
```

### 13. Save Directory Metadata

#### `POST /directory/metadata`

Saves custom metadata for a specified directory.

**Request Parameters:**
- `directory` (form): The directory path.
- `description` (form, optional): Custom description for the directory.
- `extra_metadata` (form, optional): Extra metadata for the directory in JSON format.

**Response:**
- 200 OK: Returns the metadata of the directory.
- 400 Bad Request: Invalid input.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X POST "http://localhost:8100/directory/metadata" -F "directory=documents/research" -F 'extra_metadata={"department":"Research","category":"AI"}'
```

**Example Response:**

```json
{
  "path": "documents/research",
  "custom_metadata": {
    "description": "Research documents",
    "department": "Research",
    "category": "AI"
  }
}
```

### 14. Search Files

#### `GET /search/files`

Searches for files based on a query and optionally within a specific subdirectory.

**Query Parameters:**
- `query` (query): The search query.
- `subdir` (query, optional): The subdirectory to search within.

**Response:**
- 200 OK: Returns a list of file metadata matching the search query.
- 400 Bad Request: Invalid input.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X GET "http://localhost:8100/search/files?query=example&subdir=documents"
```

**Example Response:**

```json
[
  {
    "name": "example.txt",
    "size": 1024,
    "modified_time": "2023-06-26T12:00:00Z",
    "created_time": "2023-06-26T10:00:00Z",
    "path": "documents/example.txt",
    "mime_type": "text/plain",
    "custom_metadata": {
      "author": "John Doe",
      "project": "AI Research"
    }
  }
]
```

### 15. Filter Files

#### `GET /filter/files`

Filters files based on MIME type and size.

**Query Parameters:**
- `mime_type` (query, optional): The MIME type to filter by.
- `min_size` (query, optional): The minimum file size in bytes.
- `max_size` (query, optional): The maximum file size in bytes.

**Response:**
- 200 OK: Returns a list of file metadata matching the filter criteria.
- 400 Bad Request: Invalid input.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X GET "http://localhost:8100/filter/files?mime_type=text/plain&min_size=500&max_size=2000"
```

**Example Response:**

```json
[
  {
    "name": "example.txt",
    "size": 1024,
    "modified_time": "2023-06-26T12:00:00Z",
    "created_time": "2023-06-26T10:00:00Z",
    "path": "documents/example.txt",
    "mime_type": "text/plain",
    "custom_metadata": {
      "author": "John Doe",
      "project": "AI Research"
    }
  }
]
```

### 16. View File

#### `GET /view/{file_id:path}`

View a file in its readable representation (e.g., text, PDF, DOCX).

**Path Parameters:**
- `file_id` (path): The ID of the file to view.

**Response:**
- 200 OK: Returns the content of the file in a readable format (HTML).
- 404 Not Found: File not found.
- 400 Bad Request: Invalid input.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X GET "http://localhost:8100/view/documents/example.txt"
```

**Example Response:**

```html
<html>
  <body>
    <pre>This is the content of the example.txt file.</pre>
  </body>
</html>
```

### 17. Download File

#### `GET /download/{file_id:path}`

Downloads a specified file.

**Path Parameters:**
- `file_id` (path): The ID of the file to download.

**Response:**
- 200 OK: Returns the file for download.
- 404 Not Found: File not found.
- 400 Bad Request: Invalid input.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X GET "http://localhost:8100/download/documents/example.txt"
```

**Example Response:**

Returns the file content as a binary stream for download.

## Models

### FileMetadata

Model representing metadata for a file.

**Attributes:**
- `name` (str): The name of the file.
- `size` (int): The size of the file in bytes.
- `modified_time` (str): The last modified time of the file in ISO 8601 format.
- `created_time` (str): The creation time of the file in ISO 8601 format.
- `path` (str): The relative path to the file in the storage.
- `mime_type` (Optional[str]): The MIME type of the file, if available.
- `custom_metadata` (Optional[Dict[str, Any]]): Any custom metadata associated with the file.

**Example:**

```json
{
  "name": "example.txt",
  "size": 1024,
  "modified_time": "2023-06-26T12:00:00Z",
  "created_time": "2023-06-26T10:00:00Z",
  "path": "documents/example.txt",
  "mime_type": "text/plain",
  "custom_metadata": {
    "author": "John Doe",
    "project": "AI Research"
  }
}
```

### DirectoryMetadata

Model representing metadata for a directory.

**Attributes:**
- `path` (str): The path to the directory in the storage.
- `custom_metadata` (Optional[Dict[str, Any]]): Any custom metadata associated with the directory.

**Example:**

```json
{
  "path": "documents/research",
  "custom_metadata": {
    "description": "Research documents",
    "department": "Research",
    "category": "AI"
  }
}
```

## Error Handling

The API provides detailed error responses for different scenarios, including:

- `400 Bad Request`: For invalid input.
- `404 Not Found`: When the requested resource is not found.
- `500 Internal Server Error`: For server errors.

Each error response includes a description and additional details when necessary.

## Usage

To use the API, you can make HTTP requests to the provided endpoints using tools like `curl`, Postman, or any HTTP client library in your preferred programming language.

### Usage Example

 with Python

Below is a Python example using the `requests` library to interact with the API:

#### 1. Create a Directory

```python
import requests

url = "http://localhost:8100/create_directory"
data = {
    "directory": "documents/research",
    "description": "Research documents",
    "extra_metadata": '{"department": "Research", "category": "AI"}'
}

response = requests.post(url, data=data)
print(response.json())
```

#### 2. Upload a File

```python
import requests

url = "http://localhost:8100/upload"
files = {'file': open('example.txt', 'rb')}
data = {
    "subdir": "documents",
    "file_description": "Example text file",
    "extra_metadata": '{"author": "John Doe", "project": "AI Research"}'
}

response = requests.post(url, files=files, data=data)
print(response.json())
```

#### 3. Retrieve File Metadata

```python
import requests

url = "http://localhost:8100/metadata/documents/example.txt"

response = requests.get(url)
print(response.json())
```

#### 4. Download a File

```python
import requests

url = "http://localhost:8100/download/documents/example.txt"

response = requests.get(url)
with open('downloaded_example.txt', 'wb') as f:
    f.write(response.content)
```

#### 5. Update a File

```python
import requests

url = "http://localhost:8100/update/documents/example.txt"
files = {'file': open('new_example.txt', 'rb')}
data = {
    "file_description": "Updated example text file",
    "extra_metadata": '{"author": "Jane Doe", "project": "New Research"}'
}

response = requests.put(url, files=files, data=data)
print(response.json())
```

#### 6. List Files

```python
import requests

url = "http://localhost:8100/files?subdir=documents"

response = requests.get(url)
print(response.json())
```
#### 7. Delete a File

```python
import requests

url = "http://localhost:8100/delete/documents/example.txt"

response = requests.delete(url)
print(response.json())
```

#### 8. Retrieve a File

```python
import requests

url = "http://localhost:8100/file/documents/example.txt"

response = requests.get(url)
with open('retrieved_example.txt', 'wb') as f:
    f.write(response.content)
```

#### 9. Save File Metadata

```python
import requests

url = "http://localhost:8100/file/metadata"
data = {
    "file_id": "documents/example.txt",
    "file_description": "Example text file",
    "extra_metadata": '{"author": "John Doe", "project": "AI Research"}'
}

response = requests.post(url, data=data)
print(response.json())
```

#### 10. Upload Multiple Files

```python
import requests

url = "http://localhost:8100/upload/multiple"
files = [
    ('files', open('example1.txt', 'rb')),
    ('files', open('example2.txt', 'rb'))
]
data = {
    "subdir": "documents",
    "file_description": "Batch upload",
    "extra_metadata": '{"author": "John Doe", "project": "AI Research"}'
}

response = requests.post(url, files=files, data=data)
print(response.json())
```

#### 11. Search for Files

```python
import requests

url = "http://localhost:8100/search/files"
params = {
    "query": "example",
    "subdir": "documents"
}

response = requests.get(url, params=params)
print(response.json())
```

#### 12. Filter Files

```python
import requests

url = "http://localhost:8100/filter/files"
params = {
    "mime_type": "text/plain",
    "min_size": 500,
    "max_size": 2000
}

response = requests.get(url, params=params)
print(response.json())
```

#### 13. View a File

```python
import requests

url = "http://localhost:8100/view/documents/example.txt"

response = requests.get(url)
print(response.text)
```

#### 14. List Directories

```python
import requests

url = "http://localhost:8100/directories"

response = requests.get(url)
print(response.json())
```

#### 15. Save Directory Metadata

```python
import requests

url = "http://localhost:8100/directory/metadata"
data = {
    "directory": "documents/research",
    "description": "Research documents",
    "extra_metadata": '{"department": "Research", "category": "AI"}'
}

response = requests.post(url, data=data)
print(response.json())
```

#### 16. Retrieve File Versions

```python
import requests

url = "http://localhost:8100/versions/documents/example.txt"

response = requests.get(url)
print(response.json())
```

#### 17. List Files

```python
import requests

url = "http://localhost:8100/files"

response = requests.get(url)
print(response.json())
```
