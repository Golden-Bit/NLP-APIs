import json
from datetime import datetime

import streamlit as st
import requests
from typing import List, Dict

# Definizione dell'URL dell'API
API_URL = "http://localhost:8102"


def create_or_update_collection_metadata(collection_name: str, metadata: dict) -> dict:
    try:
        response = requests.post(f"{API_URL}/collections/{collection_name}/metadata", json=metadata)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error creating/updating collection metadata: {e}")
        return {}


# Funzione per ottenere i metadati di una collezione specifica
def get_collection_metadata(collection_name: str) -> Dict:
    try:
        response = requests.get(f"{API_URL}/collections/metadata")
        if response.status_code == 200:
            all_metadata = response.json()
            for metadata in all_metadata:
                if metadata['collection_name'] == collection_name:
                    return metadata
            st.warning(f"Metadata not found for collection: {collection_name}")
            return {}
        else:
            st.error(f"Errore durante il recupero dei metadati delle collezioni: {response.status_code}")
            return {}
    except requests.exceptions.RequestException as e:
        st.error(f"Errore durante la connessione all'API: {e}")
        return {}

# Funzione per ottenere la lista dei metadati delle collezioni
def get_collections_metadata() -> list:
    try:
        response = requests.get(f"{API_URL}/collections/metadata")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Errore durante il recupero dei metadati delle collezioni: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Errore durante la connessione all'API: {e}")
        return []

# Funzione per ottenere la lista dei nomi delle collezioni
def fetch_collection_names() -> list:
    metadata_list = get_collections_metadata()
    collection_names = [metadata['collection_name'] for metadata in metadata_list]
    return collection_names

# Funzione per gestire l'invio delle richieste GET
def fetch_data(endpoint: str, params: Dict[str, str] = None) -> Dict:
    try:
        response = requests.get(f"{API_URL}{endpoint}", params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return {}

# Funzione per gestire l'invio delle richieste POST
def post_data(endpoint: str, data: Dict) -> Dict:
    try:
        response = requests.post(f"{API_URL}{endpoint}", json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error posting data: {e}")
        return {}

# Funzione per gestire l'invio delle richieste DELETE
def delete_data(endpoint: str) -> Dict:
    try:
        response = requests.delete(f"{API_URL}{endpoint}")
        response.raise_for_status()
        return {"message": "Document deleted successfully"}
    except requests.exceptions.RequestException as e:
        st.error(f"Error deleting document: {e}")
        return {}

# Funzione per gestire l'invio delle richieste PUT
def put_data(endpoint: str, data: Dict) -> Dict:
    try:
        response = requests.put(f"{API_URL}{endpoint}", json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error updating document: {e}")
        return {}

# UI Streamlit
def main():
    st.title("Document Management App")

    # Sincronizza DB e aggiorna la variabile di sessione
    if "collection_names" not in st.session_state:
        st.session_state.collection_names = fetch_collection_names()

    if st.button("Sincronizza DB"):
        st.session_state.collection_names = fetch_collection_names()
        st.success("Database sincronizzato!")

    # Sezione per ottenere la lista dei metadati delle collezioni
    st.subheader("Get Collections Metadata")
    if st.button("Get Collections Metadata"):
        collections_metadata = get_collections_metadata()
        if collections_metadata:
            st.write("Collections Metadata:")
            for metadata in collections_metadata:
                st.json(metadata)
                st.write("---")

    # Gestione dei metadati delle collezioni
    st.subheader("Create or Update Collection Metadata")

    collection_name = st.text_input("Collection Name")
    description = st.text_area("Description")

    # Generate current date in the required format
    created_at = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

    # Custom metadata input
    custom_metadata = st.text_area("Custom Metadata (JSON format)")

    if st.button("Create/Update Metadata"):
        metadata = {
            "description": description,
            "created_at": created_at,
            "custom_metadata": json.loads(custom_metadata) if custom_metadata else {}
        }
        if collection_name:
            result = create_or_update_collection_metadata(collection_name, metadata)
            if result:
                st.success("Metadata created/updated successfully!")
                st.json(result)
            else:
                st.error("Failed to create/update metadata.")

    # Creazione di un nuovo documento
    st.subheader("Create New Document")
    collection_name_create = st.selectbox("Select Collection (Create Document)", st.session_state.collection_names)
    if collection_name_create:
        # Ottieni i metadati della collezione selezionata
        #collection_metadata = get_collection_metadata(collection_name_create)

        # Mostra i metadati della collezione
        #st.subheader("Collection Metadata")
        #if collection_metadata:
        #    st.json(collection_metadata)
        #else:
        #    st.warning("Metadata not found for the selected collection.")

        page_content = st.text_area("Page Content")
        metadata = st.text_area("Metadata (JSON format)")
        if st.button("Create Document"):
            doc_data = {
                "page_content": page_content,
                "metadata": json.loads(metadata) if metadata else {}
            }
            created_doc = post_data(f"/documents/{collection_name_create}/", doc_data)
            if created_doc:
                st.success("Document created successfully!")
                st.json(created_doc)

    # Lista dei documenti nella collezione selezionata con filtri
    st.subheader("List Documents")
    collection_name_list = st.selectbox("Select Collection (List Documents)", st.session_state.collection_names)
    if collection_name_list:
        prefix = st.text_input("Prefix", "")
        suffix = st.text_input("Suffix", "")
        skip_list = st.number_input("Skip", min_value=0, value=0, key="skip_list")
        limit_list = st.number_input("Limit", min_value=1, value=10, key="limit_list")

        if st.button("Get Documents"):
            documents = fetch_data(f"/documents/{collection_name_list}/", {"prefix": prefix, "suffix": suffix, "skip": skip_list, "limit": limit_list})

            if documents:
                st.write("Total Documents:", len(documents))
                for doc in documents:
                    st.json(doc)
                    st.write("---")

    # Ricerca dei documenti nella collezione con parametri
    st.subheader("Search Documents")
    collection_name_search = st.selectbox("Select Collection (Search Documents)", st.session_state.collection_names)
    if collection_name_search:
        search_query = st.text_input("Search Query")
        skip_search = st.number_input("Skip", min_value=0, value=0, key="skip_search")
        limit_search = st.number_input("Limit", min_value=1, value=10, key="limit_search")

        if st.button("Search"):
            search_params = {
                "query": search_query,
                "skip": skip_search,
                "limit": limit_search
            }
            search_results = fetch_data(f"/search/{collection_name_search}/", search_params)
            if search_results:
                st.write("Search Results:")
                for result in search_results:
                    #st.write("Document ID:", result["metadata"]["doc_store_id"])
                    #st.write("Page Content:", result["page_content"])
                    #st.write("Metadata:", result["metadata"])
                    #st.write("---")
                    st.json(result)
                    st.write("---")

    # Funzionalità di Get Document
    st.subheader("Get Document")
    collection_name_get = st.selectbox("Select Collection (Get Document)", st.session_state.collection_names, key="collection_name_get")
    doc_id_get = st.text_input("Document ID (Get)", key="doc_id_get")
    if st.button("Get Document"):
        if collection_name_get and doc_id_get:
            document = fetch_data(f"/documents/{collection_name_get}/{doc_id_get}")
            if document:
                #st.write("Document ID:", document["metadata"]["doc_store_id"])
                #st.write("Page Content:", document["page_content"])
                #st.write("Metadata:", document["metadata"])
                #st.write("---")
                st.json(document)
                st.write("---")
            else:
                st.warning("Document not found or an error occurred.")

    # Funzionalità di Delete Document
    st.subheader("Delete Document")
    collection_name_delete = st.selectbox("Select Collection (Delete Document)", st.session_state.collection_names, key="collection_name_delete")
    doc_id_delete = st.text_input("Document ID (Delete)", key="doc_id_delete")
    if st.button("Delete Document"):
        if collection_name_delete and doc_id_delete:
            deletion_result = delete_data(f"/documents/{collection_name_delete}/{doc_id_delete}")
            if deletion_result:
                st.success("Document deleted successfully!")
            else:
                st.warning("Document not found or an error occurred.")

    # Funzionalità di Update Document
    st.subheader("Update Document")
    collection_name_update = st.selectbox("Select Collection (Update Document)", st.session_state.collection_names,
                                          key="collection_name_update")
    doc_id_update = st.text_input("Document ID (Update)", key="doc_id_update")

    # Load document for update
    if st.button("Load Document for Update"):
        if collection_name_update and doc_id_update:
            document = fetch_data(f"/documents/{collection_name_update}/{doc_id_update}")
            if document:
                st.session_state['document_to_update'] = document
            else:
                st.warning("Document not found or an error occurred.")

    # Display the form if the document is loaded
    if 'document_to_update' in st.session_state:
        document = st.session_state['document_to_update']
        with st.form(key='update_form'):
            st.write("Document ID:", document["metadata"]["doc_store_id"])
            page_content_update = st.text_area("Updated Page Content", value=document["page_content"],
                                               key="page_content_update")
            metadata_update = st.text_area("Updated Metadata (JSON format)",
                                           value=json.dumps(document["metadata"], indent=2), key="metadata_update")
            submit_button = st.form_submit_button(label="Update Document")

            if submit_button:
                update_data = {
                    "page_content": page_content_update,
                    "metadata": json.loads(metadata_update) if metadata_update else {}
                }
                updated_doc = put_data(f"/documents/{collection_name_update}/{doc_id_update}", update_data)
                if updated_doc:
                    st.success("Document updated successfully!")
                    st.json(updated_doc)
                else:
                    st.warning("Document update failed or an error occurred.")
                del st.session_state['document_to_update']


if __name__ == "__main__":
    main()
