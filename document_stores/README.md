
# API Documentation for Document Store Management System

## Overview

This API provides endpoints for managing documents and their metadata within MongoDB collections. It supports creating, retrieving, updating, deleting, and searching documents, as well as managing collection metadata. 

## Base URL

```
http://localhost:8102
```

## Endpoints

### 1. Create Document

#### `POST /documents/{collection_name}/`

Creates a new document in the specified collection.

**Path Parameters:**
- `collection_name` (str): The name of the collection. Example: "example_collection".

**Request Body:**
- `doc` (DocumentModel): The document to create.

**Response:**
- 200 OK: Returns the created document with an added unique ID in its metadata.
- 400 Bad Request: Invalid input.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X POST "http://localhost:8102/documents/example_collection/" -H "Content-Type: application/json" -d '{
  "page_content": "This is the content of the document.",
  "metadata": {"author": "John Doe", "category": "Research"},
  "type": "Document"
}'
```

**Example Response:**

```json
{
  "page_content": "This is the content of the document.",
  "metadata": {
    "author": "John Doe",
    "category": "Research",
    "doc_store_id": "abcd1234-efgh-5678-ijkl-9012mnop3456"
  },
  "type": "Document"
}
```

### 2. Retrieve Document

#### `GET /documents/{collection_name}/{doc_id}`

Retrieves a document by its ID from the specified collection.

**Path Parameters:**
- `collection_name` (str): The name of the collection. Example: "example_collection".
- `doc_id` (str): The ID of the document to retrieve. Example: "abcd1234-efgh-5678-ijkl-9012mnop3456".

**Response:**
- 200 OK: Returns the document with its content and metadata.
- 404 Not Found: Document not found.
- 400 Bad Request: Invalid input.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X GET "http://localhost:8102/documents/example_collection/abcd1234-efgh-5678-ijkl-9012mnop3456"
```

**Example Response:**

```json
{
  "page_content": "This is the content of the document.",
  "metadata": {
    "author": "John Doe",
    "category": "Research",
    "doc_store_id": "abcd1234-efgh-5678-ijkl-9012mnop3456"
  },
  "type": "Document"
}
```

### 3. Delete Document

#### `DELETE /documents/{collection_name}/{doc_id}`

Deletes a document by its ID from the specified collection.

**Path Parameters:**
- `collection_name` (str): The name of the collection. Example: "example_collection".
- `doc_id` (str): The ID of the document to delete. Example: "abcd1234-efgh-5678-ijkl-9012mnop3456".

**Response:**
- 200 OK: Document deleted successfully.
- 404 Not Found: Document not found.
- 400 Bad Request: Invalid input.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X DELETE "http://localhost:8102/documents/example_collection/abcd1234-efgh-5678-ijkl-9012mnop3456"
```

**Example Response:**

```json
{
  "detail": "Document deleted successfully"
}
```

### 4. Update Document

#### `PUT /documents/{collection_name}/{doc_id}`

Updates an existing document by its ID in the specified collection.

**Path Parameters:**
- `collection_name` (str): The name of the collection. Example: "example_collection".
- `doc_id` (str): The ID of the document to update. Example: "abcd1234-efgh-5678-ijkl-9012mnop3456".

**Request Body:**
- `doc` (DocumentModel): The updated document data.

**Response:**
- 200 OK: Returns the updated document data.
- 404 Not Found: Document not found.
- 400 Bad Request: Invalid input.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X PUT "http://localhost:8102/documents/example_collection/abcd1234-efgh-5678-ijkl-9012mnop3456" -H "Content-Type: application/json" -d '{
  "page_content": "This is the updated content of the document.",
  "metadata": {"author": "John Doe", "category": "Research"},
  "type": "Document"
}'
```

**Example Response:**

```json
{
  "page_content": "This is the updated content of the document.",
  "metadata": {
    "author": "John Doe",
    "category": "Research",
    "doc_store_id": "abcd1234-efgh-5678-ijkl-9012mnop3456"
  },
  "type": "Document"
}
```

### 5. List Documents

#### `GET /documents/{collection_name}/`

Lists documents in the specified collection with pagination.

**Path Parameters:**
- `collection_name` (str): The name of the collection. Example: "example_collection".

**Query Parameters:**
- `prefix` (optional, str): Prefix to filter documents. Example: "prefix_".
- `skip` (int): Number of documents to skip. Default is 0.
- `limit` (int): Maximum number of documents to return. Default is 10.

**Response:**
- 200 OK: Returns a list of documents with their content and metadata.
- 400 Bad Request: Invalid input.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X GET "http://localhost:8102/documents/example_collection/?skip=0&limit=10"
```

**Example Response:**

```json
[
  {
    "page_content": "This is the content of the document.",
    "metadata": {
      "author": "John Doe",
      "category": "Research",
      "doc_store_id": "abcd1234-efgh-5678-ijkl-9012mnop3456"
    },
    "type": "Document"
  }
]
```

### 6. Search Documents

#### `GET /search/{collection_name}/`

Searches for documents by query in the specified collection with pagination.

**Path Parameters:**
- `collection_name` (str): The name of the collection. Example: "example_collection".

**Query Parameters:**
- `query` (str): The search query. Example: "search_term".
- `skip` (int): Number of documents to skip. Default is 0.
- `limit` (int): Maximum number of documents to return. Default is 10.

**Response:**
- 200 OK: Returns a list of documents matching the search criteria.
- 400 Bad Request: Invalid input.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X GET "http://localhost:8102/search/example_collection/?query=search_term&skip=0&limit=10"
```

**Example Response:**

```json
[
  {
    "page_content": "This is the content of the document.",
    "metadata": {
      "author": "John Doe",
      "category": "Research",
      "doc_store_id": "abcd1234-efgh-5678-ijkl-9012mnop3456"
    },
    "type": "Document"
  }
]
```

### 7. Create Collection Metadata

#### `POST /collections/{collection_name}/metadata`

Creates or updates metadata for a specified collection.

**Path Parameters:**
- `collection_name` (str): The name of the collection. Example: "example_collection".

**Request Body:**
- `metadata` (CollectionMetadataModel): Metadata for the collection.

**Response:**
- 200 OK: Returns the created or updated collection metadata.
- 400 Bad Request: Invalid input.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X POST "http://localhost:8102/collections/example_collection/metadata" -H "Content-Type: application/json" -d '{
  "collection_name": "example_collection",
  "description": "This collection contains research documents.",
  "created_at": "2023-01-01T00:00:00Z",
  "custom_metadata": {"project": "AI Research"}
}'
```

**Example Response:**

```json
{
  "collection_name": "example_collection",
  "description": "This collection contains research documents.",
  "created_at": "2023-01-01T00:00:00Z",
  "custom_metadata": {"project": "AI Research"}
}
```

### 8. Update Collection Metadata

#### `PUT /collections/{collection_name}/metadata`

Updates metadata for a specified collection.

**Path Parameters:**
- `collection_name` (str): The name of the collection. Example: "example_collection".

**Request Body:**
- `metadata` (CollectionMetadataModel): Updated metadata for the collection.

**Response:**
- 200 OK: Returns the updated collection metadata.
- 404 Not Found: Collection metadata not found.
- 400 Bad Request

: Invalid input.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X PUT "http://localhost:8102/collections/example_collection/metadata" -H "Content-Type: application/json" -d '{
  "description": "This collection contains updated research documents.",
  "custom_metadata": {"project": "Updated AI Research"}
}'
```

**Example Response:**

```json
{
  "collection_name": "example_collection",
  "description": "This collection contains updated research documents.",
  "created_at": "2023-01-01T00:00:00Z",
  "custom_metadata": {"project": "Updated AI Research"}
}
```

### 9. List Collections Metadata

#### `GET /collections/metadata`

Lists all collections and their metadata.

**Response:**
- 200 OK: Returns a list of all collections with their metadata.
- 400 Bad Request: Invalid input.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X GET "http://localhost:8102/collections/metadata"
```

**Example Response:**

```json
[
  {
    "collection_name": "example_collection",
    "description": "This collection contains research documents.",
    "created_at": "2023-01-01T00:00:00Z",
    "custom_metadata": {"project": "AI Research"}
  }
]
```

## Models

### DocumentModel

Model representing a document.

**Attributes:**
- `page_content` (str): The content of the document.
- `metadata` (dict): Metadata associated with the document.
- `type` (str): The type of the document.

**Example:**

```json
{
  "page_content": "This is the content of the document.",
  "metadata": {
    "author": "John Doe",
    "category": "Research",
    "doc_store_id": "abcd1234-efgh-5678-ijkl-9012mnop3456"
  },
  "type": "Document"
}
```

### CollectionMetadataModel

Model representing metadata for a collection.

**Attributes:**
- `collection_name` (str): The name of the collection.
- `description` (optional, str): Description of the collection.
- `created_at` (optional, str): The creation date of the collection.
- `custom_metadata` (optional, dict): Custom metadata for the collection.

**Example:**

```json
{
  "collection_name": "example_collection",
  "description": "This collection contains research documents.",
  "created_at": "2023-01-01T00:00:00Z",
  "custom_metadata": {"project": "AI Research"}
}
```

## Usage

To use the API, you can make HTTP requests to the provided endpoints using tools like `curl`, Postman, or any HTTP client library in your preferred programming language.

### Usage Example with Python

Below is a Python example using the `requests` library to interact with the API:

#### 1. Create a Document

```python
import requests

url = "http://localhost:8102/documents/example_collection/"
data = {
    "page_content": "This is the content of the document.",
    "metadata": {"author": "John Doe", "category": "Research"},
    "type": "Document"
}

response = requests.post(url, json=data)
print(response.json())
```

#### 2. Retrieve a Document

```python
import requests

url = "http://localhost:8102/documents/example_collection/abcd1234-efgh-5678-ijkl-9012mnop3456"

response = requests.get(url)
print(response.json())
```

#### 3. Delete a Document

```python
import requests

url = "http://localhost:8102/documents/example_collection/abcd1234-efgh-5678-ijkl-9012mnop3456"

response = requests.delete(url)
print(response.json())
```

#### 4. Update a Document

```python
import requests

url = "http://localhost:8102/documents/example_collection/abcd1234-efgh-5678-ijkl-9012mnop3456"
data = {
    "page_content": "This is the updated content of the document.",
    "metadata": {"author": "John Doe", "category": "Research"},
    "type": "Document"
}

response = requests.put(url, json=data)
print(response.json())
```

#### 5. List Documents

```python
import requests

url = "http://localhost:8102/documents/example_collection/?skip=0&limit=10"

response = requests.get(url)
print(response.json())
```

#### 6. Search Documents

```python
import requests

url = "http://localhost:8102/search/example_collection/?query=search_term&skip=0&limit=10"

response = requests.get(url)
print(response.json())
```

#### 7. Create Collection Metadata

```python
import requests

url = "http://localhost:8102/collections/example_collection/metadata"
data = {
    "description": "This collection contains research documents.",
    "created_at": "2023-01-01T00:00:00Z",
    "custom_metadata": {"project": "AI Research"}
}

response = requests.post(url, json=data)
print(response.json())
```

#### 8. Update Collection Metadata

```python
import requests

url = "http://localhost:8102/collections/example_collection/metadata"
data = {
    "description": "This collection contains updated research documents.",
    "custom_metadata": {"project": "Updated AI Research"}
}

response = requests.put(url, json=data)
print(response.json())
```

#### 9. List Collections Metadata

```python
import requests

url = "http://localhost:8102/collections/metadata"

response = requests.get(url)
print(response.json())
```
