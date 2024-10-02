# API Documentation for Chain Management System

## Overview

This API provides endpoints for configuring, managing, and executing chains. The API supports creating, retrieving, updating, and deleting chain configurations, as well as loading and unloading chains into memory and executing them.

## Base URL

```
http://localhost:8109
```

## Endpoints

### 1. Configure Chain

#### `POST /chains/configure_chain/`

Configures a new chain and stores its configuration.

**Request Body:**
- `config_id` (str, required): The unique ID of the chain configuration.
- `chain_id` (str, required): The unique ID of the chain.
- `prompt_id` (str, required): The unique ID of the prompt.
- `llm_id` (str, required): The unique ID of the LLM.
- `vectorstore_id` (str, required): The unique ID of the vectorstore.

**Response:**
- 200 OK: Returns the configuration ID of the newly created chain configuration.

**Example Request:**

```bash
curl -X POST "http://localhost:8109/chains/configure_chain/" -H "Content-Type: application/json" -d '{
  "config_id": "example_chain_config",
  "chain_id": "example_chain",
  "prompt_id": "example_prompt",
  "llm_id": "example_llm",
  "vectorstore_id": "example_vectorstore"
}'
```

**Example Response:**

```json
{
  "config_id": "example_chain_config"
}
```

### 2. Update Chain Configuration

#### `PUT /chains/update_chain_config/{config_id}`

Updates an existing chain configuration.

**Path Parameters:**
- `config_id` (str, required): The ID of the configuration to update.

**Request Body:**
- `config_id` (str, required): The unique ID of the chain configuration.
- `chain_id` (str, required): The unique ID of the chain.
- `prompt_id` (str, required): The unique ID of the prompt.
- `llm_id` (str, required): The unique ID of the LLM.
- `vectorstore_id` (str, required): The unique ID of the vectorstore.

**Response:**
- 200 OK: Returns the configuration ID of the updated chain configuration.

**Example Request:**

```bash
curl -X PUT "http://localhost:8109/chains/update_chain_config/example_chain_config" -H "Content-Type: application/json" -d '{
  "config_id": "example_chain_config",
  "chain_id": "example_chain",
  "prompt_id": "example_prompt",
  "llm_id": "example_llm",
  "vectorstore_id": "example_vectorstore"
}'
```

**Example Response:**

```json
{
  "config_id": "example_chain_config"
}
```

### 3. Delete Chain Configuration

#### `DELETE /chains/delete_chain_config/{config_id}`

Deletes a specific chain configuration.

**Path Parameters:**
- `config_id` (str, required): The unique ID of the chain configuration to delete.

**Response:**
- 200 OK: Returns a success message upon successful deletion.

**Example Request:**

```bash
curl -X DELETE "http://localhost:8109/chains/delete_chain_config/example_chain_config"
```

**Example Response:**

```json
{
  "detail": "Configuration deleted successfully"
}
```

### 4. Load Chain

#### `POST /chains/load_chain/{config_id}`

Loads a chain into memory based on its configuration ID.

**Path Parameters:**
- `config_id` (str, required): The unique ID of the chain configuration to load.

**Response:**
- 200 OK: Returns a success message upon successful loading.

**Example Request:**

```bash
curl -X POST "http://localhost:8109/chains/load_chain/example_chain_config"
```

**Example Response:**

```json
{
  "message": "Chain loaded successfully"
}
```

### 5. Unload Chain

#### `POST /chains/unload_chain/{chain_id}`

Unloads a chain from memory.

**Path Parameters:**
- `chain_id` (str, required): The unique ID of the chain to unload.

**Response:**
- 200 OK: Returns a success message upon successful unloading.

**Example Request:**

```bash
curl -X POST "http://localhost:8109/chains/unload_chain/example_chain"
```

**Example Response:**

```json
{
  "message": "Chain unloaded successfully"
}
```

### 6. List Loaded Chains

#### `GET /chains/list_loaded_chains/`

Lists all currently loaded chains.

**Response:**
- 200 OK: Returns a list of loaded chain IDs.

**Example Request:**

```bash
curl -X GET "http://localhost:8109/chains/list_loaded_chains/"
```

**Example Response:**

```json
[
  "example_chain"
]
```

### 7. List Chain Configurations

#### `GET /chains/list_chain_configs/`

Lists all chain configurations stored in MongoDB.

**Response:**
- 200 OK: Returns a list of chain configurations.

**Example Request:**

```bash
curl -X GET "http://localhost:8109/chains/list_chain_configs/"
```

**Example Response:**

```json
[
  {
    "config_id": "example_chain_config",
    "chain_id": "example_chain",
    "prompt_id": "example_prompt",
    "llm_id": "example_llm",
    "vectorstore_id": "example_vectorstore"
  }
]
```

### 8. Get Chain Configuration

#### `GET /chains/chain_config/{config_id}`

Retrieves a specific chain configuration.

**Path Parameters:**
- `config_id` (str, required): The unique ID of the chain configuration to retrieve.

**Response:**
- 200 OK: Returns the chain configuration details.

**Example Request:**

```bash
curl -X GET "http://localhost:8109/chains/chain_config/example_chain_config"
```

**Example Response:**

```json
{
  "config_id": "example_chain_config",
  "chain_id": "example_chain",
  "prompt_id": "example_prompt",
  "llm_id": "example_llm",
  "vectorstore_id": "example_vectorstore"
}
```

### 9. Execute Chain

#### `POST /chains/execute_chain/`

Executes a specific chain.

**Request Body:**
- `chain_id` (str, required): The unique ID of the chain to execute.
- `query` (str, required): The input query for the chain.

**Response:**
- 200 OK: Returns the result of the chain execution.

**Example Request:**

```bash
curl -X POST "http://localhost:8109/chains/execute_chain/" -H "Content-Type: application/json" -d '{
  "chain_id": "example_chain",
  "query": "What are the approaches to Task Decomposition?"
}'
```

**Example Response:**

```json
{
  "result": "The approaches to Task Decomposition are..."
}
```

## Models

**ChainConfigRequest**
- `config_id` (str): The unique ID of the chain configuration.
- `chain_id` (str): The unique ID of the chain.
- `prompt_id` (str): The unique ID of the prompt.
- `llm_id` (str): The unique ID of the LLM.
- `vectorstore_id` (str): The unique ID of the vectorstore.

**ExecuteChainRequest**
- `chain_id` (str): The unique ID of the chain to execute.
- `query` (str): The input query for the chain.

## Usage

To use the API, you can make HTTP requests to the provided endpoints using tools like `curl`, Postman, or any HTTP client library in your preferred programming language.

### Usage Example with Python

Below is a Python example using the `requests` library to interact with the API:

#### 1. Configure Chain

```python
import requests

url = "http://localhost:8109/chains/configure_chain/"
data = {
    "config_id": "example_chain_config",
    "chain_id": "example_chain",
    "prompt_id": "example_prompt",
    "llm_id": "example_llm",
    "vectorstore_id": "example_vectorstore"
}

response = requests.post(url, json=data)
print(response.json())
```

#### 2. Update Chain Configuration

```python
import requests

url = "http://localhost:8109/chains/update_chain_config/example_chain_config"
data = {
    "config_id": "example_chain_config",
    "chain_id": "example_chain",
    "prompt_id": "example_prompt",
    "llm_id": "example_llm",
    "vectorstore_id": "example_vectorstore"
}

response = requests.put(url, json=data)
print(response.json())
```

#### 3. Delete Chain Configuration

```python
import requests

url = "http://localhost:8109/chains/delete_chain_config/example_chain_config"

response = requests.delete(url)
print(response.json())
```

#### 4. Load Chain

```python
import requests

url = "http://localhost:8109/chains/load_chain/example_chain_config"

response = requests.post(url)
print(response.json())
```

#### 5. Unload Chain

```python
import requests

url = "http://localhost:8109/chains/unload_chain/example_chain"

response = requests.post(url)
print(response.json())
```

#### 6. List Loaded Chains

```python
import requests

url = "

http://localhost:8109/chains/list_loaded_chains/"

response = requests.get(url)
print(response.json())
```

#### 7. List Chain Configurations

```python
import requests

url = "http://localhost:8109/chains/list_chain_configs/"

response = requests.get(url)
print(response.json())
```

#### 8. Get Chain Configuration

```python
import requests

url = "http://localhost:8109/chains/chain_config/example_chain_config"

response = requests.get(url)
print(response.json())
```

#### 9. Execute Chain

```python
import requests

url = "http://localhost:8109/chains/execute_chain/"
data = {
    "chain_id": "example_chain",
    "query": "What are the approaches to Task Decomposition?"
}

response = requests.post(url, json=data)
print(response.json())
```

