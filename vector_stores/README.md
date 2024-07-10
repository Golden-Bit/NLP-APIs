
# API Documentation for Vector Store Management System

## Overview

This API provides endpoints for configuring, managing, and searching vector stores. It supports creating, retrieving, updating, and deleting vector store configurations, as well as adding and searching documents within these vector stores. The vector stores and document embeddings are managed in MongoDB.

## Base URL

```
http://localhost:8104
```

## Endpoints

### 1. Configure Vector Store

#### `POST /vector_store/configure`

Creates a new vector store configuration with specified parameters.

**Request Body:**
- `config_id` (optional, str): The unique ID for the vector store configuration. If not provided, a new ID will be generated.
- `store_id` (optional, str): The unique ID for the vector store instance. If not provided, a new ID will be generated.
- `vector_store_class` (str): The class of the vector store.
- `params` (dict): Configuration parameters for the vector store.
- `embeddings_model_class` (optional, str): The class of the embeddings model.
- `embeddings_params` (optional, dict): Configuration parameters for the embeddings model.
- `description` (optional, str): A description of the vector store configuration.
- `custom_metadata` (optional, dict): Custom metadata for the configuration.

**Response:**
- 200 OK: Returns the created vector store configuration.
- 400 Bad Request: Invalid input or configuration ID already exists.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X POST "http://localhost:8104/vector_store/configure" -H "Content-Type: application/json" -d '{
  "vector_store_class": "Chroma",
  "params": {"param1": "value1", "param2": "value2"},
  "embeddings_model_class": "OpenAIEmbeddings",
  "embeddings_params": {"api_key": "your_openai_api_key"},
  "description": "This is a Chroma vector store configuration for project X.",
  "custom_metadata": {"project": "Project X", "owner": "John Doe"}
}'
```

**Example Response:**

```json
{
  "config_id": "abcd1234-efgh-5678-ijkl-9012mnop3456",
  "store_id": "abcd1234-efgh-5678-ijkl-9012mnop3456",
  "vector_store_class": "Chroma",
  "params": {"param1": "value1", "param2": "value2"},
  "embeddings_model_class": "OpenAIEmbeddings",
  "embeddings_params": {"api_key": "your_openai_api_key"},
  "description": "This is a Chroma vector store configuration for project X.",
  "custom_metadata": {"project": "Project X", "owner": "John Doe"}
}
```

### 2. Delete Vector Store Configuration

#### `DELETE /vector_store/configure/{config_id}`

Deletes a specified vector store configuration from MongoDB.

**Path Parameters:**
- `config_id` (str): The unique ID of the vector store configuration to delete.

**Response:**
- 200 OK: Configuration deleted successfully.
- 404 Not Found: Configuration not found.
- 400 Bad Request: Invalid input.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X DELETE "http://localhost:8104/vector_store/configure/abcd1234-efgh-5678-ijkl-9012mnop3456"
```

**Example Response:**

```json
{
  "detail": "Configuration deleted successfully"
}
```

### 3. Update Vector Store Configuration

#### `PUT /vector_store/configure/{config_id}`

Updates the configuration of an existing vector store in MongoDB.

**Path Parameters:**
- `config_id` (str): The unique ID of the vector store configuration to update.

**Request Body:**
- `store_id` (optional, str): The unique ID for the vector store instance.
- `vector_store_class` (str): The class of the vector store.
- `params` (dict): Configuration parameters for the vector store.
- `embeddings_model_class` (optional, str): The class of the embeddings model.
- `embeddings_params` (optional, dict): Configuration parameters for the embeddings model.
- `description` (optional, str): A description of the vector store configuration.
- `custom_metadata` (optional, dict): Custom metadata for the configuration.

**Response:**
- 200 OK: Returns the updated vector store configuration.
- 404 Not Found: Configuration not found.
- 400 Bad Request: Invalid input.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X PUT "http://localhost:8104/vector_store/configure/abcd1234-efgh-5678-ijkl-9012mnop3456" -H "Content-Type: application/json" -d '{
  "vector_store_class": "Chroma",
  "params": {"param1": "new_value1", "param2": "new_value2"},
  "embeddings_model_class": "OpenAIEmbeddings",
  "embeddings_params": {"api_key": "new_api_key"},
  "description": "Updated description for project X.",
  "custom_metadata": {"project": "Updated Project X", "owner": "Jane Doe"}
}'
```

**Example Response:**

```json
{
  "config_id": "abcd1234-efgh-5678-ijkl-9012mnop3456",
  "store_id": "abcd1234-efgh-5678-ijkl-9012mnop3456",
  "vector_store_class": "Chroma",
  "params": {"param1": "new_value1", "param2": "new_value2"},
  "embeddings_model_class": "OpenAIEmbeddings",
  "embeddings_params": {"api_key": "new_api_key"},
  "description": "Updated description for project X.",
  "custom_metadata": {"project": "Updated Project X", "owner": "Jane Doe"}
}
```

### 4. List Vector Store Configurations

#### `GET /vector_store/configurations`

Retrieves and returns a list of all vector store configurations stored in MongoDB.

**Response:**
- 200 OK: Returns a list of all vector store configurations.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X GET "http://localhost:8104/vector_store/configurations"
```

**Example Response:**

```json
[
  {
    "config_id": "abcd1234-efgh-5678-ijkl-9012mnop3456",
    "store_id": "abcd1234-efgh-5678-ijkl-9012mnop3456",
    "vector_store_class": "Chroma",
    "params": {"param1": "value1", "param2": "value2"},
    "embeddings_model_class": "OpenAIEmbeddings",
    "embeddings_params": {"api_key": "your_openai_api_key"},
    "description": "This is a Chroma vector store configuration for project X.",
    "custom_metadata": {"project": "Project X", "owner": "John Doe"}
  }
]
```

### 5. Load Vector Store

#### `POST /vector_store/load/{config_id}`

Loads a vector store into memory using the specified configuration ID.

**Path Parameters:**
- `config_id` (str): The unique ID of the vector store configuration to load.

**Response:**
- 200 OK: Returns a confirmation message upon successful loading.
- 404 Not Found: Configuration not found.
- 400 Bad Request: Store ID already exists in memory.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X POST "http://localhost:8104/vector_store/load/abcd1234-efgh-5678-ijkl-9012mnop3456"
```

**Example Response:**

```json
{
  "detail": "Vector store abcd1234-efgh-5678-ijkl-9012mnop3456 loaded successfully"
}
```

### 6. Offload Vector Store

#### `POST /vector_store/offload/{store_id}`

Offloads a vector store from memory using the specified store ID.

**Path Parameters:**
- `store_id` (str): The unique ID of the vector store to offload from memory.

**Response:**
- 200 OK: Returns a confirmation message upon successful offloading.
- 404 Not Found: Vector store not found in memory.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X POST "http://localhost:8104/vector_store/offload/abcd1234-efgh-5678-ijkl-9012mnop3456"
```

**Example Response:**

```json
{
  "detail": "Vector store abcd1234-efgh-5678-ijkl-9012mnop3456 offloaded successfully"
}
```

### 7. Get Loaded Store IDs

#### `GET /vector_store/loaded_store_ids`

Returns a list of IDs for vector stores currently loaded in memory.

**Response:**
- 200 OK: Returns a list of loaded store IDs.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X GET "http://localhost:8104/vector_store/loaded_store_ids"
```

**Example Response:**

```json
[
  "abcd1234-efgh-5678-ijkl-9012mnop3456"
]
```

### 8. Add

 Documents to Vector Store

#### `POST /vector_store/documents/{store_id}`

Adds documents to a vector store specified by the store ID.

**Path Parameters:**
- `store_id` (str): The unique ID of the vector store instance.

**Request Body:**
- `documents` (list): The documents to add to the vector store.

**Response:**
- 200 OK: Returns a confirmation message upon successful addition.
- 404 Not Found: Vector store not found in memory.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X POST "http://localhost:8104/vector_store/documents/abcd1234-efgh-5678-ijkl-9012mnop3456" -H "Content-Type: application/json" -d '{
  "documents": [
    {"page_content": "Document content", "metadata": {"author": "John Doe"}}
  ]
}'
```

**Example Response:**

```json
{
  "detail": "Documents added to vector store abcd1234-efgh-5678-ijkl-9012mnop3456 successfully"
}
```

### 9. Add Texts to Vector Store

#### `POST /vector_store/texts/{store_id}`

Adds texts and optional metadata to a vector store specified by the store ID.

**Path Parameters:**
- `store_id` (str): The unique ID of the vector store instance.

**Request Body:**
- `texts` (list): The texts to add to the vector store.
- `metadatas` (optional, list): Optional metadata associated with the texts.

**Response:**
- 200 OK: Returns a confirmation message upon successful addition.
- 404 Not Found: Vector store not found in memory.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X POST "http://localhost:8104/vector_store/texts/abcd1234-efgh-5678-ijkl-9012mnop3456" -H "Content-Type: application/json" -d '{
  "texts": ["Text content 1", "Text content 2"],
  "metadatas": [{"author": "John Doe"}, {"author": "Jane Doe"}]
}'
```

**Example Response:**

```json
{
  "detail": "Texts added to vector store abcd1234-efgh-5678-ijkl-9012mnop3456 successfully"
}
```

### 10. Remove Documents from Vector Store

#### `DELETE /vector_store/documents/{store_id}`

Removes documents from a vector store specified by the store ID.

**Path Parameters:**
- `store_id` (str): The unique ID of the vector store instance.

**Request Body:**
- `ids` (list): The IDs of the documents to remove from the vector store.

**Response:**
- 200 OK: Returns a confirmation message upon successful removal.
- 404 Not Found: Vector store not found in memory.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X DELETE "http://localhost:8104/vector_store/documents/abcd1234-efgh-5678-ijkl-9012mnop3456" -H "Content-Type: application/json" -d '{
  "ids": ["id1", "id2"]
}'
```

**Example Response:**

```json
{
  "detail": "Documents removed from vector store abcd1234-efgh-5678-ijkl-9012mnop3456 successfully"
}
```

### 11. Execute Vector Store Method

#### `POST /vector_store/method/{store_id}`

Executes a specific method with provided kwargs on the vector store specified by the store ID.

**Path Parameters:**
- `store_id` (str): The unique ID of the vector store instance.

**Request Body:**
- `method_name` (str): The name of the method to call.
- `kwargs` (dict): Keyword arguments for the method.

**Response:**
- 200 OK: Returns the result of the method execution.
- 404 Not Found: Vector store not found in memory.
- 400 Bad Request: Method not found in vector store class.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X POST "http://localhost:8104/vector_store/method/abcd1234-efgh-5678-ijkl-9012mnop3456" -H "Content-Type: application/json" -d '{
  "method_name": "persist",
  "kwargs": {"param1": "value1", "param2": "value2"}
}'
```

**Example Response:**

```json
{
  "detail": "Method persist executed successfully on vector store abcd1234-efgh-5678-ijkl-9012mnop3456",
  "result": "Persisted successfully"
}
```

### 12. Add Documents from Document Store

#### `POST /vector_store/add_documents_from_store/{store_id}`

Retrieves documents from a specified document collection in the document store and adds them to the vector store specified by the store ID.

**Path Parameters:**
- `store_id` (str): The unique ID of the vector store instance.

**Query Parameters:**
- `document_collection` (str): The name of the document collection in the document store.

**Response:**
- 200 OK: Returns a confirmation message upon successful addition.
- 404 Not Found: Vector store not found in memory.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X POST "http://localhost:8104/vector_store/add_documents_from_store/abcd1234-efgh-5678-ijkl-9012mnop3456?document_collection=my_document_collection"
```

**Example Response:**

```json
{
  "detail": "Documents from collection my_document_collection added to vector store abcd1234-efgh-5678-ijkl-9012mnop3456 successfully"
}
```

### 13. Update Document in Vector Store

#### `PUT /vector_store/documents/{store_id}/{document_id}`

Updates a document in a vector store specified by the store ID and document ID.

**Path Parameters:**
- `store_id` (str): The unique ID of the vector store instance.
- `document_id` (str): The unique ID of the document to update.

**Request Body:**
- `document` (DocumentModel): The updated document data.

**Response:**
- 200 OK: Returns a confirmation message upon successful update.
- 404 Not Found: Vector store not found in memory.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X PUT "http://localhost:8104/vector_store/documents/abcd1234-efgh-5678-ijkl-9012mnop3456/doc1234" -H "Content-Type: application/json" -d '{
  "document": {"page_content": "Updated document content", "metadata": {"author": "Jane Doe"}}
}'
```

**Example Response:**

```json
{
  "detail": "Document doc1234 updated in vector store abcd1234-efgh-5678-ijkl-9012mnop3456 successfully"
}
```

### 14. Search Vector Store

#### `POST /vector_store/search/{store_id}`

Searches a vector store using the specified search type and query.

**Path Parameters:**
- `store_id` (str): The unique ID of the vector store instance.

**Request Body:**
- `query` (str): The search query.
- `search_type` (str): The type of search to perform. Supported types: 'similarity', 'mmr', 'similarity_score_threshold'.
- `search_kwargs` (dict): Additional keyword arguments for the search method.

**Response:**
- 200 OK: Returns a list of documents that match the search criteria.
- 404 Not Found: Vector store not found in memory.
- 400 Bad Request: Unsupported search type.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X POST "http://localhost:8104/vector_store/search/abcd1234-efgh-5678-ijkl-9012mnop3456" -H "Content-Type: application/json" -d '{
  "query": "example query",
  "search_type": "similarity",
  "search_kwargs": {"k": 4}
}'
```

**Example Response:**

```json
[
  {"page_content": "Document content 1", "metadata": {"author": "John Doe"}},
  {"page_content": "Document content 2", "metadata": {"author": "Jane Doe"}}
]
```

### 15. Filter Vector Store

#### `POST /vector_store/filter/{store_id}`

Retrieves documents from a vector store that match the specified filter criteria.

**Path Parameters:**
- `store_id` (str): The unique ID of the vector store instance.

**Request Body:**
- `filter` (dict): The filter criteria for retrieving documents.
- `skip` (optional, int): The number of documents to skip.
- `limit` (optional, int): The maximum number of documents to return.

**Response:**
- 200 OK: Returns a list of documents that match the filter criteria.
- 404 Not Found: Vector store not found in memory.
- 400 Bad Request: Unsupported filter method.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X POST "http://localhost:8104/vector_store/filter/abcd1234-efgh-5678

-ijkl-9012mnop3456" -H "Content-Type: application/json" -d '{
  "filter": {"author": "John Doe"},
  "skip": 0,
  "limit": 10
}'
```

**Example Response:**

```json
[
  {"page_content": "Document content 1", "metadata": {"author": "John Doe"}},
  {"page_content": "Document content 2", "metadata": {"author": "John Doe"}}
]
```

## Models

### VectorStoreConfigModel

Model representing the configuration for a vector store.

**Attributes:**
- `config_id` (optional, str): The unique ID for the vector store configuration.
- `store_id` (optional, str): The unique ID for the vector store instance.
- `vector_store_class` (str): The class of the vector store.
- `params` (dict): Configuration parameters for the vector store.
- `embeddings_model_class` (optional, str): The class of the embeddings model.
- `embeddings_params` (optional, dict): Configuration parameters for the embeddings model.
- `description` (optional, str): A description of the vector store configuration.
- `custom_metadata` (optional, dict): Custom metadata for the configuration.

**Example:**

```json
{
  "config_id": "abcd1234-efgh-5678-ijkl-9012mnop3456",
  "store_id": "abcd1234-efgh-5678-ijkl-9012mnop3456",
  "vector_store_class": "Chroma",
  "params": {"param1": "value1", "param2": "value2"},
  "embeddings_model_class": "OpenAIEmbeddings",
  "embeddings_params": {"api_key": "your_openai_api_key"},
  "description": "This is a Chroma vector store configuration for project X.",
  "custom_metadata": {"project": "Project X", "owner": "John Doe"}
}
```

### DocumentModel

Model representing a document.

**Attributes:**
- `page_content` (str): The content of the document.
- `metadata` (dict): Metadata associated with the document.

**Example:**

```json
{
  "page_content": "This is the content of the document.",
  "metadata": {"author": "John Doe"}
}
```

### MethodRequestModel

Model representing a request to execute a specific method on a vector store.

**Attributes:**
- `method_name` (str): The name of the method to call.
- `kwargs` (dict): Keyword arguments for the method.

**Example:**

```json
{
  "method_name": "persist",
  "kwargs": {"param1": "value1", "param2": "value2"}
}
```

### SearchRequestModel

Model representing a search request in a vector store.

**Attributes:**
- `query` (str): The search query.
- `search_type` (str): The type of search to perform. Supported types: 'similarity', 'mmr', 'similarity_score_threshold'.
- `search_kwargs` (dict): Additional keyword arguments for the search method.

**Example:**

```json
{
  "query": "example query",
  "search_type": "similarity",
  "search_kwargs": {"k": 4}
}
```

### FilterRequestModel

Model representing a filter request for retrieving documents from a vector store.

**Attributes:**
- `filter` (dict): The filter criteria for retrieving documents.
- `skip` (optional, int): The number of documents to skip.
- `limit` (optional, int): The maximum number of documents to return.

**Example:**

```json
{
  "filter": {"author": "John Doe"},
  "skip": 0,
  "limit": 10
}
```

## Usage

To use the API, you can make HTTP requests to the provided endpoints using tools like `curl`, Postman, or any HTTP client library in your preferred programming language.

### Usage Example with Python

Below is a Python example using the `requests` library to interact with the API:

#### 1. Configure Vector Store

```python
import requests

url = "http://localhost:8104/vector_store/configure"
data = {
    "vector_store_class": "Chroma",
    "params": {"param1": "value1", "param2": "value2"},
    "embeddings_model_class": "OpenAIEmbeddings",
    "embeddings_params": {"api_key": "your_openai_api_key"},
    "description": "This is a Chroma vector store configuration for project X.",
    "custom_metadata": {"project": "Project X", "owner": "John Doe"}
}

response = requests.post(url, json=data)
print(response.json())
```

#### 2. Delete Vector Store Configuration

```python
import requests

url = "http://localhost:8104/vector_store/configure/abcd1234-efgh-5678-ijkl-9012mnop3456"

response = requests.delete(url)
print(response.json())
```

#### 3. Update Vector Store Configuration

```python
import requests

url = "http://localhost:8104/vector_store/configure/abcd1234-efgh-5678-ijkl-9012mnop3456"
data = {
    "vector_store_class": "Chroma",
    "params": {"param1": "new_value1", "param2": "new_value2"},
    "embeddings_model_class": "OpenAIEmbeddings",
    "embeddings_params": {"api_key": "new_api_key"},
    "description": "Updated description for project X.",
    "custom_metadata": {"project": "Updated Project X", "owner": "Jane Doe"}
}

response = requests.put(url, json=data)
print(response.json())
```

#### 4. List Vector Store Configurations

```python
import requests

url = "http://localhost:8104/vector_store/configurations"

response = requests.get(url)
print(response.json())
```

#### 5. Load Vector Store

```python
import requests

url = "http://localhost:8104/vector_store/load/abcd1234-efgh-5678-ijkl-9012mnop3456"

response = requests.post(url)
print(response.json())
```

#### 6. Offload Vector Store

```python
import requests

url = "http://localhost:8104/vector_store/offload/abcd1234-efgh-5678-ijkl-9012mnop3456"

response = requests.post(url)
print(response.json())
```

#### 7. Get Loaded Store IDs

```python
import requests

url = "http://localhost:8104/vector_store/loaded_store_ids"

response = requests.get(url)
print(response.json())
```

#### 8. Add Documents to Vector Store

```python
import requests

url = "http://localhost:8104/vector_store/documents/abcd1234-efgh-5678-ijkl-9012mnop3456"
data = {
    "documents": [
        {"page_content": "Document content", "metadata": {"author": "John Doe"}}
    ]
}

response = requests.post(url, json=data)
print(response.json())
```

#### 9. Add Texts to Vector Store

```python
import requests

url = "http://localhost:8104/vector_store/texts/abcd1234-efgh-5678-ijkl-9012mnop3456"
data = {
    "texts": ["Text content 1", "Text content 2"],
    "metadatas": [{"author": "John Doe"}, {"author": "Jane Doe"}]
}

response = requests.post(url, json=data)
print(response.json())
```

#### 10. Remove Documents from Vector Store

```python
import requests

url = "http://localhost:8104/vector_store/documents/abcd1234-efgh-5678-ijkl-9012mnop3456"
data = {
    "ids": ["id1", "id2"]
}

response = requests.delete(url, json=data)
print(response.json())
```

#### 11. Execute Vector Store Method

```python
import requests

url = "http://localhost:8104/vector_store/method/abcd1234-efgh-5678-ijkl-9012mnop3456"
data = {
    "method_name": "persist",
    "kwargs": {"param1": "value1", "param2": "value2"}
}

response = requests.post(url, json=data)
print(response.json())
```

#### 12. Add Documents from Document Store

```python
import requests

url = "http://localhost:8104/vector_store/add_documents_from_store/abcd1234-efgh-5678-ijkl-9012mnop3456?document_collection=my_document_collection"

response = requests.post(url)
print(response.json())
```

#### 13. Update Document in Vector Store

```python
import requests

url = "http://localhost:8104/vector_store/documents/abcd1234-efgh-5678-ijkl-9012mnop3456/doc1234"
data = {
    "document": {"page_content": "Updated document content", "metadata": {"author": "Jane Doe"}}
}

response = requests.put(url, json=data)
print(response.json())
```

#### 14. Search Vector Store

```python
import requests

url = "http://localhost:8104/vector_store/search/abcd1234-efgh-5678-ijkl-9012mnop3456"
data = {
    "query": "example query",
    "search_type": "similarity",
    "search_kwargs": {"k": 4}
}

response = requests.post(url, json=data

)
print(response.json())
```

#### 15. Filter Vector Store

```python
import requests

url = "http://localhost:8104/vector_store/filter/abcd1234-efgh-5678-ijkl-9012mnop3456"
data = {
    "filter": {"author": "John Doe"},
    "skip": 0,
    "limit": 10
}

response = requests.post(url, json=data)
print(response.json())
```
