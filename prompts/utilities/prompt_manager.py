import os
from pymongo import MongoClient
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, ChatMessagePromptTemplate
from pydantic import BaseModel, Field
from typing import Dict, Any, List

# Configurazione della connessione a MongoDB
MONGO_CONNECTION_STRING = os.getenv('MONGO_CONNECTION_STRING', 'localhost')
client = MongoClient(MONGO_CONNECTION_STRING)
db = client['prompt_db']
collection = db['prompt_configs']


class PromptConfig(BaseModel):
    """
    Class representing a prompt configuration.

    Attributes:
        config_id (str): Unique ID of the prompt configuration.
        template (str): Template string for the prompt.
        type (str): Type of the prompt, either 'string' or 'chat'.
        variables (List[str]): List of variables used in the prompt template.
    """
    config_id: str = Field(..., example="example_prompt_config", title="Config ID",
                           description="The unique ID of the prompt configuration.")
    template: str = Field(..., example="Tell me a {adjective} joke about {content}.", title="Template",
                          description="The template string for the prompt.")
    type: str = Field("string", example="string", title="Type",
                      description="The type of the prompt, either 'string' or 'chat'.")
    variables: List[str] = Field(..., example=["adjective", "content"], title="Variables",
                                 description="The variables used in the prompt template.")


class ChatPromptConfig(BaseModel):
    """
    Class representing a chat prompt configuration.

    Attributes:
        config_id (str): Unique ID of the chat prompt configuration.
        messages (List[Dict[str, str]]): List of messages for the chat prompt.
        variables (List[str]): List of variables used in the chat prompt template.
    """
    config_id: str = Field(..., example="example_chat_prompt_config", title="Config ID",
                           description="The unique ID of the chat prompt configuration.")
    messages: List[Dict[str, str]] = Field(..., example=[
        {"role": "system", "content": "You are a helpful AI bot. Your name is {name}."},
        {"role": "human", "content": "Hello, how are you doing?"},
        {"role": "ai", "content": "I'm doing well, thanks!"},
        {"role": "human", "content": "{user_input}"}
    ], title="Messages", description="The list of messages for the chat prompt.")
    type: str = Field("chat", example="chat", title="Type",
                      description="The type of the prompt, either 'string' or 'chat'.")
    variables: List[str] = Field(..., example=["name", "user_input"], title="Variables",
                                 description="The variables used in the chat prompt template.")


class PromptManager:
    """
    Manager class for handling prompt configurations stored in MongoDB.

    Methods:
        add_prompt_config: Adds a new prompt configuration to the database.
        update_prompt_config: Updates an existing prompt configuration.
        delete_prompt_config: Deletes a prompt configuration.
        get_prompt_config: Retrieves a prompt configuration.
        add_chat_prompt_config: Adds a new chat prompt configuration to the database.
        update_chat_prompt_config: Updates an existing chat prompt configuration.
        delete_chat_prompt_config: Deletes a chat prompt configuration.
        get_chat_prompt_config: Retrieves a chat prompt configuration.
        instantiate_prompt: Instantiates a prompt based on its configuration and variables.
        instantiate_chat_prompt: Instantiates a chat prompt based on its configuration and variables.
    """

    def __init__(self, db_collection):
        """
        Initializes the PromptManager with the given MongoDB collection.

        Args:
            db_collection: The MongoDB collection to store and retrieve prompt configurations.
        """
        self.collection = db_collection

    def add_prompt_config(self, prompt_config: PromptConfig):
        """
        Adds a new prompt configuration to the database.

        Args:
            prompt_config (PromptConfig): The prompt configuration to add.

        Returns:
            dict: A message indicating success.
        """
        config = prompt_config.dict()
        if self.collection.find_one({"_id": config['config_id']}):
            raise ValueError("Prompt Config ID already exists")
        config['_id'] = config['config_id']
        self.collection.insert_one(config)
        return {"message": "Prompt Config added successfully"}

    def update_prompt_config(self, config_id: str, prompt_config: PromptConfig):
        """
        Updates an existing prompt configuration in the database.

        Args:
            config_id (str): The ID of the prompt configuration to update.
            prompt_config (PromptConfig): The updated prompt configuration.

        Returns:
            dict: A message indicating success.
        """
        config = prompt_config.dict()
        if not self.collection.find_one({"_id": config_id}):
            raise ValueError("Prompt Config ID does not exist")
        self.collection.update_one({"_id": config_id}, {"$set": config})
        return {"message": "Prompt Config updated successfully"}

    def delete_prompt_config(self, config_id: str):
        """
        Deletes a prompt configuration from the database.

        Args:
            config_id (str): The ID of the prompt configuration to delete.

        Returns:
            dict: A message indicating success.
        """
        result = self.collection.delete_one({"_id": config_id})
        if result.deleted_count == 0:
            raise ValueError("Prompt Config ID does not exist")
        return {"message": "Prompt Config deleted successfully"}

    def get_prompt_config(self, config_id: str):
        """
        Retrieves a prompt configuration from the database.

        Args:
            config_id (str): The ID of the prompt configuration to retrieve.

        Returns:
            dict: The prompt configuration.
        """
        config = self.collection.find_one({"_id": config_id})
        if not config:
            raise ValueError("Prompt Config ID does not exist")
        return config

    def add_chat_prompt_config(self, chat_prompt_config: ChatPromptConfig):
        """
        Adds a new chat prompt configuration to the database.

        Args:
            chat_prompt_config (ChatPromptConfig): The chat prompt configuration to add.

        Returns:
            dict: A message indicating success.
        """
        config = chat_prompt_config.dict()
        if self.collection.find_one({"_id": config['config_id']}):
            raise ValueError("Chat Prompt Config ID already exists")
        config['_id'] = config['config_id']
        self.collection.insert_one(config)
        return {"message": "Chat Prompt Config added successfully"}

    def update_chat_prompt_config(self, config_id: str, chat_prompt_config: ChatPromptConfig):
        """
        Updates an existing chat prompt configuration in the database.

        Args:
            config_id (str): The ID of the chat prompt configuration to update.
            chat_prompt_config (ChatPromptConfig): The updated chat prompt configuration.

        Returns:
            dict: A message indicating success.
        """
        config = chat_prompt_config.dict()
        if not self.collection.find_one({"_id": config_id}):
            raise ValueError("Chat Prompt Config ID does not exist")
        self.collection.update_one({"_id": config_id}, {"$set": config})
        return {"message": "Chat Prompt Config updated successfully"}

    def delete_chat_prompt_config(self, config_id: str):
        """
        Deletes a chat prompt configuration from the database.

        Args:
            config_id (str): The ID of the chat prompt configuration to delete.

        Returns:
            dict: A message indicating success.
        """
        result = self.collection.delete_one({"_id": config_id})
        if result.deleted_count == 0:
            raise ValueError("Chat Prompt Config ID does not exist")
        return {"message": "Chat Prompt Config deleted successfully"}

    def get_chat_prompt_config(self, config_id: str):
        """
        Retrieves a chat prompt configuration from the database.

        Args:
            config_id (str): The ID of the chat prompt configuration to retrieve.

        Returns:
            dict: The chat prompt configuration.
        """
        config = self.collection.find_one({"_id": config_id})
        if not config:
            raise ValueError("Chat Prompt Config ID does not exist")
        return config

    def get_prompt(self, config_id: str, variables: Dict[str, Any], is_partial: bool = False, is_format: bool = False):
        """
        Instantiates a prompt based on its configuration and provided variables.

        Args:
            config_id (str): The ID of the prompt configuration to use.
            variables (Dict[str, Any]): The variables to format the prompt template.
            is_partial (bool): Whether to perform partial formatting.
            is_format (bool): Whether to fully format the prompt.

        Returns:
            str or PromptTemplate: The formatted prompt string or the prompt template instance.
        """
        config = self.get_prompt_config(config_id)
        if config['type'] == 'string':
            prompt_template = PromptTemplate.from_template(config['template'])
            if is_partial:
                return prompt_template.partial(**variables)
            elif is_format:
                return prompt_template.format(**variables)
            else:
                return prompt_template
        else:
            raise ValueError("Invalid prompt type")

    def get_chat_prompt(self, config_id: str, variables: Dict[str, Any], is_partial: bool = False,
                        is_format: bool = False):
        """
        Instantiates a chat prompt based on its configuration and provided variables.

        Args:
            config_id (str): The ID of the chat prompt configuration to use.
            variables (Dict[str, Any]): The variables to format the chat prompt template.
            is_partial (bool): Whether to perform partial formatting.
            is_format (bool): Whether to fully format the chat prompt.

        Returns:
            List[Dict[str, str]] or ChatPromptTemplate: The formatted chat messages or the chat prompt template instance.
        """

        config = self.get_chat_prompt_config(config_id)
        chat_messages = []
        for msg in config['messages']:
            chat_message_template = ChatMessagePromptTemplate.from_template(
                role=msg['role'], template=msg['content']
            )
            chat_messages.append(chat_message_template)

        chat_prompt_template = ChatPromptTemplate.from_messages(chat_messages)

        if is_partial:
            return chat_prompt_template.partial(**variables)
        elif is_format:
            return chat_prompt_template.format(**variables)
        else:
            return chat_prompt_template

    def list_prompt_configs(self):
        """
        Lists all prompt configurations from the database.

        Returns:
            List[Dict[str, Any]]: A list of all prompt configurations.
        """
        configs = self.collection.find({"type": "string"})
        return [config for config in configs]

    def list_chat_prompt_configs(self):
        """
        Lists all chat prompt configurations from the database.

        Returns:
            List[Dict[str, Any]]: A list of all chat prompt configurations.
        """
        configs = self.collection.find({"type": "chat"})
        return [config for config in configs]


# Esempi di utilizzo
if __name__ == "__main__":
    manager = PromptManager(collection)

    # Aggiungi una nuova configurazione di prompt
    new_prompt_config = PromptConfig(
        config_id="example_prompt_config_4",
        template="Tell me a {adjective} joke about {content}.",
        type="string",
        variables=["adjective", "content"]
    )
    print(manager.add_prompt_config(new_prompt_config))

    # Aggiungi una nuova configurazione di chat prompt
    new_chat_prompt_config = ChatPromptConfig(
        config_id="example_chat_prompt_config_4",
        messages=[
            {"role": "system", "content": "You are a helpful AI bot. Your name is {name}."},
            {"role": "human", "content": "Hello, how are you doing?"},
            {"role": "ai", "content": "I'm doing well, thanks!"},
            {"role": "human", "content": "{user_input}"}
        ],
        variables=["name", "user_input"]
    )
    print(manager.add_chat_prompt_config(new_chat_prompt_config))

    # Instanzia un prompt
    variables = {"adjective": "funny", "content": "chickens"}
    print(manager.get_prompt("example_prompt_config_4", variables))

    # Instanzia un chat prompt
    chat_variables = {"name": "Bob", "user_input": "What is your name?"}
    print(manager.get_chat_prompt("example_chat_prompt_config_4", chat_variables))

    # Aggiorna una configurazione di prompt
    updated_prompt_config = PromptConfig(
        config_id="example_prompt_config_4",
        template="Tell me a {adjective} story about {content}.",
        type="string",
        variables=["adjective", "content"]
    )
    print(manager.update_prompt_config("example_prompt_config_4", updated_prompt_config))

    # Elimina una configurazione di prompt
    print(manager.delete_prompt_config("example_prompt_config_4"))

    # Elimina una configurazione di chat prompt
    print(manager.delete_chat_prompt_config("example_chat_prompt_config_4"))
