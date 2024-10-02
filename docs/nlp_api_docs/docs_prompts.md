# API Documentation for Prompt Management System

## Overview

This API provides endpoints for configuring, managing, and executing prompts and chat prompts. The API supports creating, retrieving, updating, and deleting prompt configurations, as well as loading and executing methods on these configurations.

## Base URL

```
http://localhost:8107
```

## Endpoints

### 1. Add Prompt Configuration

#### `POST /prompts/add_prompt_config/`

Adds a new prompt configuration to the database.

**Request Body:**
- `config_id` (str, required): The unique ID of the prompt configuration.
- `template` (str, required): The template string for the prompt.
- `type` (str, required): The type of the prompt (e.g., 'string').
- `variables` (list of str, required): The variables used in the prompt template.

**Response:**
- 200 OK: Returns a success message with the configuration ID of the newly created prompt configuration.

**Example Request:**

```bash
curl -X POST "http://localhost:8107/prompts/add_prompt_config/" -H "Content-Type: application/json" -d '{
  "config_id": "example_prompt_config",
  "template": "Tell me a {adjective} joke about {content}.",
  "type": "string",
  "variables": ["adjective", "content"]
}'
```

**Example Response:**

```json
{
  "config_id": "example_prompt_config"
}
```

### 2. Add Chat Prompt Configuration

#### `POST /prompts/add_chat_prompt_config/`

Adds a new chat prompt configuration to the database.

**Request Body:**
- `config_id` (str, required): The unique ID of the chat prompt configuration.
- `messages` (list of dict, required): The list of messages in the chat prompt.
- `variables` (list of str, required): The variables used in the chat prompt messages.

**Response:**
- 200 OK: Returns a success message with the configuration ID of the newly created chat prompt configuration.

**Example Request:**

```bash
curl -X POST "http://localhost:8107/prompts/add_chat_prompt_config/" -H "Content-Type: application/json" -d '{
  "config_id": "example_chat_prompt_config",
  "messages": [
    {"role": "system", "content": "You are a helpful AI bot. Your name is {name}."},
    {"role": "human", "content": "Hello, how are you doing?"},
    {"role": "ai", "content": "I'm doing well, thanks!"},
    {"role": "human", "content": "{user_input}"}
  ],
  "variables": ["name", "user_input"]
}'
```

**Example Response:**

```json
{
  "config_id": "example_chat_prompt_config"
}
```

### 3. Update Prompt Configuration

#### `PUT /prompts/update_prompt_config/{config_id}`

Updates an existing prompt configuration in the database.

**Path Parameters:**
- `config_id` (str, required): The ID of the prompt configuration to update.

**Request Body:**
- `config_id` (str, required): The unique ID of the prompt configuration.
- `template` (str, required): The template string for the prompt.
- `type` (str, required): The type of the prompt (e.g., 'string').
- `variables` (list of str, required): The variables used in the prompt template.

**Response:**
- 200 OK: Returns a success message with the configuration ID of the updated prompt configuration.

**Example Request:**

```bash
curl -X PUT "http://localhost:8107/prompts/update_prompt_config/example_prompt_config" -H "Content-Type: application/json" -d '{
  "config_id": "example_prompt_config",
  "template": "Tell me a {adjective} story about {content}.",
  "type": "string",
  "variables": ["adjective", "content"]
}'
```

**Example Response:**

```json
{
  "config_id": "example_prompt_config"
}
```

### 4. Update Chat Prompt Configuration

#### `PUT /prompts/update_chat_prompt_config/{config_id}`

Updates an existing chat prompt configuration in the database.

**Path Parameters:**
- `config_id` (str, required): The ID of the chat prompt configuration to update.

**Request Body:**
- `config_id` (str, required): The unique ID of the chat prompt configuration.
- `messages` (list of dict, required): The list of messages in the chat prompt.
- `variables` (list of str, required): The variables used in the chat prompt messages.

**Response:**
- 200 OK: Returns a success message with the configuration ID of the updated chat prompt configuration.

**Example Request:**

```bash
curl -X PUT "http://localhost:8107/prompts/update_chat_prompt_config/example_chat_prompt_config" -H "Content-Type: application/json" -d '{
  "config_id": "example_chat_prompt_config",
  "messages": [
    {"role": "system", "content": "You are a helpful AI bot. Your name is {name}."},
    {"role": "human", "content": "Hello, how are you doing?"},
    {"role": "ai", "content": "I'm doing well, thanks!"},
    {"role": "human", "content": "{user_input}"}
  ],
  "variables": ["name", "user_input"]
}'
```

**Example Response:**

```json
{
  "config_id": "example_chat_prompt_config"
}
```

### 5. Delete Prompt Configuration

#### `DELETE /prompts/delete_prompt_config/{config_id}`

Deletes a prompt configuration from the database.

**Path Parameters:**
- `config_id` (str, required): The ID of the prompt configuration to delete.

**Response:**
- 200 OK: Returns a success message upon successful deletion.

**Example Request:**

```bash
curl -X DELETE "http://localhost:8107/prompts/delete_prompt_config/example_prompt_config"
```

**Example Response:**

```json
{
  "detail": "Configuration deleted successfully"
}
```

### 6. Delete Chat Prompt Configuration

#### `DELETE /prompts/delete_chat_prompt_config/{config_id}`

Deletes a chat prompt configuration from the database.

**Path Parameters:**
- `config_id` (str, required): The ID of the chat prompt configuration to delete.

**Response:**
- 200 OK: Returns a success message upon successful deletion.

**Example Request:**

```bash
curl -X DELETE "http://localhost:8107/prompts/delete_chat_prompt_config/example_chat_prompt_config"
```

**Example Response:**

```json
{
  "detail": "Configuration deleted successfully"
}
```

### 7. Get Prompt Configuration

#### `GET /prompts/get_prompt_config/{config_id}`

Retrieves a prompt configuration from the database.

**Path Parameters:**
- `config_id` (str, required): The ID of the prompt configuration to retrieve.

**Response:**
- 200 OK: Returns the prompt configuration details.

**Example Request:**

```bash
curl -X GET "http://localhost:8107/prompts/get_prompt_config/example_prompt_config"
```

**Example Response:**

```json
{
  "config_id": "example_prompt_config",
  "template": "Tell me a {adjective} joke about {content}.",
  "type": "string",
  "variables": ["adjective", "content"]
}
```

### 8. Get Chat Prompt Configuration

#### `GET /prompts/get_chat_prompt_config/{config_id}`

Retrieves a chat prompt configuration from the database.

**Path Parameters:**
- `config_id` (str, required): The ID of the chat prompt configuration to retrieve.

**Response:**
- 200 OK: Returns the chat prompt configuration details.

**Example Request:**

```bash
curl -X GET "http://localhost:8107/prompts/get_chat_prompt_config/example_chat_prompt_config"
```

**Example Response:**

```json
{
  "config_id": "example_chat_prompt_config",
  "messages": [
    {"role": "system", "content": "You are a helpful AI bot. Your name is {name}."},
    {"role": "human", "content": "Hello, how are you doing?"},
    {"role": "ai", "content": "I'm doing well, thanks!"},
    {"role": "human", "content": "{user_input}"}
  ],
  "variables": ["name", "user_input"]
}
```

### 9. Instantiate Prompt

#### `POST /prompts/get_prompt/`

Instantiates a prompt based on its configuration and provided variables.

**Request Body:**
- `config_id` (str, required): The unique ID of the prompt configuration.
- `variables` (dict of str to Any, required): The variables to format the prompt template.
- `is_partial` (bool, optional): Whether to perform partial formatting.
- `is_format` (bool, optional): Whether to perform full formatting.

**Response:**
- 200 OK: Returns the instantiated prompt.

**Example Request:**

```bash
curl -X POST "http://localhost:8107/prompts/get_prompt/" -H "Content-Type: application/json" -d '{
  "config_id": "example_prompt_config",
  "variables": {"adjective": "funny", "content": "chickens"},
  "is_partial": false,
  "is_format": true
}'
```

**Example Response:**

```json
{
  "prompt": "Tell

 me a funny joke about chickens."
}
```

### 10. Instantiate Chat Prompt

#### `POST /prompts/get_chat_prompt/`

Instantiates a chat prompt based on its configuration and provided variables.

**Request Body:**
- `config_id` (str, required): The unique ID of the chat prompt configuration.
- `variables` (dict of str to Any, required): The variables to format the chat prompt template.
- `is_partial` (bool, optional): Whether to perform partial formatting.
- `is_format` (bool, optional): Whether to perform full formatting.

**Response:**
- 200 OK: Returns the instantiated chat prompt.

**Example Request:**

```bash
curl -X POST "http://localhost:8107/prompts/get_chat_prompt/" -H "Content-Type: application/json" -d '{
  "config_id": "example_chat_prompt_config",
  "variables": {"name": "Bob", "user_input": "What is your name?"},
  "is_partial": false,
  "is_format": true
}'
```

**Example Response:**

```json
{
  "chat_prompt": [
    {"role": "system", "content": "You are a helpful AI bot. Your name is Bob."},
    {"role": "human", "content": "Hello, how are you doing?"},
    {"role": "ai", "content": "I'm doing well, thanks!"},
    {"role": "human", "content": "What is your name?"}
  ]
}
```

### 11. List Prompt Configurations

#### `GET /prompts/list_prompt_configs/`

Lists all prompt configurations from the database.

**Response:**
- 200 OK: Returns a list of prompt configurations.

**Example Request:**

```bash
curl -X GET "http://localhost:8107/prompts/list_prompt_configs/"
```

**Example Response:**

```json
[
  {
    "config_id": "example_prompt_config",
    "template": "Tell me a {adjective} joke about {content}.",
    "type": "string",
    "variables": ["adjective", "content"]
  }
]
```

### 12. List Chat Prompt Configurations

#### `GET /prompts/list_chat_prompt_configs/`

Lists all chat prompt configurations from the database.

**Response:**
- 200 OK: Returns a list of chat prompt configurations.

**Example Request:**

```bash
curl -X GET "http://localhost:8107/prompts/list_chat_prompt_configs/"
```

**Example Response:**

```json
[
  {
    "config_id": "example_chat_prompt_config",
    "messages": [
      {"role": "system", "content": "You are a helpful AI bot. Your name is {name}."},
      {"role": "human", "content": "Hello, how are you doing?"},
      {"role": "ai", "content": "I'm doing well, thanks!"},
      {"role": "human", "content": "{user_input}"}
    ],
    "variables": ["name", "user_input"]
  }
]
```

### 13. Execute Method on Prompt

#### `POST /prompts/execute_prompt_method/`

Executes a method on a loaded prompt instance.

**Request Body:**
- `config_id` (str, required): The unique ID of the prompt configuration.
- `method_name` (str, required): The name of the method to call on the prompt.
- `args` (list, optional): The positional arguments for the method (if any).
- `kwargs` (dict, optional): The keyword arguments for the method (if any).

**Response:**
- 200 OK: Returns the result of the method execution.

**Example Request:**

```bash
curl -X POST "http://localhost:8107/prompts/execute_prompt_method/" -H "Content-Type: application/json" -d '{
  "config_id": "example_prompt_config",
  "method_name": "some_method",
  "args": [],
  "kwargs": {"param1": "value1", "param2": "value2"}
}'
```

**Example Response:**

```json
{
  "result": "Method executed successfully"
}
```

### 14. Get Attribute of Prompt

#### `POST /prompts/get_prompt_attribute/`

Gets an attribute of a loaded prompt instance.

**Request Body:**
- `config_id` (str, required): The unique ID of the prompt configuration.
- `attribute_name` (str, required): The name of the attribute to retrieve.

**Response:**
- 200 OK: Returns the value of the specified attribute.

**Example Request:**

```bash
curl -X POST "http://localhost:8107/prompts/get_prompt_attribute/" -H "Content-Type: application/json" -d '{
  "config_id": "example_prompt_config",
  "attribute_name": "attribute_name"
}'
```

**Example Response:**

```json
{
  "attribute": "Attribute value"
}
```

### 15. Execute Method on Chat Prompt

#### `POST /prompts/execute_chat_prompt_method/`

Executes a method on a loaded chat prompt instance.

**Request Body:**
- `config_id` (str, required): The unique ID of the chat prompt configuration.
- `method_name` (str, required): The name of the method to call on the chat prompt.
- `args` (list, optional): The positional arguments for the method (if any).
- `kwargs` (dict, optional): The keyword arguments for the method (if any).

**Response:**
- 200 OK: Returns the result of the method execution.

**Example Request:**

```bash
curl -X POST "http://localhost:8107/prompts/execute_chat_prompt_method/" -H "Content-Type: application/json" -d '{
  "config_id": "example_chat_prompt_config",
  "method_name": "some_method",
  "args": [],
  "kwargs": {"param1": "value1", "param2": "value2"}
}'
```

**Example Response:**

```json
{
  "result": "Method executed successfully"
}
```

### 16. Get Attribute of Chat Prompt

#### `POST /prompts/get_chat_prompt_attribute/`

Gets an attribute of a loaded chat prompt instance.

**Request Body:**
- `config_id` (str, required): The unique ID of the chat prompt configuration.
- `attribute_name` (str, required): The name of the attribute to retrieve.

**Response:**
- 200 OK: Returns the value of the specified attribute.

**Example Request:**

```bash
curl -X POST "http://localhost:8107/prompts/get_chat_prompt_attribute/" -H "Content-Type: application/json" -d '{
  "config_id": "example_chat_prompt_config",
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

**PromptConfig**
- `config_id` (str): The unique ID of the prompt configuration.
- `template` (str): The template string for the prompt.
- `type` (str): The type of the prompt (e.g., 'string').
- `variables` (list of str): The variables used in the prompt template.

**ChatPromptConfig**
- `config_id` (str): The unique ID of the chat prompt configuration.
- `messages` (list of dict): The list of messages in the chat prompt.
- `variables` (list of str): The variables used in the chat prompt messages.

**PromptRequest**
- `config_id` (str): The unique ID of the prompt configuration.
- `variables` (dict of str to Any): The variables to format the prompt template.
- `is_partial` (bool): Whether to perform partial formatting.
- `is_format` (bool): Whether to perform full formatting.

**ChatPromptRequest**
- `config_id` (str): The unique ID of the chat prompt configuration.
- `variables` (dict of str to Any): The variables to format the chat prompt template.
- `is_partial` (bool): Whether to perform partial formatting.
- `is_format` (bool): Whether to perform full formatting.

**ExecutePromptMethodRequest**
- `config_id` (str): The unique ID of the prompt configuration.
- `method_name` (str): The name of the method to call on the prompt.
- `args` (list): The positional arguments for the method (if any).
- `kwargs` (dict): The keyword arguments for the method (if any).

**ExecuteChatPromptMethodRequest**
- `config_id` (str): The unique ID of the chat prompt configuration.
- `method_name` (str): The name of the method to call on the chat prompt.
- `args` (list): The positional arguments for the method (if any).
- `kwargs` (dict): The keyword arguments for the method (if any).

**GetPromptAttributeRequest**
- `config_id` (str): The unique ID of the prompt configuration.
- `attribute_name` (str): The name of the attribute to retrieve.

**GetChatPromptAttributeRequest**
- `config_id` (str): The unique ID of the chat prompt configuration.
- `attribute_name` (str): The name of the attribute to retrieve.

## Usage

To use the API, you can make HTTP requests to the provided endpoints using tools like `curl`, Postman, or any HTTP client library in your preferred programming language.

### Usage Example with Python

Below is a Python example using the `requests` library to interact with the API:

#### 1. Add Prompt Configuration

```python
import requests

url =

 "http://localhost:8107/prompts/add_prompt_config/"
data = {
    "config_id": "example_prompt_config",
    "template": "Tell me a {adjective} joke about {content}.",
    "type": "string",
    "variables": ["adjective", "content"]
}

response = requests.post(url, json=data)
print(response.json())
```

#### 2. Add Chat Prompt Configuration

```python
import requests

url = "http://localhost:8107/prompts/add_chat_prompt_config/"
data = {
    "config_id": "example_chat_prompt_config",
    "messages": [
        {"role": "system", "content": "You are a helpful AI bot. Your name is {name}."},
        {"role": "human", "content": "Hello, how are you doing?"},
        {"role": "ai", "content": "I'm doing well, thanks!"},
        {"role": "human", "content": "{user_input}"}
    ],
    "variables": ["name", "user_input"]
}

response = requests.post(url, json=data)
print(response.json())
```

#### 3. Update Prompt Configuration

```python
import requests

url = "http://localhost:8107/prompts/update_prompt_config/example_prompt_config"
data = {
    "config_id": "example_prompt_config",
    "template": "Tell me a {adjective} story about {content}.",
    "type": "string",
    "variables": ["adjective", "content"]
}

response = requests.put(url, json=data)
print(response.json())
```

#### 4. Update Chat Prompt Configuration

```python
import requests

url = "http://localhost:8107/prompts/update_chat_prompt_config/example_chat_prompt_config"
data = {
    "config_id": "example_chat_prompt_config",
    "messages": [
        {"role": "system", "content": "You are a helpful AI bot. Your name is {name}."},
        {"role": "human", "content": "Hello, how are you doing?"},
        {"role": "ai", "content": "I'm doing well, thanks!"},
        {"role": "human", "content": "{user_input}"}
    ],
    "variables": ["name", "user_input"]
}

response = requests.put(url, json=data)
print(response.json())
```

#### 5. Delete Prompt Configuration

```python
import requests

url = "http://localhost:8107/prompts/delete_prompt_config/example_prompt_config"

response = requests.delete(url)
print(response.json())
```

#### 6. Delete Chat Prompt Configuration

```python
import requests

url = "http://localhost:8107/prompts/delete_chat_prompt_config/example_chat_prompt_config"

response = requests.delete(url)
print(response.json())
```

#### 7. Get Prompt Configuration

```python
import requests

url = "http://localhost:8107/prompts/get_prompt_config/example_prompt_config"

response = requests.get(url)
print(response.json())
```

#### 8. Get Chat Prompt Configuration

```python
import requests

url = "http://localhost:8107/prompts/get_chat_prompt_config/example_chat_prompt_config"

response = requests.get(url)
print(response.json())
```

#### 9. Instantiate Prompt

```python
import requests

url = "http://localhost:8107/prompts/get_prompt/"
data = {
    "config_id": "example_prompt_config",
    "variables": {"adjective": "funny", "content": "chickens"},
    "is_partial": false,
    "is_format": true
}

response = requests.post(url, json=data)
print(response.json())
```

#### 10. Instantiate Chat Prompt

```python
import requests

url = "http://localhost:8107/prompts/get_chat_prompt/"
data = {
    "config_id": "example_chat_prompt_config",
    "variables": {"name": "Bob", "user_input": "What is your name?"},
    "is_partial": false,
    "is_format": true
}

response = requests.post(url, json=data)
print(response.json())
```

#### 11. List Prompt Configurations

```python
import requests

url = "http://localhost:8107/prompts/list_prompt_configs/"

response = requests.get(url)
print(response.json())
```

#### 12. List Chat Prompt Configurations

```python
import requests

url = "http://localhost:8107/prompts/list_chat_prompt_configs/"

response = requests.get(url)
print(response.json())
```

#### 13. Execute Method on Prompt

```python
import requests

url = "http://localhost:8107/prompts/execute_prompt_method/"
data = {
    "config_id": "example_prompt_config",
    "method_name": "some_method",
    "args": [],
    "kwargs": {"param1": "value1", "param2": "value2"}
}

response = requests.post(url, json=data)
print(response.json())
```

#### 14. Get Attribute of Prompt

```python
import requests

url = "http://localhost:8107/prompts/get_prompt_attribute/"
data = {
    "config_id": "example_prompt_config",
    "attribute_name": "attribute_name"
}

response = requests.post(url, json=data)
print(response.json())
```

#### 15. Execute Method on Chat Prompt

```python
import requests

url = "http://localhost:8107/prompts/execute_chat_prompt_method/"
data = {
    "config_id": "example_chat_prompt_config",
    "method_name": "some_method",
    "args": [],
    "kwargs": {"param1": "value1", "param2": "value2"}
}

response = requests.post(url, json=data)
print(response.json())
```

#### 16. Get Attribute of Chat Prompt

```python
import requests

url = "http://localhost:8107/prompts/get_chat_prompt_attribute/"
data = {
    "config_id": "example_chat_prompt_config",
    "attribute_name": "attribute_name"
}

response = requests.post(url, json=data)
print(response.json())
```
