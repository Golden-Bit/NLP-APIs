
import os
from pymongo import MongoClient
from langchain_community.llms import VLLM, VLLMOpenAI
from langchain_openai import OpenAI, ChatOpenAI
from typing import Dict

# MongoDB connection setup
client = MongoClient(os.getenv('mongodb://localhost:27017/'))
db = client['model_config_db']
collection = db['model_configs']

available_models = {
    "OpenAI": OpenAI,
    "ChatOpenAI": ChatOpenAI,
    "VLLM": VLLM,
    "VLLMOpenAI": VLLMOpenAI
}


# ModelManager class definition
class ModelManager:
    """
    Manages loading and offloading of LLM models.
    """

    def __init__(self):
        self.models: Dict[str, object] = {}

    def load_model(self, config_id: str):
        """
        Loads a model based on its configuration ID.
        """
        config = collection.find_one({"_id": config_id})
        if not config:
            raise ValueError("Configuration not found")

        model_id = config['model_id']
        #model_name = config['model_name']
        model_type = config['model_type']
        model_kwargs = config.get('model_kwargs', {})

        self.models[model_id] = available_models[model_type](**model_kwargs)

        #if model_type == 'openai':
        #    self.models[model_id] = OpenAI(model_name=model_name, openai_api_key=os.getenv('OPENAI_API_KEY'),
        #                                   **model_kwargs)
        #elif model_type == 'vllm':
        #    self.models[model_id] = VLLM(model=model_name, trust_remote_code=True, **model_kwargs)
        #elif model_type == 'vllm-openai':
        #    self.models[model_id] = VLLMOpenAI(model=model_name, openai_api_key="EMPTY",
        #                                       **model_kwargs)
        #else:
        #    raise ValueError("Unsupported model type")

    def unload_model(self, model_id: str):
        """
        Unloads a model from memory.
        """
        if model_id in self.models:
            del self.models[model_id]

    def get_model(self, model_id: str):
        """
        Retrieves a loaded model by its model ID.
        """
        return self.models.get(model_id)

    def list_loaded_models(self):
        """
        Lists all currently loaded model IDs.
        """
        return list(self.models.keys())