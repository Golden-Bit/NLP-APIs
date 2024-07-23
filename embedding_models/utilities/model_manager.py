from typing import Dict, Any
from pymongo import MongoClient
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings


class EmbeddingModelManager:
    def __init__(self, db_collection):
        self.models = {}
        self.collection = db_collection
        self.available_models = {
            "HuggingFaceEmbeddings": HuggingFaceEmbeddings,
            "OpenAIEmbeddings": OpenAIEmbeddings,
            # Add other models as needed
        }

    def load_model(self, config_id: str):
        config = self.collection.find_one({"_id": config_id})
        if not config:
            raise ValueError("Configuration not found")

        model_id = config["model_id"]
        model_class = config["model_class"]
        model_kwargs = config["model_kwargs"]

        if model_id in self.models:
            raise ValueError("Model with this model_id is already loaded")

        if model_class not in self.available_models:
            raise ValueError(f"Model class {model_class} not supported")

        model_class_instance = self.available_models[model_class]
        model_instance = model_class_instance(**model_kwargs)
        self.models[model_id] = model_instance

    def unload_model(self, model_id: str):
        if model_id in self.models:
            del self.models[model_id]
        else:
            raise ValueError("Model with this model_id is not loaded")

    def get_model(self, model_id: str):
        if model_id in self.models:
            return self.models[model_id]
        else:
            raise ValueError("Model with this model_id is not loaded")

    def list_loaded_models(self):
        return list(self.models.keys())
