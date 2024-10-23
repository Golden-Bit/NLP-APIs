from typing import Dict, Any

from pymongo import MongoClient
from langchain.chains import RetrievalQA

# TODO:
#  - [ ] to implement 'get_object' methods
#from data_stores.api import router as router_1
#from document_loaders.api import router as router_2
#from document_stores.api import router as router_3
#from document_transformers.api import router as router_4
#from embedding_models.api import router as router_5, embedding_manager

# TODO:
#  - [ ] to implement VectorStoreManager class
from chains.chain_scripts import qa_chain, agent_with_tools
from chains.chain_scripts import mongodb_chain
from chains.chain_scripts import dataloader_chain
#from chains.chain_scripts import tmp as qa_chain
from llms.api import model_manager, load_model
from prompts.api import prompt_manager
from tools.api import tool_manager
from vector_stores.api import vector_stores, load_vector_store


# Functions for getting components by ID


def get_tool_component(tool_id: str):
    tool = tool_manager.get_tool(tool_id)
    return tool


def get_prompt_component(config_id: str):
    # Function to get a prompt component by ID

    prompt = prompt_manager.get_prompt(config_id)

    return prompt


def get_llm_component(model_id: str):
    # Function to get an LLM component by ID

    if not model_manager.get_model(model_id):
        try:
            load_model(config_id=f"{model_id}_config")
        except Exception as e:
            print(e)

    llm_model = model_manager.get_model(model_id)

    return llm_model


def get_vectorstore_component(store_id: str):
    # Function to get a vectorstore component by ID

    if not vector_stores.get(store_id):
        try:
            load_vector_store(config_id=f"{store_id}_config")
        except Exception as e:
            print(e)

    vector_store = vector_stores[store_id]

    return vector_store


class ChainManager:

    available_chains: Dict[str, Any] = {
        "qa_chain": qa_chain,
        "mongodb_chain": mongodb_chain,
        "dataloader_chain": dataloader_chain,
        "agent_with_tools": agent_with_tools
    }

    def __init__(self, db_collection):
        self.chains = {}
        self.collection = db_collection

    def configure_chain(self, chain_config: dict):
        config_id = chain_config['config_id']
        if self.collection.find_one({"_id": config_id}):
            raise ValueError("Configuration ID already exists")

        chain_config["_id"] = config_id
        self.collection.insert_one(chain_config)
        return {"config_id": config_id}

    def update_chain_config(self, config_id: str, chain_config: dict):
        if not self.collection.find_one({"_id": config_id}):
            raise ValueError("Configuration not found")

        self.collection.update_one({"_id": config_id}, {"$set": chain_config})
        return {"config_id": config_id}

    def delete_chain_config(self, config_id: str):
        result = self.collection.delete_one({"_id": config_id})
        if result.deleted_count == 0:
            raise ValueError("Configuration not found")
        return {"detail": "Configuration deleted successfully"}

    def load_chain(self, config_id: str):
        config = self.collection.find_one({"_id": config_id})
        if not config:
            raise ValueError("Configuration not found")

        chain_type = config["chain_type"]
        chain_id = config["chain_id"]
        if chain_id in self.chains:
            raise ValueError("Chain already loaded")

        if chain_type == "qa_chain":
            #prompt = get_prompt_component(config["prompt_id"])
            llm = get_llm_component(config["llm_id"])
            vectorstore = get_vectorstore_component(config["vectorstore_id"])
            retriever = vectorstore.as_retriever(**{"search_type": "similarity", "search_kwargs": {"k": 10}})

            chain = self.available_chains[chain_type].get_chain(llm=llm,
                                                                retriever=retriever)

            self.chains[chain_id] = chain

        elif chain_type == "agent_with_tools":
            llm = get_llm_component(config["llm_id"])
            chain = self.available_chains[chain_type].get_chain(llm=llm)
            self.chains[chain_id] = chain

        return {"message": "Chain loaded successfully", "chain_id": chain_id}

    def unload_chain(self, chain_id: str):
        if chain_id not in self.chains:
            raise ValueError("Chain not found")

        del self.chains[chain_id]
        return {"message": "Chain unloaded successfully"}

    def list_loaded_chains(self):
        return list(self.chains.keys())

    def list_chain_configs(self):
        configs = list(
            self.collection.find({}, {"_id": 1, "chain_id": 1, "prompt_id": 1, "llm_id": 1, "vectorstore_id": 1}))
        return configs

    def get_chain_config(self, config_id: str):
        config = self.collection.find_one({"_id": config_id})
        if not config:
            raise ValueError("Configuration not found")
        return config

    def get_chain(self, chain_id: str):
        if chain_id not in self.chains:
            raise ValueError("Chain not found")
        return self.chains[chain_id]
