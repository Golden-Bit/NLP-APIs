# API Documentation for Embedding Model Management System

## Overview

This API provides endpoints for configuring, managing, and performing inference with Embedding Models. The API supports creating, retrieving, updating, and deleting model configurations, as well as loading and unloading models into memory and performing inference.

## Base URL

```
http://localhost:8104
```

## Endpoints

### 1. Configure Embedding Model

#### `POST /embedding_models/configure_embedding_model/`

Configures a new embedding model and stores its configuration.

**Request Body:**
- `config_id` (str, required): The unique ID of the embedding configuration.
- `model_id` (str, required): The unique ID of the embedding model.
- `model_class` (str, required): The class of the embedding model (e.g., 'HuggingFaceEmbeddings', 'OpenAIEmbeddings').
- `model_kwargs` (dict, optional): Additional keyword arguments for model initialization.

**Response:**
- 200 OK: Returns the configuration ID of the newly created model configuration.

**Example Request:**

```bash
curl -X POST "http://localhost:8104/embedding_models/configure_embedding_model/" -H "Content-Type: application/json" -d '{
  "config_id": "example_embedding_config",
  "model_id": "example_model",
  "model_class": "HuggingFaceEmbeddings",
  "model_kwargs": {
    "model_name": "distilbert-base-uncased"
  }
}'
```

**Example Response:**

```json
{
  "config_id": "example_embedding_config"
}
```

### 2. Load Embedding Model

#### `POST /embedding_models/load_embedding_model/{config_id}`

Loads an embedding model based on its configuration ID.

**Path Parameters:**
- `config_id` (str, required): The configuration ID of the embedding model to load.

**Response:**
- 200 OK: Returns a success message.

**Example Request:**

```bash
curl -X POST "http://localhost:8104/embedding_models/load_embedding_model/example_embedding_config"
```

**Example Response:**

```json
{
  "message": "Model loaded successfully"
}
```

### 3. Unload Embedding Model

#### `POST /embedding_models/unload_embedding_model/{model_id}`

Unloads an embedding model from memory.

**Path Parameters:**
- `model_id` (str, required): The ID of the embedding model to unload.

**Response:**
- 200 OK: Returns a success message.

**Example Request:**

```bash
curl -X POST "http://localhost:8104/embedding_models/unload_embedding_model/example_model"
```

**Example Response:**

```json
{
  "message": "Model unloaded successfully"
}
```

### 4. Perform Inference

#### `POST /embedding_models/embedding_inference/`

Performs inference using a loaded embedding model.

**Request Body:**
- `model_id` (str, required): The ID of the embedding model to use for inference.
- `texts` (list of str, required): The texts to generate embeddings for.
- `inference_kwargs` (dict, optional): Additional keyword arguments for inference.

**Response:**
- 200 OK: Returns the inference response with generated embeddings.

**Example Request:**

```bash
curl -X POST "http://localhost:8104/embedding_models/embedding_inference/" -H "Content-Type: application/json" -d '{
  "model_id": "example_model",
  "texts": ["Hello world", "How are you?"],
  "inference_kwargs": {}
}'
```

**Example Response:**

```json
{
  "embeddings": [
    [0.123, 0.456, 0.789],
    [0.321, 0.654, 0.987]
  ]
}
```

### 5. List Loaded Embedding Models

#### `GET /embedding_models/list_loaded_embedding_models/`

Lists all currently loaded embedding models.

**Response:**
- 200 OK: Returns a list of loaded model IDs.

**Example Request:**

```bash
curl -X GET "http://localhost:8104/embedding_models/list_loaded_embedding_models/"
```

**Example Response:**

```json
[
  "example_model"
]
```

### 6. Get Embedding Model Configuration

#### `GET /embedding_models/embedding_model_config/{config_id}`

Retrieves a specific embedding model configuration.

**Path Parameters:**
- `config_id` (str, required): The configuration ID to retrieve.

**Response:**
- 200 OK: Returns the model configuration.

**Example Request:**

```bash
curl -X GET "http://localhost:8104/embedding_models/embedding_model_config/example_embedding_config"
```

**Example Response:**

```json
{
  "config_id": "example_embedding_config",
  "model_id": "example_model",
  "model_class": "HuggingFaceEmbeddings",
  "model_kwargs": {
    "model_name": "distilbert-base-uncased"
  }
}
```

### 7. Delete Embedding Model Configuration

#### `DELETE /embedding_models/embedding_model_config/{config_id}`

Deletes a specific embedding model configuration.

**Path Parameters:**
- `config_id` (str, required): The configuration ID to delete.

**Response:**
- 200 OK: Returns a success message.

**Example Request:**

```bash
curl -X DELETE "http://localhost:8104/embedding_models/embedding_model_config/example_embedding_config"
```

**Example Response:**

```json
{
  "detail": "Configuration deleted successfully"
}
```

### 8. Execute Method on Embedding Model

#### `POST /embedding_models/execute_embedding_method/`

Executes a method on a loaded embedding model instance.

**Request Body:**
- `model_id` (str, required): The ID of the embedding model.
- `method_name` (str, required): The name of the method to call on the embedding model.
- `args` (list, optional): The positional arguments for the method (if any).
- `kwargs` (dict, optional): The keyword arguments for the method (if any).

**Response:**
- 200 OK: Returns the result of the method execution.

**Example Request:**

```bash
curl -X POST "http://localhost:8104/embedding_models/execute_embedding_method/" -H "Content-Type: application/json" -d '{
  "model_id": "example_model",
  "method_name": "generate",
  "args": [],
  "kwargs": {}
}'
```

**Example Response:**

```json
{
  "result": "Method executed successfully"
}
```

### 9. Get Attribute of Embedding Model

#### `POST /embedding_models/get_embedding_attribute/`

Gets an attribute of a loaded embedding model instance.

**Request Body:**
- `model_id` (str, required): The ID of the embedding model.
- `attribute_name` (str, required): The name of the attribute to retrieve.

**Response:**
- 200 OK: Returns the value of the specified attribute.

**Example Request:**

```bash
curl -X POST "http://localhost:8104/embedding_models/get_embedding_attribute/" -H "Content-Type: application/json" -d '{
  "model_id": "example_model",
  "attribute_name": "attribute_name"
}'
```

**Example Response:**

```json
{
  "attribute": "Attribute value"
}
```

## Models

**EmbeddingConfigRequest**
- `config_id` (str): The unique ID of the embedding configuration.
- `model_id` (str): The unique ID of the embedding model.
- `model_class` (str): The class of the embedding model (e.g., 'HuggingFaceEmbeddings', 'OpenAIEmbeddings').
- `model_kwargs` (dict): Additional keyword arguments for model initialization.

**InferenceRequest**
- `model_id` (str): The ID of the embedding model to use for inference.
- `texts` (list of str): The texts to generate embeddings for.
- `inference_kwargs` (dict): Additional keyword arguments for inference.

**ExecuteMethodRequest**
- `model_id` (str): The ID of the embedding model.
- `method_name` (str): The name of the method to call on the embedding model.
- `args` (list): The positional arguments for the method (if any).
- `kwargs` (dict): The keyword arguments for the method (if any).

**GetAttributeRequest**
- `model_id` (str): The ID of the embedding model.
- `attribute_name` (str): The name of the attribute to retrieve.

## Usage

To use the API, you can make HTTP requests to the provided endpoints using tools like `curl`, Postman, or any HTTP client library in your preferred programming language.

### Usage Example with Python

Below is a Python example using the `requests` library to interact with the API:

#### 1. Configure Embedding Model

```python
import requests

url = "http://localhost:8104/embedding_models/configure_embedding_model/"
data = {
    "config_id": "example_embedding_config",
    "model_id": "example_model",
    "model_class": "HuggingFaceEmbeddings",
    "model_kwargs": {
        "model_name": "distilbert-base-uncased"
    }
}

response = requests.post(url, json=data)
print(response.json())
```

#### 2. Load Embedding Model

```python
import requests

url = "http://localhost:8104/embedding_models/load_embedding_model/example_embedding_config"

response = requests.post(url)
print(response

.json())
```

#### 3. Unload Embedding Model

```python
import requests

url = "http://localhost:8104/embedding_models/unload_embedding_model/example_model"

response = requests.post(url)
print(response.json())
```

#### 4. Perform Inference

```python
import requests

url = "http://localhost:8104/embedding_models/embedding_inference/"
data = {
    "model_id": "example_model",
    "texts": ["Hello world", "How are you?"],
    "inference_kwargs": {}
}

response = requests.post(url, json=data)
print(response.json())
```

#### 5. List Loaded Embedding Models

```python
import requests

url = "http://localhost:8104/embedding_models/list_loaded_embedding_models/"

response = requests.get(url)
print(response.json())
```

#### 6. Get Embedding Model Configuration

```python
import requests

url = "http://localhost:8104/embedding_models/embedding_model_config/example_embedding_config"

response = requests.get(url)
print(response.json())
```

#### 7. Delete Embedding Model Configuration

```python
import requests

url = "http://localhost:8104/embedding_models/embedding_model_config/example_embedding_config"

response = requests.delete(url)
print(response.json())
```

#### 8. Execute Method on Embedding Model

```python
import requests

url = "http://localhost:8104/embedding_models/execute_embedding_method/"
data = {
    "model_id": "example_model",
    "method_name": "generate",
    "args": [],
    "kwargs": {}
}

response = requests.post(url, json=data)
print(response.json())
```

#### 9. Get Attribute of Embedding Model

```python
import requests

url = "http://localhost:8104/embedding_models/get_embedding_attribute/"
data = {
    "model_id": "example_model",
    "attribute_name": "attribute_name"
}

response = requests.post(url, json=data)
print(response.json())
```
