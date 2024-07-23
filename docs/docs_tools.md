# API Documentation for Tool Management System

## Overview

This API provides endpoints for configuring, managing, and executing tools. The API supports creating, retrieving, updating, and deleting tool configurations, as well as instantiating tools and executing methods on these instances.

## Base URL

```
http://localhost:8108
```

## Endpoints

### 1. Add Tool Configuration

#### `POST /tools/add_tool_config/`

Adds a new tool configuration to the database.

**Request Body:**
- `config_id` (str, required): The unique ID of the tool configuration.
- `tool_class` (str, required): The class of the tool (e.g., 'OpenAITool').
- `tool_kwargs` (dict, optional): Additional keyword arguments for tool initialization.

**Response:**
- 200 OK: Returns a success message with the configuration ID of the newly created tool configuration.

**Example Request:**

```bash
curl -X POST "http://localhost:8108/tools/add_tool_config/" -H "Content-Type: application/json" -d '{
  "config_id": "example_tool_config",
  "tool_class": "OpenAITool",
  "tool_kwargs": {
    "api_key": "your_api_key"
  }
}'
```

**Example Response:**

```json
{
  "config_id": "example_tool_config"
}
```

### 2. Update Tool Configuration

#### `PUT /tools/update_tool_config/{config_id}`

Updates an existing tool configuration in the database.

**Path Parameters:**
- `config_id` (str, required): The ID of the tool configuration to update.

**Request Body:**
- `config_id` (str, required): The unique ID of the tool configuration.
- `tool_class` (str, required): The class of the tool (e.g., 'OpenAITool').
- `tool_kwargs` (dict, optional): Additional keyword arguments for tool initialization.

**Response:**
- 200 OK: Returns a success message with the configuration ID of the updated tool configuration.

**Example Request:**

```bash
curl -X PUT "http://localhost:8108/tools/update_tool_config/example_tool_config" -H "Content-Type: application/json" -d '{
  "config_id": "example_tool_config",
  "tool_class": "OpenAITool",
  "tool_kwargs": {
    "api_key": "your_new_api_key"
  }
}'
```

**Example Response:**

```json
{
  "config_id": "example_tool_config"
}
```

### 3. Delete Tool Configuration

#### `DELETE /tools/delete_tool_config/{config_id}`

Deletes a tool configuration from the database.

**Path Parameters:**
- `config_id` (str, required): The ID of the tool configuration to delete.

**Response:**
- 200 OK: Returns a success message upon successful deletion.

**Example Request:**

```bash
curl -X DELETE "http://localhost:8108/tools/delete_tool_config/example_tool_config"
```

**Example Response:**

```json
{
  "detail": "Configuration deleted successfully"
}
```

### 4. Get Tool Configuration

#### `GET /tools/get_tool_config/{config_id}`

Retrieves a tool configuration from the database.

**Path Parameters:**
- `config_id` (str, required): The ID of the tool configuration to retrieve.

**Response:**
- 200 OK: Returns the tool configuration details.

**Example Request:**

```bash
curl -X GET "http://localhost:8108/tools/get_tool_config/example_tool_config"
```

**Example Response:**

```json
{
  "config_id": "example_tool_config",
  "tool_class": "OpenAITool",
  "tool_kwargs": {
    "api_key": "your_api_key"
  }
}
```

### 5. List Tool Configurations

#### `GET /tools/list_tool_configs/`

Lists all tool configurations from the database.

**Response:**
- 200 OK: Returns a list of tool configurations.

**Example Request:**

```bash
curl -X GET "http://localhost:8108/tools/list_tool_configs/"
```

**Example Response:**

```json
[
  {
    "config_id": "example_tool_config",
    "tool_class": "OpenAITool",
    "tool_kwargs": {
      "api_key": "your_api_key"
    }
  }
]
```

### 6. Instantiate Tool

#### `POST /tools/instantiate_tool/`

Instantiates a tool based on its configuration.

**Request Body:**
- `config_id` (str, required): The unique ID of the tool configuration.

**Response:**
- 200 OK: Returns the instantiated tool with its ID.

**Example Request:**

```bash
curl -X POST "http://localhost:8108/tools/instantiate_tool/" -H "Content-Type: application/json" -d '{
  "config_id": "example_tool_config"
}'
```

**Example Response:**

```json
{
  "tool_id": "123e4567-e89b-12d3-a456-426614174000"
}
```

### 7. Remove Tool Instance

#### `POST /tools/remove_tool_instance/`

Removes a tool instance.

**Request Body:**
- `tool_id` (str, required): The unique ID of the tool instance.

**Response:**
- 200 OK: Returns a success message upon successful removal.

**Example Request:**

```bash
curl -X POST "http://localhost:8108/tools/remove_tool_instance/" -H "Content-Type: application/json" -d '{
  "tool_id": "123e4567-e89b-12d3-a456-426614174000"
}'
```

**Example Response:**

```json
{
  "detail": "Tool instance removed successfully"
}
```

### 8. Get Tool Instance

#### `GET /tools/get_tool_instance/{tool_id}`

Gets the JSON representation of a tool instance.

**Path Parameters:**
- `tool_id` (str, required): The unique ID of the tool instance.

**Response:**
- 200 OK: Returns the JSON representation of the tool instance.

**Example Request:**

```bash
curl -X GET "http://localhost:8108/tools/get_tool_instance/123e4567-e89b-12d3-a456-426614174000"
```

**Example Response:**

```json
{
  "tool_id": "123e4567-e89b-12d3-a456-426614174000",
  "tool_class": "OpenAITool",
  "tool_kwargs": {
    "api_key": "your_api_key"
  }
}
```

### 9. List Tool Instances

#### `GET /tools/list_tool_instances/`

Lists all tool instance IDs.

**Response:**
- 200 OK: Returns a list of tool instance IDs.

**Example Request:**

```bash
curl -X GET "http://localhost:8108/tools/list_tool_instances/"
```

**Example Response:**

```json
[
  "123e4567-e89b-12d3-a456-426614174000",
  "987e6543-b21c-45d2-a456-789012345678"
]
```

### 10. Execute Method on Tool Instance

#### `POST /tools/execute_tool_method/`

Executes a method on a tool instance.

**Request Body:**
- `tool_id` (str, required): The unique ID of the tool instance.
- `method` (str, required): The name of the method to execute.
- `args` (list, optional): The positional arguments for the method (if any).
- `kwargs` (dict, optional): The keyword arguments for the method (if any).

**Response:**
- 200 OK: Returns the result of the method execution.

**Example Request:**

```bash
curl -X POST "http://localhost:8108/tools/execute_tool_method/" -H "Content-Type: application/json" -d '{
  "tool_id": "123e4567-e89b-12d3-a456-426614174000",
  "method": "method_name",
  "args": [],
  "kwargs": {
    "param1": "value1",
    "param2": "value2"
  }
}'
```

**Example Response:**

```json
{
  "result": "Method executed successfully"
}
```

### 11. Get Attribute of Tool Instance

#### `POST /tools/get_tool_attribute/`

Gets an attribute of a tool instance.

**Request Body:**
- `tool_id` (str, required): The unique ID of the tool instance.
- `attribute` (str, required): The name of the attribute to retrieve.

**Response:**
- 200 OK: Returns the value of the specified attribute.

**Example Request:**

```bash
curl -X POST "http://localhost:8108/tools/get_tool_attribute/" -H "Content-Type: application/json" -d '{
  "tool_id": "123e4567-e89b-12d3-a456-426614174000",
  "attribute": "attribute_name"
}'
```

**Example Response:**

```json
{
  "attribute": "Attribute value"
}
```

## Models

**ToolConfig**
- `config_id` (str): The unique ID of the tool configuration.
- `tool_class` (str): The class of the tool (e.g., 'OpenAITool').
- `tool_kwargs` (dict): Additional keyword arguments for tool initialization.

**ToolRequest**
- `config_id` (str): The unique ID of the tool configuration.
- `tool_id` (str, optional): The

 unique ID of the tool instance.

**ExecuteMethodRequest**
- `tool_id` (str): The unique ID of the tool instance.
- `method` (str): The name of the method to execute.
- `args` (list): The positional arguments for the method (if any).
- `kwargs` (dict): The keyword arguments for the method (if any).

**GetAttributeRequest**
- `tool_id` (str): The unique ID of the tool instance.
- `attribute` (str): The name of the attribute to retrieve.

## Usage

To use the API, you can make HTTP requests to the provided endpoints using tools like `curl`, Postman, or any HTTP client library in your preferred programming language.

### Usage Example with Python

Below is a Python example using the `requests` library to interact with the API:

#### 1. Add Tool Configuration

```python
import requests

url = "http://localhost:8108/tools/add_tool_config/"
data = {
    "config_id": "example_tool_config",
    "tool_class": "OpenAITool",
    "tool_kwargs": {
        "api_key": "your_api_key"
    }
}

response = requests.post(url, json=data)
print(response.json())
```

#### 2. Update Tool Configuration

```python
import requests

url = "http://localhost:8108/tools/update_tool_config/example_tool_config"
data = {
    "config_id": "example_tool_config",
    "tool_class": "OpenAITool",
    "tool_kwargs": {
        "api_key": "your_new_api_key"
    }
}

response = requests.put(url, json=data)
print(response.json())
```

#### 3. Delete Tool Configuration

```python
import requests

url = "http://localhost:8108/tools/delete_tool_config/example_tool_config"

response = requests.delete(url)
print(response.json())
```

#### 4. Get Tool Configuration

```python
import requests

url = "http://localhost:8108/tools/get_tool_config/example_tool_config"

response = requests.get(url)
print(response.json())
```

#### 5. List Tool Configurations

```python
import requests

url = "http://localhost:8108/tools/list_tool_configs/"

response = requests.get(url)
print(response.json())
```

#### 6. Instantiate Tool

```python
import requests

url = "http://localhost:8108/tools/instantiate_tool/"
data = {
    "config_id": "example_tool_config"
}

response = requests.post(url, json=data)
print(response.json())
```

#### 7. Remove Tool Instance

```python
import requests

url = "http://localhost:8108/tools/remove_tool_instance/"
data = {
    "tool_id": "123e4567-e89b-12d3-a456-426614174000"
}

response = requests.post(url, json=data)
print(response.json())
```

#### 8. Get Tool Instance

```python
import requests

url = "http://localhost:8108/tools/get_tool_instance/123e4567-e89b-12d3-a456-426614174000"

response = requests.get(url)
print(response.json())
```

#### 9. List Tool Instances

```python
import requests

url = "http://localhost:8108/tools/list_tool_instances/"

response = requests.get(url)
print(response.json())
```

#### 10. Execute Method on Tool Instance

```python
import requests

url = "http://localhost:8108/tools/execute_tool_method/"
data = {
    "tool_id": "123e4567-e89b-12d3-a456-426614174000",
    "method": "method_name",
    "args": [],
    "kwargs": {
        "param1": "value1",
        "param2": "value2"
    }
}

response = requests.post(url, json=data)
print(response.json())
```

#### 11. Get Attribute of Tool Instance

```python
import requests

url = "http://localhost:8108/tools/get_tool_attribute/"
data = {
    "tool_id": "123e4567-e89b-12d3-a456-426614174000",
    "attribute": "attribute_name"
}

response = requests.post(url, json=data)
print(response.json())
```
