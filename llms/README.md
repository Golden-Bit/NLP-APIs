# API Documentation for LLM Management System

## Overview

This API provides endpoints for configuring, managing, and performing inference with Large Language Models (LLMs). The API supports creating, retrieving, updating, and deleting model configurations, as well as loading and unloading models into memory and performing inference.

## Base URL

```
http://localhost:8105
```

## Endpoints

### 1. Configure Model

#### `POST /llm/configure_model/`

Configures a new model and stores its configuration.

**Request Body:**
- `model_id` (str, required): The unique ID of the model.
- `model_name` (str, required): The name of the model.
- `model_type` (str, required): The type of the model (e.g., 'openai', 'vllm').
- `model_kwargs` (dict, optional): Additional keyword arguments for model initialization.

**Response:**
- 200 OK: Returns the configuration ID of the newly created model configuration.

**Example Request:**

```bash
curl -X POST "http://localhost:8000/llm/configure_model/" -H "Content-Type: application/json" -d '{
  "model_id": "example_model",
  "model_name": "gpt-3",
  "model_type": "openai",
  "model_kwargs": {
    "temperature": 0.7
  }
}'
```

**Example Response:**

```json
{
  "config_id": "abcd1234-efgh-5678-ijkl-9012mnop3456"
}
```

### 2. Load Model

#### `POST /llm/load_model/{config_id}`

Loads a model based on its configuration ID.

**Path Parameters:**
- `config_id` (str, required): The configuration ID of the model to load.

**Response:**
- 200 OK: Returns a success message.

**Example Request:**

```bash
curl -X POST "http://localhost:8000/llm/load_model/abcd1234-efgh-5678-ijkl-9012mnop3456"
```

**Example Response:**

```json
{
  "message": "Model loaded successfully"
}
```

### 3. Unload Model

#### `POST /llm/unload_model/{model_id}`

Unloads a model from memory.

**Path Parameters:**
- `model_id` (str, required): The ID of the model to unload.

**Response:**
- 200 OK: Returns a success message.

**Example Request:**

```bash
curl -X POST "http://localhost:8000/llm/unload_model/example_model"
```

**Example Response:**

```json
{
  "message": "Model unloaded successfully"
}
```

### 4. Perform Inference

#### `POST /llm/inference/`

Performs inference using a loaded model.

**Request Body:**
- `model_id` (str, required): The ID of the model to use for inference.
- `prompt` (str, required): The input prompt for the model.
- `inference_kwargs` (dict, optional): Additional keyword arguments for inference.

**Response:**
- 200 OK: Returns the inference response.

**Example Request:**

```bash
curl -X POST "http://localhost:8000/llm/inference/" -H "Content-Type: application/json" -d '{
  "model_id": "example_model",
  "prompt": "What is the capital of France?",
  "inference_kwargs": {
    "max_tokens": 50
  }
}'
```

**Example Response:**

```json
{
  "response": "The capital of France is Paris."
}
```

### 5. List Model Configurations

#### `GET /llm/configurations/`

Lists all stored model configurations.

**Response:**
- 200 OK: Returns a list of all model configurations.

**Example Request:**

```bash
curl -X GET "http://localhost:8000/llm/configurations/"
```

**Example Response:**

```json
[
  {
    "config_id": "abcd1234-efgh-5678-ijkl-9012mnop3456",
    "model_id": "example_model",
    "model_name": "gpt-3",
    "model_type": "openai",
    "model_kwargs": {
      "temperature": 0.7
    }
  }
]
```

### 6. Get Model Configuration

#### `GET /llm/configuration/{config_id}`

Retrieves a specific model configuration.

**Path Parameters:**
- `config_id` (str, required): The configuration ID to retrieve.

**Response:**
- 200 OK: Returns the model configuration.

**Example Request:**

```bash
curl -X GET "http://localhost:8000/llm/configuration/abcd1234-efgh-5678-ijkl-9012mnop3456"
```

**Example Response:**

```json
{
  "config_id": "abcd1234-efgh-5678-ijkl-9012mnop3456",
  "model_id": "example_model",
  "model_name": "gpt-3",
  "model_type": "openai",
  "model_kwargs": {
    "temperature": 0.7
  }
}
```

### 7. Delete Model Configuration

#### `DELETE /llm/configuration/{config_id}`

Deletes a specific model configuration.

**Path Parameters:**
- `config_id` (str, required): The configuration ID to delete.

**Response:**
- 200 OK: Returns a success message.

**Example Request:**

```bash
curl -X DELETE "http://localhost:8000/llm/configuration/abcd1234-efgh-5678-ijkl-9012mnop3456"
```

**Example Response:**

```json
{
  "detail": "Configuration deleted successfully"
}
```

### 8. List Loaded Models

#### `GET /llm/loaded_models/`

Lists all currently loaded models.

**Response:**
- 200 OK: Returns a list of loaded model IDs.

**Example Request:**

```bash
curl -X GET "http://localhost:8000/llm/loaded_models/"
```

**Example Response:**

```json
[
  "example_model"
]
```
## Models

**ModelConfigRequest**
- `model_id` (str): The unique ID of the model.
- `model_name` (str): The name of the model.
- `model_type` (str): The type of the model (e.g., 'openai', 'vllm').
- `model_kwargs` (dict): Additional keyword arguments for model initialization.

**InferenceRequest**
- `model_id` (str): The ID of the model to use for inference.
- `prompt` (str): The input prompt for the model.
- `inference_kwargs` (dict): Additional keyword arguments for inference.

## Usage

To use the API, you can make HTTP requests to the provided endpoints using tools like `curl`, Postman, or any HTTP client library in your preferred programming language.

### Usage Example with Python

Below is a Python example using the `requests` library to interact with the API:

#### 1. Configure Model

```python
import requests

url = "http://localhost:8000/llm/configure_model/"
data = {
    "model_id": "example_model",
    "model_name": "gpt-3",
    "model_type": "openai",
    "model_kwargs": {
        "temperature": 0.7
    }
}

response = requests.post(url, json=data)
print(response.json())
```

#### 2. Load Model

```python
import requests

url = "http://localhost:8000/llm/load_model/abcd1234-efgh-5678-ijkl-9012mnop3456"

response = requests.post(url)
print(response.json())
```

#### 3. Unload Model

```python
import requests

url = "http://localhost:8000/llm/unload_model/example_model"

response = requests.post(url)
print(response.json())
```

#### 4. Perform Inference

```python
import requests

url = "http://localhost:8000/llm/inference/"
data = {
    "model_id": "example_model",
    "prompt": "What is the capital of France?",
    "inference_kwargs": {
        "max_tokens": 50
    }
}

response = requests.post(url, json=data)
print(response.json())
```

#### 5. List Model Configurations

```python
import requests

url = "http://localhost:8000/llm/configurations/"

response = requests.get(url)
print(response.json())
```

#### 6. Get Model Configuration

```python
import requests

url = "http://localhost:8000/llm/configuration/abcd1234-efgh-5678-ijkl-9012mnop3456"

response = requests.get(url)
print(response.json())
```

#### 7. Delete Model Configuration

```python
import requests

url = "http://localhost:8000/llm/configuration/abcd1234-efgh-5678-ijkl-9012mnop3456"

response = requests.delete(url)
print(response.json())
```

#### 8. List Loaded Models

```python
import requests

url = "http://localhost:8000/llm/loaded_models/"

response = requests.get(url)
print(response.json())
```
