import json
import os
from pymongo import MongoClient
from pydantic import BaseModel, Field
from typing import Optional, Any
from langchain_core.tools import StructuredTool

# Modelli Pydantic per operazioni MongoDB
class WriteDataModel(BaseModel):
    database_name: Optional[str] = Field(None, title="Database Name", description="Nome del database.")
    collection_name: Optional[str] = Field(None, title="Collection Name", description="Nome della collection.")
    data: str = Field('{"abc": 123}', title="Data", description="Stringa Json dei dati da inserire nella collection.")


class ReadDataModel(BaseModel):
    database_name: Optional[str] = Field(None, title="Database Name", description="Nome del database.")
    collection_name: Optional[str] = Field(None, title="Collection Name", description="Nome della collection.")
    query: Optional[str] = Field(default="{}", title="Query", description="Query per il recupero dei dati.")


class DeleteDataModel(BaseModel):
    database_name: Optional[str] = Field(None, title="Database Name", description="Nome del database.")
    collection_name: Optional[str] = Field(None, title="Collection Name", description="Nome della collection.")
    query: str = Field("{}", title="Query", description="Query per eliminare i dati.")


class UpdateDataModel(BaseModel):
    database_name: Optional[str] = Field(None, title="Database Name", description="Nome del database.")
    collection_name: Optional[str] = Field(None, title="Collection Name", description="Nome della collection.")
    query: str = Field("{}", title="Query", description="Query per aggiornare i dati.")
    new_values: str = Field(..., title="New Values", description="Nuovi valori per l'aggiornamento.")


class MongoDBToolKitManager:
    def __init__(self, connection_string: str, default_database: str = "default_db", default_collection: str = "default_collection"):
        """Inizializza MongoDBToolKit con una connection string e opzionalmente un database e collection di default."""
        self.client = MongoClient(connection_string)
        self.default_database = default_database
        self.default_collection = default_collection

    def set_default_database(self, database_name: str):
        """Imposta il database di default."""
        self.default_database = database_name

    def set_default_collection(self, collection_name: str):
        """Imposta la collection di default."""
        self.default_collection = collection_name

    def _get_collection(self, database_name: Optional[str] = None, collection_name: Optional[str] = None):
        """Recupera la collection Mongo, utilizzando i valori di default se non specificati."""
        db_name = database_name or self.default_database
        coll_name = collection_name or self.default_collection
        db = self.client[db_name]
        return db[coll_name]

    # Metodi per operazioni MongoDB
    def write_to_mongo(self, database_name: str, collection_name: str, data: str):
        """Inserisce un documento nella collection specificata o in quella di default."""
        collection = self._get_collection(database_name=database_name,
                                          collection_name=collection_name)

        result = collection.insert_one(json.loads(data))
        return f"Document inserted with id: {str(result.inserted_id)}"

    def read_from_mongo(self, database_name: str, collection_name: str, query: Any):
        """Legge documenti dalla collection specificata o da quella di default."""
        collection = self._get_collection(database_name=database_name, collection_name=collection_name)
        documents = list(collection.find(json.loads(query)))
        return str(documents)

    def delete_from_mongo(self, database_name: str, collection_name: str, query: Any):
        """Elimina documenti dalla collection specificata o da quella di default."""
        collection = self._get_collection(database_name=database_name, collection_name=collection_name)
        result = collection.delete_one(json.loads(query))
        return f"Documents deleted: {result.deleted_count}"

    def update_in_mongo(self, database_name: str, collection_name: str, query: Any, new_values: str):
        """Aggiorna documenti nella collection specificata o in quella di default."""
        collection = self._get_collection(database_name=database_name, collection_name=collection_name)
        result = collection.update_one(json.loads(query), {"$set": json.loads(new_values)})
        return f"Documents updated: {result.modified_count}"

    def get_tools(self):
        """Restituisce una lista degli strumenti configurati usando StructuredTool."""
        return [
            StructuredTool(
                name="write_to_mongo",
                func=self.write_to_mongo,
                description="Use this tool to write data to MongoDB. Requires database name, collection name, and the data to insert.",
                args_schema=WriteDataModel
            ),
            StructuredTool(
                name="read_from_mongo",
                func=self.read_from_mongo,
                description="Use this tool to read data from MongoDB. Requires database name, collection name, and a query to match documents.",
                args_schema=ReadDataModel
            ),
            StructuredTool(
                name="delete_from_mongo",
                func=self.delete_from_mongo,
                description="Use this tool to delete data from MongoDB. Requires database name, collection name, and a query to match documents.",
                args_schema=DeleteDataModel
            ),
            StructuredTool(
                name="update_in_mongo",
                func=self.update_in_mongo,
                description="Use this tool to update data in MongoDB. Requires database name, collection name, a query, and the new values.",
                args_schema=UpdateDataModel
            )
        ]


# Esempio di utilizzo
#if __name__ == "__main__":
    # Inizializza MongoDBToolKit con una connection string
#    mongo_toolkit = MongoDBToolKitManager(connection_string="mongodb://localhost:27017", default_database="sans7-database_0")

    # Definisci i dati da inserire
#    write_data = WriteDataModel(collection_name="example_collection", data={"name": "Alice", "age": 30})

    # Inserisci il documento nella collection
#    result = mongo_toolkit.write_to_mongo(write_data)
#    print(result)

    # Leggi il documento inserito
#    read_data = ReadDataModel(collection_name="example_collection", query={"name": "Alice"})
#    documents = mongo_toolkit.read_from_mongo(read_data)
#    print(documents)
