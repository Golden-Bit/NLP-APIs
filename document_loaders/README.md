
# API Documentation for Custom Directory Loader

## Overview

This API provides endpoints for configuring and using custom directory loaders. It allows users to create loader configurations, load documents using these configurations, retrieve loader configurations by ID, list all existing configurations, search for configurations based on criteria, and delete configurations. The configurations and loaded documents are stored in a MongoDB database.

## Base URL

```
http://localhost:8101
```

## Endpoints

### 1. Configure Loader

#### `POST /configure_loader`

Creates a new loader configuration with specified parameters.

**Request Body:**
- `config_id` (optional, str): The unique ID for the loader configuration. If not provided, a new ID will be generated. Example: "abcd1234-efgh-5678-ijkl-9012mnop3456".
- `path` (str): The path to the directory containing documents to load. Example: "/path/to/documents".
- `loader_map` (dict): Mapping of file patterns to loader classes. Example: {"*.txt": "TextLoader", "*.html": "BSHTMLLoader"}.
- `loader_kwargs_map` (optional, dict): Optional keyword arguments for each loader. Example: {"*.csv": {"delimiter": ","}}.
- `metadata_map` (optional, dict): Mapping of file patterns to metadata. Example: {"*.txt": {"author": "John Doe"}}.
- `default_metadata` (optional, dict): Default metadata to apply to all documents. Example: {"project": "AI Research"}.
- `recursive` (bool): Whether to load documents recursively from subdirectories. Example: True.
- `max_depth` (optional, int): Maximum depth for recursive loading. Example: 5.
- `silent_errors` (bool): Whether to ignore errors during document loading. Example: True.
- `load_hidden` (bool): Whether to load hidden files. Example: True.
- `show_progress` (bool): Whether to show progress during loading. Example: True.
- `use_multithreading` (bool): Whether to use multithreading for loading. Example: True.
- `max_concurrency` (int): Maximum number of concurrent threads for loading. Example: 8.
- `exclude` (optional, list): List of file patterns to exclude from loading. Example: ["*.tmp", "*.log"].
- `sample_size` (int): Number of samples to load. If 0, all documents are loaded. Example: 10.
- `randomize_sample` (bool): Whether to randomize the sample. Example: True.
- `sample_seed` (optional, int): Seed for randomization of the sample. Example: 42.
- `output_store_map` (optional, dict): Mapping of file patterns to output stores. Example: {"*.txt": {"collection_name": "text_files"}}.
- `default_output_store` (optional, dict): Default output store configuration. Example: {"collection_name": "default_store"}.

**Response:**
- 200 OK: Returns the unique ID of the created loader configuration.
- 400 Bad Request: Invalid input or configuration ID already exists.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X POST "http://localhost:8101/configure_loader" -H "Content-Type: application/json" -d '{
  "path": "/path/to/documents",
  "loader_map": {"*.txt": "TextLoader", "*.html": "BSHTMLLoader"},
  "default_metadata": {"project": "AI Research"},
  "recursive": true,
  "max_depth": 5,
  "silent_errors": true,
  "load_hidden": true,
  "show_progress": true,
  "use_multithreading": true,
  "max_concurrency": 8,
  "exclude": ["*.tmp", "*.log"],
  "sample_size": 10,
  "randomize_sample": true,
  "sample_seed": 42,
  "output_store_map": {"*.txt": {"collection_name": "text_files"}},
  "default_output_store": {"collection_name": "default_store"}
}'
```

**Example Response:**

```json
{
  "config_id": "abcd1234-efgh-5678-ijkl-9012mnop3456"
}
```

### 2. Load Documents

#### `POST /load_documents/{config_id}`

Loads documents using a pre-configured loader identified by a unique configuration ID.

**Path Parameters:**
- `config_id` (str): The unique ID of the loader configuration. Example: "abcd1234-efgh-5678-ijkl-9012mnop3456".

**Response:**
- 200 OK: Returns a list of loaded documents with their metadata.
- 404 Not Found: Configuration not found.
- 400 Bad Request: Invalid input.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X POST "http://localhost:8101/load_documents/abcd1234-efgh-5678-ijkl-9012mnop3456"
```

**Example Response:**

```json
[
  {
    "page_content": "This is the content of the document.",
    "metadata": {
      "author": "John Doe",
      "category": "Research",
      "doc_store_id": "abcd1234-efgh-5678-ijkl-9012mnop3456",
      "doc_store_collection": "text_files"
    },
    "type": "Document"
  }
]
```

### 3. Get Configuration by ID

#### `GET /get_config/{config_id}`

Retrieves a single loader configuration by its unique ID.

**Path Parameters:**
- `config_id` (str): The unique ID of the loader configuration to retrieve. Example: "abcd1234-efgh-5678-ijkl-9012mnop3456".

**Response:**
- 200 OK: Returns the loader configuration.
- 404 Not Found: Configuration not found.
- 400 Bad Request: Invalid input.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X GET "http://localhost:8101/get_config/abcd1234-efgh-5678-ijkl-9012mnop3456"
```

**Example Response:**

```json
{
  "config_id": "abcd1234-efgh-5678-ijkl-9012mnop3456",
  "path": "/path/to/documents",
  "loader_map": {"*.txt": "TextLoader", "*.html": "BSHTMLLoader"},
  "default_metadata": {"project": "AI Research"},
  "recursive": true,
  "max_depth": 5,
  "silent_errors": true,
  "load_hidden": true,
  "show_progress": true,
  "use_multithreading": true,
  "max_concurrency": 8,
  "exclude": ["*.tmp", "*.log"],
  "sample_size": 10,
  "randomize_sample": true,
  "sample_seed": 42,
  "output_store_map": {"*.txt": {"collection_name": "text_files"}},
  "default_output_store": {"collection_name": "default_store"}
}
```

### 4. List Configurations

#### `GET /list_configs`

Lists all existing loader configurations.

**Response:**
- 200 OK: Returns a list of all loader configurations.
- 400 Bad Request: Invalid input.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X GET "http://localhost:8101/list_configs"
```

**Example Response:**

```json
[
  {
    "config_id": "abcd1234-efgh-5678-ijkl-9012mnop3456",
    "path": "/path/to/documents",
    "loader_map": {"*.txt": "TextLoader", "*.html": "BSHTMLLoader"},
    "default_metadata": {"project": "AI Research"},
    "recursive": true,
    "max_depth": 5,
    "silent_errors": true,
    "load_hidden": true,
    "show_progress": true,
    "use_multithreading": true,
    "max_concurrency": 8,
    "exclude": ["*.tmp", "*.log"],
    "sample_size": 10,
    "randomize_sample": true,
    "sample_seed": 42,
    "output_store_map": {"*.txt": {"collection_name": "text_files"}},
    "default_output_store": {"collection_name": "default_store"}
  }
]
```

### 5. Search Configurations

#### `POST /search_configs`

Searches for loader configurations based on specified criteria.

**Request Body:**
- `path` (optional, str): Path to filter configurations. Example: "/path/to/documents".
- `loader_type` (optional, str): Loader type to filter configurations. Example: "TextLoader".
- `recursive` (optional, bool): Whether to filter by recursive loading. Example: True.
- `max_depth` (optional, int): Maximum depth to filter configurations. Example: 5.

**Response:**
- 200 OK: Returns a list of configurations matching the search criteria.
- 400 Bad Request: Invalid input.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X POST "http://localhost:8101/search_configs" -H "Content-Type: application/json" -d '{
  "path": "/path/to/documents",
  "loader_type": "TextLoader",
  "recursive": true,
  "max_depth": 5
}'
```

**Example Response:**

```json
[
  {
    "config_id": "abcd123

4-efgh-5678-ijkl-9012mnop3456",
    "path": "/path/to/documents",
    "loader_map": {"*.txt": "TextLoader", "*.html": "BSHTMLLoader"},
    "default_metadata": {"project": "AI Research"},
    "recursive": true,
    "max_depth": 5,
    "silent_errors": true,
    "load_hidden": true,
    "show_progress": true,
    "use_multithreading": true,
    "max_concurrency": 8,
    "exclude": ["*.tmp", "*.log"],
    "sample_size": 10,
    "randomize_sample": true,
    "sample_seed": 42,
    "output_store_map": {"*.txt": {"collection_name": "text_files"}},
    "default_output_store": {"collection_name": "default_store"}
  }
]
```

### 6. Delete Configuration

#### `DELETE /delete_config/{config_id}`

Deletes a loader configuration by its unique ID.

**Path Parameters:**
- `config_id` (str): The unique ID of the loader configuration to delete. Example: "abcd1234-efgh-5678-ijkl-9012mnop3456".

**Response:**
- 200 OK: Configuration deleted successfully.
- 404 Not Found: Configuration not found.
- 400 Bad Request: Invalid input.
- 500 Internal Server Error: Server error.

**Example Request:**

```bash
curl -X DELETE "http://localhost:8101/delete_config/abcd1234-efgh-5678-ijkl-9012mnop3456"
```

**Example Response:**

```json
{
  "detail": "Configuration deleted successfully"
}
```

## Models

### LoaderConfig

Model representing the configuration for a loader.

**Attributes:**
- `config_id` (optional, str): The unique ID for the loader configuration. Example: "abcd1234-efgh-5678-ijkl-9012mnop3456".
- `path` (str): The path to the directory containing documents to load. Example: "/path/to/documents".
- `loader_map` (dict): Mapping of file patterns to loader classes. Example: {"*.txt": "TextLoader", "*.html": "BSHTMLLoader"}.
- `loader_kwargs_map` (optional, dict): Optional keyword arguments for each loader. Example: {"*.csv": {"delimiter": ","}}.
- `metadata_map` (optional, dict): Mapping of file patterns to metadata. Example: {"*.txt": {"author": "John Doe"}}.
- `default_metadata` (optional, dict): Default metadata to apply to all documents. Example: {"project": "AI Research"}.
- `recursive` (bool): Whether to load documents recursively from subdirectories. Example: True.
- `max_depth` (optional, int): Maximum depth for recursive loading. Example: 5.
- `silent_errors` (bool): Whether to ignore errors during document loading. Example: True.
- `load_hidden` (bool): Whether to load hidden files. Example: True.
- `show_progress` (bool): Whether to show progress during loading. Example: True.
- `use_multithreading` (bool): Whether to use multithreading for loading. Example: True.
- `max_concurrency` (int): Maximum number of concurrent threads for loading. Example: 8.
- `exclude` (optional, list): List of file patterns to exclude from loading. Example: ["*.tmp", "*.log"].
- `sample_size` (int): Number of samples to load. If 0, all documents are loaded. Example: 10.
- `randomize_sample` (bool): Whether to randomize the sample. Example: True.
- `sample_seed` (optional, int): Seed for randomization of the sample. Example: 42.
- `output_store_map` (optional, dict): Mapping of file patterns to output stores. Example: {"*.txt": {"collection_name": "text_files"}}.
- `default_output_store` (optional, dict): Default output store configuration. Example: {"collection_name": "default_store"}.

**Example:**

```json
{
  "config_id": "abcd1234-efgh-5678-ijkl-9012mnop3456",
  "path": "/path/to/documents",
  "loader_map": {"*.txt": "TextLoader", "*.html": "BSHTMLLoader"},
  "loader_kwargs_map": {"*.csv": {"delimiter": ","}},
  "metadata_map": {"*.txt": {"author": "John Doe"}},
  "default_metadata": {"project": "AI Research"},
  "recursive": true,
  "max_depth": 5,
  "silent_errors": true,
  "load_hidden": true,
  "show_progress": true,
  "use_multithreading": true,
  "max_concurrency": 8,
  "exclude": ["*.tmp", "*.log"],
  "sample_size": 10,
  "randomize_sample": true,
  "sample_seed": 42,
  "output_store_map": {"*.txt": {"collection_name": "text_files"}},
  "default_output_store": {"collection_name": "default_store"}
}
```

### DocumentModel

Model representing a document.

**Attributes:**
- `page_content` (str): The content of the document. Example: "This is the content of the document."
- `metadata` (dict): Metadata associated with the document. Example: {"author": "John Doe", "category": "Research"}.
- `type` (str): Type of the document. Example: "Document".

**Example:**

```json
{
  "page_content": "This is the content of the document.",
  "metadata": {"author": "John Doe", "category": "Research"},
  "type": "Document"
}
```

### SearchConfig

Model representing the criteria for searching configurations.

**Attributes:**
- `path` (optional, str): Path to filter configurations. Example: "/path/to/documents".
- `loader_type` (optional, str): Loader type to filter configurations. Example: "TextLoader".
- `recursive` (optional, bool): Whether to filter by recursive loading. Example: True.
- `max_depth` (optional, int): Maximum depth to filter configurations. Example: 5.

**Example:**

```json
{
  "path": "/path/to/documents",
  "loader_type": "TextLoader",
  "recursive": true,
  "max_depth": 5
}
```

## Usage

To use the API, you can make HTTP requests to the provided endpoints using tools like `curl`, Postman, or any HTTP client library in your preferred programming language.

### Usage Example with Python

Below is a Python example using the `requests` library to interact with the API:

#### 1. Configure Loader

```python
import requests

url = "http://localhost:8101/configure_loader"
data = {
    "path": "/path/to/documents",
    "loader_map": {"*.txt": "TextLoader", "*.html": "BSHTMLLoader"},
    "default_metadata": {"project": "AI Research"},
    "recursive": True,
    "max_depth": 5,
    "silent_errors": True,
    "load_hidden": True,
    "show_progress": True,
    "use_multithreading": True,
    "max_concurrency": 8,
    "exclude": ["*.tmp", "*.log"],
    "sample_size": 10,
    "randomize_sample": True,
    "sample_seed": 42,
    "output_store_map": {"*.txt": {"collection_name": "text_files"}},
    "default_output_store": {"collection_name": "default_store"}
}

response = requests.post(url, json=data)
print(response.json())
```

#### 2. Load Documents

```python
import requests

url = "http://localhost:8101/load_documents/abcd1234-efgh-5678-ijkl-9012mnop3456"

response = requests.post(url)
print(response.json())
```

#### 3. Get Configuration by ID

```python
import requests

url = "http://localhost:8101/get_config/abcd1234-efgh-5678-ijkl-9012mnop3456"

response = requests.get(url)
print(response.json())
```

#### 4. List Configurations

```python
import requests

url = "http://localhost:8101/list_configs"

response = requests.get(url)
print(response.json())
```

#### 5. Search Configurations

```python
import requests

url = "http://localhost:8101/search_configs"
data = {
    "path": "/path/to/documents",
    "loader_type": "TextLoader",
    "recursive": True,
    "max_depth": 5
}

response = requests.post(url, json=data)
print(response.json())
```

#### 6. Delete Configuration

```python
import requests

url = "http://localhost:8101/delete_config/abcd1234-efgh-5678-ijkl-9012mnop3456"

response = requests.delete(url)
print(response.json())
```
