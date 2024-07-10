
# API Documentation for Document Transformer Management System

## Overview

This API provides endpoints for configuring and using document transformers. It supports creating, retrieving, updating, and deleting transformer configurations, as well as managing transformer map configurations. The transformers process documents and store the results in a MongoDB database.

## Base URL

```
http://localhost:8103
```

## Endpoints

### 1. Configure Transformer

#### `POST /configure_transformer`

Creates a new transformer configuration with specified parameters.

**Request Body:**
- `config_id` (optional, str): The unique ID for the transformer configuration. If not provided, a new ID will be generated.
- `transformer` (str): The transformer class name.
- `kwargs` (dict): Keyword arguments for the transformer.
- `add_prefix_to_id` (optional, str): Prefix to add to the document ID.
- `add_suffix_to_id` (optional, str): Suffix to add to the document ID.
- `add_split_index_to_id` (bool): Whether to add split index to the document ID.
- `output_store` (optional, dict): Output store configuration.
- `description` (optional, str): Description of the transformer configuration.
- `metadata` (optional, dict): Metadata associated with the transformer configuration.
- `add_metadata_to_docs` (dict): Metadata to add to documents.

**Response:**
- 200 OK: Returns the unique ID of the created transformer configuration.
- 400 Bad Request: Invalid input or configuration ID already exists.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X POST "http://localhost:8103/configure_transformer" -H "Content-Type: application/json" -d '{
  "transformer": "CharacterTextSplitter",
  "kwargs": {"chunk_size": 1, "chunk_overlap": 0, "separator": " "},
  "add_split_index_to_id": true,
  "output_store": {"collection_name": "text_files"},
  "description": "Character Text Splitter Configuration",
  "metadata": {"project": "AI Research"},
  "add_metadata_to_docs": {"author": "John Doe"}
}'
```

**Example Response:**

```json
{
  "config_id": "abcd1234-efgh-5678-ijkl-9012mnop3456"
}
```

### 2. List Transformer Configurations

#### `GET /list_transformer_configs`

Lists all existing transformer configurations.

**Query Parameters:**
- `skip` (optional, int): Number of records to skip.
- `limit` (optional, int): Maximum number of records to return.

**Response:**
- 200 OK: Returns a list of all transformer configurations.
- 400 Bad Request: Invalid input.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X GET "http://localhost:8103/list_transformer_configs?skip=0&limit=10"
```

**Example Response:**

```json
[
  {
    "config_id": "abcd1234-efgh-5678-ijkl-9012mnop3456",
    "transformer": "CharacterTextSplitter",
    "kwargs": {"chunk_size": 1, "chunk_overlap": 0, "separator": " "},
    "add_prefix_to_id": null,
    "add_suffix_to_id": null,
    "add_split_index_to_id": true,
    "output_store": {"collection_name": "text_files"},
    "description": "Character Text Splitter Configuration",
    "metadata": {"project": "AI Research"},
    "add_metadata_to_docs": {"author": "John Doe"}
  }
]
```

### 3. Get Transformer Configuration by ID

#### `GET /get_transformer_config/{config_id}`

Retrieves a specific transformer configuration by its unique ID.

**Path Parameters:**
- `config_id` (str): The unique ID of the transformer configuration to retrieve.

**Response:**
- 200 OK: Returns the transformer configuration.
- 404 Not Found: Configuration not found.
- 400 Bad Request: Invalid input.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X GET "http://localhost:8103/get_transformer_config/abcd1234-efgh-5678-ijkl-9012mnop3456"
```

**Example Response:**

```json
{
  "config_id": "abcd1234-efgh-5678-ijkl-9012mnop3456",
  "transformer": "CharacterTextSplitter",
  "kwargs": {"chunk_size": 1, "chunk_overlap": 0, "separator": " "},
  "add_prefix_to_id": null,
  "add_suffix_to_id": null,
  "add_split_index_to_id": true,
  "output_store": {"collection_name": "text_files"},
  "description": "Character Text Splitter Configuration",
  "metadata": {"project": "AI Research"},
  "add_metadata_to_docs": {"author": "John Doe"}
}
```

### 4. Search Transformer Configurations

#### `POST /search_transformer_configs`

Searches for transformer configurations based on specified criteria.

**Request Body:**
- `transformer` (optional, str): Transformer type to filter configurations.
- `add_prefix_to_id` (optional, str): Prefix to filter configurations.
- `add_suffix_to_id` (optional, str): Suffix to filter configurations.
- `add_split_index_to_id` (optional, bool): Whether to filter by split index addition.
- `metadata` (optional, dict): Metadata to filter configurations.
- `skip` (optional, int): Number of records to skip.
- `limit` (optional, int): Maximum number of records to return.

**Response:**
- 200 OK: Returns a list of configurations matching the search criteria.
- 400 Bad Request: Invalid input.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X POST "http://localhost:8103/search_transformer_configs" -H "Content-Type: application/json" -d '{
  "transformer": "CharacterTextSplitter",
  "add_split_index_to_id": true,
  "metadata": {"project": "AI Research"},
  "skip": 0,
  "limit": 10
}'
```

**Example Response:**

```json
[
  {
    "config_id": "abcd1234-efgh-5678-ijkl-9012mnop3456",
    "transformer": "CharacterTextSplitter",
    "kwargs": {"chunk_size": 1, "chunk_overlap": 0, "separator": " "},
    "add_prefix_to_id": null,
    "add_suffix_to_id": null,
    "add_split_index_to_id": true,
    "output_store": {"collection_name": "text_files"},
    "description": "Character Text Splitter Configuration",
    "metadata": {"project": "AI Research"},
    "add_metadata_to_docs": {"author": "John Doe"}
  }
]
```

### 5. Delete Transformer Configuration

#### `DELETE /delete_transformer_config/{config_id}`

Deletes a specific transformer configuration by its unique ID.

**Path Parameters:**
- `config_id` (str): The unique ID of the transformer configuration to delete.

**Response:**
- 200 OK: Configuration deleted successfully.
- 404 Not Found: Configuration not found.
- 400 Bad Request: Invalid input.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X DELETE "http://localhost:8103/delete_transformer_config/abcd1234-efgh-5678-ijkl-9012mnop3456"
```

**Example Response:**

```json
{
  "detail": "Configuration deleted successfully"
}
```

### 6. Configure Transformer Map

#### `POST /configure_transformer_map`

Creates a new transformer map configuration with specified parameters.

**Request Body:**
- `config_id` (optional, str): The unique ID for the transformer map configuration. If not provided, a new ID will be generated.
- `transformer_map` (dict): Mapping of queries to transformer configurations.
- `default_transformer` (optional, str): The default transformer class name.
- `default_kwargs` (dict): Default keyword arguments for the transformer.
- `default_add_prefix_to_id` (optional, str): Default prefix to add to the document ID.
- `default_add_suffix_to_id` (optional, str): Default suffix to add to the document ID.
- `default_add_split_index_to_id` (bool): Whether to add default split index to the document ID.
- `default_add_metadata_to_docs` (dict): Default metadata to add to documents.
- `default_output_store` (optional, dict): Default output store configuration.
- `description` (optional, str): Description of the transformer map configuration.
- `metadata` (optional, dict): Metadata associated with the transformer map configuration.

**Response:**
- 200 OK: Returns the unique ID of the created transformer map configuration.
- 400 Bad Request: Invalid input or configuration ID already exists.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X POST "http://localhost:8103/configure_transformer_map" -H "Content-Type: application/json" -d '{
  "transformer_map": {"query1": "abcd1234-efgh-5678-ijkl-9012mnop3456"},
  "default_transformer": "CharacterTextSplitter",
  "default_kwargs": {"chunk_size": 1000, "chunk_overlap": 200},
  "default_add_split_index_to_id

": true,
  "default_add_metadata_to_docs": {"default_key": "default_value"},
  "description": "Default transformer map configuration"
}'
```

**Example Response:**

```json
{
  "config_id": "wxyz5678-abcd-1234-ijkl-9012mnop3456"
}
```

### 7. Get Transformer Map Configuration by ID

#### `GET /get_transformer_map_config/{config_id}`

Retrieves a specific transformer map configuration by its unique ID.

**Path Parameters:**
- `config_id` (str): The unique ID of the transformer map configuration to retrieve.

**Response:**
- 200 OK: Returns the transformer map configuration.
- 404 Not Found: Configuration not found.
- 400 Bad Request: Invalid input.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X GET "http://localhost:8103/get_transformer_map_config/wxyz5678-abcd-1234-ijkl-9012mnop3456"
```

**Example Response:**

```json
{
  "config_id": "wxyz5678-abcd-1234-ijkl-9012mnop3456",
  "transformer_map": {"query1": {"transformer": "CharacterTextSplitter", "kwargs": {"chunk_size": 1, "chunk_overlap": 0, "separator": " "}, "add_split_index_to_id": true, "output_store": {"collection_name": "text_files"}, "description": "Character Text Splitter Configuration", "metadata": {"project": "AI Research"}, "add_metadata_to_docs": {"author": "John Doe"}}},
  "default_transformer": "CharacterTextSplitter",
  "default_kwargs": {"chunk_size": 1000, "chunk_overlap": 200},
  "default_add_prefix_to_id": null,
  "default_add_suffix_to_id": null,
  "default_add_split_index_to_id": true,
  "default_add_metadata_to_docs": {"default_key": "default_value"},
  "default_output_store": null,
  "description": "Default transformer map configuration",
  "metadata": null
}
```

### 8. Transform Documents

#### `POST /transform_documents/{config_id}`

Transforms documents using a configured transformer map identified by a unique configuration ID.

**Path Parameters:**
- `config_id` (str): The unique ID of the transformer map configuration.

**Request Body:**
- `documents` (list): List of documents to be transformed.

**Response:**
- 200 OK: Returns the transformed documents with their metadata.
- 404 Not Found: Configuration not found.
- 400 Bad Request: Invalid input.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X POST "http://localhost:8103/transform_documents/wxyz5678-abcd-1234-ijkl-9012mnop3456" -H "Content-Type: application/json" -d '{
  "documents": [
    {
      "page_content": "This is the content of the document.",
      "metadata": {"author": "John Doe", "category": "Research"}
    }
  ]
}'
```

**Example Response:**

```json
[
  {
    "page_content": "This is the content of the document.",
    "metadata": {"author": "John Doe", "category": "Research", "doc_store_id": "abcd1234-efgh-5678-ijkl-9012mnop3456", "doc_store_collection": "text_files"}
  }
]
```

### 9. Transform Documents from Store

#### `POST /transform_documents_from_store/{config_id}`

Transforms documents directly from a specified MongoDB collection using a configured transformer map identified by a unique configuration ID.

**Path Parameters:**
- `config_id` (str): The unique ID of the transformer map configuration.

**Request Body:**
- `input_store` (dict): Input store configuration.

**Response:**
- 200 OK: Returns the transformed documents with their metadata.
- 404 Not Found: Configuration not found.
- 400 Bad Request: Invalid input.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X POST "http://localhost:8103/transform_documents_from_store/wxyz5678-abcd-1234-ijkl-9012mnop3456" -H "Content-Type: application/json" -d '{
  "input_store": {"collection_name": "input_text_files"}
}'
```

**Example Response:**

```json
[
  {
    "page_content": "This is the content of the document.",
    "metadata": {"author": "John Doe", "category": "Research", "doc_store_id": "abcd1234-efgh-5678-ijkl-9012mnop3456", "doc_store_collection": "text_files"}
  }
]
```

### 10. List Transformer Map Configurations

#### `GET /list_transformer_map_configs`

Lists all existing transformer map configurations.

**Query Parameters:**
- `skip` (optional, int): Number of records to skip.
- `limit` (optional, int): Maximum number of records to return.

**Response:**
- 200 OK: Returns a list of all transformer map configurations.
- 400 Bad Request: Invalid input.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X GET "http://localhost:8103/list_transformer_map_configs?skip=0&limit=10"
```

**Example Response:**

```json
[
  {
    "config_id": "wxyz5678-abcd-1234-ijkl-9012mnop3456",
    "transformer_map": {"query1": {"transformer": "CharacterTextSplitter", "kwargs": {"chunk_size": 1, "chunk_overlap": 0, "separator": " "}, "add_split_index_to_id": true, "output_store": {"collection_name": "text_files"}, "description": "Character Text Splitter Configuration", "metadata": {"project": "AI Research"}, "add_metadata_to_docs": {"author": "John Doe"}}},
    "default_transformer": "CharacterTextSplitter",
    "default_kwargs": {"chunk_size": 1000, "chunk_overlap": 200},
    "default_add_prefix_to_id": null,
    "default_add_suffix_to_id": null,
    "default_add_split_index_to_id": true,
    "default_add_metadata_to_docs": {"default_key": "default_value"},
    "default_output_store": null,
    "description": "Default transformer map configuration",
    "metadata": null
  }
]
```

### 11. Search Transformer Map Configurations

#### `POST /search_transformer_map_configs`

Searches for transformer map configurations based on specified criteria.

**Request Body:**
- `transformer` (optional, str): Transformer type to filter configurations.
- `add_prefix_to_id` (optional, str): Prefix to filter configurations.
- `add_suffix_to_id` (optional, str): Suffix to filter configurations.
- `add_split_index_to_id` (optional, bool): Whether to filter by split index addition.
- `metadata` (optional, dict): Metadata to filter configurations.
- `skip` (optional, int): Number of records to skip.
- `limit` (optional, int): Maximum number of records to return.

**Response:**
- 200 OK: Returns a list of configurations matching the search criteria.
- 400 Bad Request: Invalid input.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X POST "http://localhost:8103/search_transformer_map_configs" -H "Content-Type: application/json" -d '{
  "transformer": "CharacterTextSplitter",
  "add_split_index_to_id": true,
  "metadata": {"project": "AI Research"},
  "skip": 0,
  "limit": 10
}'
```

**Example Response:**

```json
[
  {
    "config_id": "wxyz5678-abcd-1234-ijkl-9012mnop3456",
    "transformer_map": {"query1": {"transformer": "CharacterTextSplitter", "kwargs": {"chunk_size": 1, "chunk_overlap": 0, "separator": " "}, "add_split_index_to_id": true, "output_store": {"collection_name": "text_files"}, "description": "Character Text Splitter Configuration", "metadata": {"project": "AI Research"}, "add_metadata_to_docs": {"author": "John Doe"}}},
    "default_transformer": "CharacterTextSplitter",
    "default_kwargs": {"chunk_size": 1000, "chunk_overlap": 200},
    "default_add_prefix_to_id": null,
    "default_add_suffix_to_id": null,
    "default_add_split_index_to_id": true,
    "default_add_metadata_to_docs": {"default_key": "default_value"},
    "default_output_store": null,
    "description": "Default transformer map configuration",
    "metadata": null
  }
]
```

### 12. Delete Transformer Map Configuration

#### `DELETE /delete_transformer_map_config/{config_id}`

Deletes a specific transformer map configuration by its unique ID.

**Path Parameters:**
- `config_id` (str): The unique ID of the transformer map configuration to delete.

**Response:**
- 200 OK: Configuration deleted successfully.
- 404 Not Found: Configuration not found.
- 400 Bad Request: Invalid input.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X DELETE "http://localhost:8103/delete_transformer_map_config/wxyz5678-ab

cd-1234-ijkl-9012mnop3456"
```

**Example Response:**

```json
{
  "detail": "Configuration deleted successfully"
}
```

## Models

### TransformerConfig

Model representing the configuration for a transformer.

**Attributes:**
- `config_id` (optional, str): The unique ID for the transformer configuration.
- `transformer` (str): The transformer class name.
- `kwargs` (dict): Keyword arguments for the transformer.
- `add_prefix_to_id` (optional, str): Prefix to add to the document ID.
- `add_suffix_to_id` (optional, str): Suffix to add to the document ID.
- `add_split_index_to_id` (bool): Whether to add split index to the document ID.
- `output_store` (optional, dict): Output store configuration.
- `description` (optional, str): Description of the transformer configuration.
- `metadata` (optional, dict): Metadata associated with the transformer configuration.
- `add_metadata_to_docs` (dict): Metadata to add to documents.

**Example:**

```json
{
  "config_id": "abcd1234-efgh-5678-ijkl-9012mnop3456",
  "transformer": "CharacterTextSplitter",
  "kwargs": {"chunk_size": 1, "chunk_overlap": 0, "separator": " "},
  "add_prefix_to_id": null,
  "add_suffix_to_id": null,
  "add_split_index_to_id": true,
  "output_store": {"collection_name": "text_files"},
  "description": "Character Text Splitter Configuration",
  "metadata": {"project": "AI Research"},
  "add_metadata_to_docs": {"author": "John Doe"}
}
```

### TransformerMapConfig

Model representing the configuration for a transformer map.

**Attributes:**
- `config_id` (optional, str): The unique ID for the transformer map configuration.
- `transformer_map` (dict): Mapping of queries to transformer configurations.
- `default_transformer` (optional, str): The default transformer class name.
- `default_kwargs` (dict): Default keyword arguments for the transformer.
- `default_add_prefix_to_id` (optional, str): Default prefix to add to the document ID.
- `default_add_suffix_to_id` (optional, str): Default suffix to add to the document ID.
- `default_add_split_index_to_id` (bool): Whether to add default split index to the document ID.
- `default_add_metadata_to_docs` (dict): Default metadata to add to documents.
- `default_output_store` (optional, dict): Default output store configuration.
- `description` (optional, str): Description of the transformer map configuration.
- `metadata` (optional, dict): Metadata associated with the transformer map configuration.

**Example:**

```json
{
  "config_id": "wxyz5678-abcd-1234-ijkl-9012mnop3456",
  "transformer_map": {"query1": {"transformer": "CharacterTextSplitter", "kwargs": {"chunk_size": 1, "chunk_overlap": 0, "separator": " "}, "add_split_index_to_id": true, "output_store": {"collection_name": "text_files"}, "description": "Character Text Splitter Configuration", "metadata": {"project": "AI Research"}, "add_metadata_to_docs": {"author": "John Doe"}}},
  "default_transformer": "CharacterTextSplitter",
  "default_kwargs": {"chunk_size": 1000, "chunk_overlap": 200},
  "default_add_prefix_to_id": null,
  "default_add_suffix_to_id": null,
  "default_add_split_index_to_id": true,
  "default_add_metadata_to_docs": {"default_key": "default_value"},
  "default_output_store": null,
  "description": "Default transformer map configuration",
  "metadata": null
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
  "metadata": {"author": "John Doe", "category": "Research"}
}
```

### SearchConfig

Model representing the criteria for searching configurations.

**Attributes:**
- `transformer` (optional, str): Transformer type to filter configurations.
- `add_prefix_to_id` (optional, str): Prefix to filter configurations.
- `add_suffix_to_id` (optional, str): Suffix to filter configurations.
- `add_split_index_to_id` (optional, bool): Whether to filter by split index addition.
- `metadata` (optional, dict): Metadata to filter configurations.
- `skip` (optional, int): Number of records to skip.
- `limit` (optional, int): Maximum number of records to return.

**Example:**

```json
{
  "transformer": "CharacterTextSplitter",
  "add_prefix_to_id": "doc_",
  "add_suffix_to_id": "_001",
  "add_split_index_to_id": true,
  "metadata": {"project": "AI Research"},
  "skip": 0,
  "limit": 10
}
```

## Usage

To use the API, you can make HTTP requests to the provided endpoints using tools like `curl`, Postman, or any HTTP client library in your preferred programming language.

### Usage Example with Python

Below is a Python example using the `requests` library to interact with the API:

#### 1. Configure Transformer

```python
import requests

url = "http://localhost:8103/configure_transformer"
data = {
    "transformer": "CharacterTextSplitter",
    "kwargs": {"chunk_size": 1, "chunk_overlap": 0, "separator": " "},
    "add_split_index_to_id": True,
    "output_store": {"collection_name": "text_files"},
    "description": "Character Text Splitter Configuration",
    "metadata": {"project": "AI Research"},
    "add_metadata_to_docs": {"author": "John Doe"}
}

response = requests.post(url, json=data)
print(response.json())
```

#### 2. List Transformer Configurations

```python
import requests

url = "http://localhost:8103/list_transformer_configs?skip=0&limit=10"

response = requests.get(url)
print(response.json())
```

#### 3. Get Transformer Configuration by ID

```python
import requests

url = "http://localhost:8103/get_transformer_config/abcd1234-efgh-5678-ijkl-9012mnop3456"

response = requests.get(url)
print(response.json())
```

#### 4. Search Transformer Configurations

```python
import requests

url = "http://localhost:8103/search_transformer_configs"
data = {
    "transformer": "CharacterTextSplitter",
    "add_split_index_to_id": True,
    "metadata": {"project": "AI Research"},
    "skip": 0,
    "limit": 10
}

response = requests.post(url, json=data)
print(response.json())
```

#### 5. Delete Transformer Configuration

```python
import requests

url = "http://localhost:8103/delete_transformer_config/abcd1234-efgh-5678-ijkl-9012mnop3456"

response = requests.delete(url)
print(response.json())
```

#### 6. Configure Transformer Map

```python
import requests

url = "http://localhost:8103/configure_transformer_map"
data = {
    "transformer_map": {"query1": "abcd1234-efgh-5678-ijkl-9012mnop3456"},
    "default_transformer": "CharacterTextSplitter",
    "default_kwargs": {"chunk_size": 1000, "chunk_overlap": 200},
    "default_add_split_index_to_id": True,
    "default_add_metadata_to_docs": {"default_key": "default_value"},
    "description": "Default transformer map configuration"
}

response = requests.post(url, json=data)
print(response.json())
```

#### 7. Get Transformer Map Configuration by ID

```python
import requests

url = "http://localhost:8103/get_transformer_map_config/wxyz5678-abcd-1234-ijkl-9012mnop3456"

response = requests.get(url)
print(response.json())
```

#### 8. Transform Documents

```python
import requests

url = "http://localhost:8103/transform_documents/wxyz5678-abcd-1234-ijkl-9012mnop3456"
data = {
    "documents": [
        {
            "page_content": "This is the content of the document.",
            "metadata": {"author": "John Doe", "category": "Research"}
        }
    ]
}

response = requests.post(url, json=data)
print(response.json())
```

#### 9. Transform Documents from Store

```python
import requests

url = "http://localhost:8103/transform_documents_from_store/wxyz5678-abcd-1234-ijkl-9012mnop3456"
data = {
    "input_store": {"collection_name": "input_text_files"}
}

response = requests.post(url, json=data)
print(response.json())
```

#### 10. List Transformer Map Configurations

```python
import requests

url = "http://localhost:8103/list_transformer_map_configs?skip=0&limit=10"

response = requests.get(url)
print(response.json())
```

#### 11. Search Transformer Map Configurations

```python
import requests

url = "http://localhost:8103/search_transformer_map_configs"
data = {
   

 "transformer": "CharacterTextSplitter",
    "add_split_index_to_id": True,
    "metadata": {"project": "AI Research"},
    "skip": 0,
    "limit": 10
}

response = requests.post(url, json=data)
print(response.json())
```

#### 12. Delete Transformer Map Configuration

```python
import requests

url = "http://localhost:8103/delete_transformer_map_config/wxyz5678-abcd-1234-ijkl-9012mnop3456"

response = requests.delete(url)
print(response.json())
```
