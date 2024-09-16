from typing import Any

from pymongo import MongoClient
import json
from langchain.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_history_aware_retriever, create_retrieval_chain

# Step 1: Connessione al database MongoDB e recupero dati
def get_chain(llm: Any, retriever: Any):
    # Variabili costanti per il nome del database e le collection
    DATABASE_NAME = 'sans7-database_0'
    COLLECTION_LIST = ['tasks',
                       'documents',
                       'contacts'
                       'products'
                       'appointments'
                       'taskLists'
                       'Services'
                       'folders'
                       ]  # Sostituisci con le collection reali

    # Connessione al database MongoDB locale
    client = MongoClient('mongodb://localhost:27017/')
    db = client[DATABASE_NAME]

    # Inizializziamo un dizionario per contenere i dati
    data = {}

    # Recuperiamo i dati da ogni collection nella lista
    for collection_name in COLLECTION_LIST:
        collection = db[collection_name]
        documents = list(collection.find())  # Recupera tutti i documenti
        # Convertiamo i documenti in JSON e li aggiungiamo al dizionario
        data[collection_name] = json.dumps(documents, default=str)
        print(data[collection_name])
    # Chiudi la connessione al database
    client.close()

    # Step 2: Creazione del messaggio di sistema che include i dati del database
    system_message = "Answer the user's questions based on the below database content:\n\n"
    for collection_name, collection_data in data.items():
        system_message += f"Collection: {collection_name}\nData: {collection_data}\n\n"

    # Prompt per generare la query di ricerca
    search_prompt = ChatPromptTemplate.from_messages(
        [
            ("placeholder", "{chat_history}"),
            ("user", "{input}"),
            (
                "user",
                "Given the above conversation, generate a search query to look up to get information relevant to the conversation",
            ),
        ]
    )

    # Creiamo la catena di recupero storia-aware
    retriever_chain = create_history_aware_retriever(llm, retriever, search_prompt)

    # Prompt per rispondere basato sui dati recuperati
    response_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                system_message,  # Usa il messaggio di sistema che include i dati del database
            ),
            ("placeholder", "{chat_history}"),
            ("user", "{input}"),
        ]
    )

    # Creiamo la catena di documenti
    document_chain = create_stuff_documents_chain(llm, prompt=response_prompt)

    # Restituiamo la catena finale che combina il retriever e i documenti
    return create_retrieval_chain(retriever_chain, document_chain)

# Placeholder per llm e retriever, che saranno definiti nel contesto reale
# llm = ...  # Inserisci il modello LLM che stai usando
# retriever = ...  # Inserisci il retriever

# Esempio di utilizzo della funzione get_chain:
# chain = get_chain(llm, retriever)
# input_chat = ...  # Inserisci input di test
# result = chain.run(input_chat)
# print(result)

