import json
import streamlit as st
import requests
from typing import List, Dict, Any, Union

# Definizione dell'URL dell'API
API_URL = "http://localhost:8105"

# Funzione per ottenere le configurazioni dei vector store
def fetch_vector_store_configs() -> List[Dict[str, Any]]:
    try:
        response = requests.get(f"{API_URL}/vector_store/configurations")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching vector store configurations: {e}")
        return []

# Funzione per ottenere gli ID dei vector store caricati in memoria
def fetch_loaded_store_ids() -> List[str]:
    try:
        response = requests.get(f"{API_URL}/vector_store/loaded_store_ids")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching loaded store IDs: {e}")
        return []

# Funzione per inviare richieste GET
def fetch_data(endpoint: str, params: Dict[str, str] = None) -> Dict:
    try:
        response = requests.get(f"{API_URL}{endpoint}", params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return {}

# Funzione per inviare richieste POST
def post_data(endpoint: str, data: Union[Dict, List[Dict]]) -> Dict:
    try:
        response = requests.post(f"{API_URL}{endpoint}", json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error posting data: {e}")
        return {}

# Funzione per inviare richieste DELETE
def delete_data(endpoint: str) -> Dict:
    try:
        response = requests.delete(f"{API_URL}{endpoint}")
        response.raise_for_status()
        return {"message": "Success"}
    except requests.exceptions.RequestException as e:
        st.error(f"Error deleting data: {e}")
        return {}

# Funzione per inviare richieste PUT
def put_data(endpoint: str, data: Dict) -> Dict:
    try:
        response = requests.put(f"{API_URL}{endpoint}", json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error updating data: {e}")
        return {}

# Funzione per aggiungere documenti da un document store
def add_documents_from_document_store(store_id: str, document_collection: str) -> Dict:
    try:
        response = requests.post(f"{API_URL}/vector_store/add_documents_from_store/{store_id}", params={"document_collection": document_collection})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error adding documents from document store: {e}")
        return {}

# Funzione per filtrare documenti
def filter_documents(store_id: str, filter_criteria: Dict[str, Any], skip: int = 0, limit: int = 10) -> List[Dict]:
    try:
        response = requests.post(f"{API_URL}/vector_store/filter/{store_id}", json={"filter": filter_criteria, "skip": skip, "limit": limit})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error filtering documents: {e}")
        return []

# Funzione per aggiornare documenti
def update_document(store_id: str, document_id: str, updated_document: Dict) -> Dict:
    try:
        response = requests.put(f"{API_URL}/vector_store/documents/{store_id}/{document_id}", json=updated_document)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error updating document: {e}")
        return {}

# Funzione per cancellare documenti
def delete_document(store_id: str, document_id: str) -> Dict:
    try:
        response = requests.delete(f"{API_URL}/vector_store/documents/{store_id}", json={"ids": [document_id]})
        response.raise_for_status()
        return {"message": "Success"}
    except requests.exceptions.RequestException as e:
        st.error(f"Error deleting document: {e}")
        return {}

# UI Streamlit
def main():
    st.title("Vector Store Management App")

    # Sincronizza DB e aggiorna le variabili di sessione
    if "vector_store_configs" not in st.session_state:
        st.session_state.vector_store_configs = fetch_vector_store_configs()

    if st.button("Sincronizza"):
        st.session_state.vector_store_configs = fetch_vector_store_configs()
        st.session_state.loaded_store_ids = fetch_loaded_store_ids()
        st.success("Database sincronizzato!")

    st.subheader("List Vector Store Configurations")
    if st.button("Show Vector Store Configurations"):
        if st.session_state.vector_store_configs:
            for config in st.session_state.vector_store_configs:
                st.write(f"Config ID: {config['config_id']}")
                st.json(config)
                st.write("---")

    # Creazione di un nuovo vector store
    st.subheader("Create New Vector Store")
    config_id_create = st.text_input("Config ID (leave blank to auto-generate)", key="config_id_create")
    store_id_create = st.text_input("Store ID (leave blank to auto-generate)", key="store_id_create")
    vector_store_class = st.selectbox("Select Vector Store Class", ["Chroma", "ElasticsearchStore", "ElasticVectorSearch", "FAISS"])
    params = st.text_area("Vector Store Params (JSON format)")
    embeddings_model_class = st.selectbox("Select Embeddings Model Class", ["None", "OpenAIEmbeddings"])
    embeddings_params = st.text_area("Embeddings Params (JSON format)")
    description = st.text_area("Description")
    custom_metadata = st.text_area("Custom Metadata (JSON format)")

    if st.button("Create Vector Store"):
        vector_store_data = {
            "config_id": config_id_create or None,
            "store_id": store_id_create or None,
            "vector_store_class": vector_store_class,
            "params": json.loads(params) if params else {},
            "embeddings_model_class": embeddings_model_class if embeddings_model_class != "None" else None,
            "embeddings_params": json.loads(embeddings_params) if embeddings_params else {},
            "description": description,
            "custom_metadata": json.loads(custom_metadata) if custom_metadata else {}
        }
        created_vector_store = post_data(f"/vector_store/configure", vector_store_data)
        if created_vector_store:
            st.success("Vector store created successfully!")
            st.json(created_vector_store)
            st.session_state.loaded_store_ids = fetch_loaded_store_ids()

    # Aggiunta di documenti al vector store con un form
    st.subheader("Add Documents to Vector Store")
    if "loaded_store_ids" not in st.session_state:
        st.session_state.loaded_store_ids = fetch_loaded_store_ids()

    with st.form(key="add_document_form"):
        store_id_add_docs = st.selectbox("Store ID (Add Documents)", st.session_state.loaded_store_ids)
        page_content = st.text_area("Page Content", key="page_content_add_docs_form")
        metadata = st.text_area("Metadata (JSON format)", key="metadata_add_docs_form")
        submit_button = st.form_submit_button(label="Add Document")

    if submit_button:
        doc_data = {
            "page_content": page_content,
            "metadata": json.loads(metadata) if metadata else {}
        }
        result = post_data(f"/vector_store/documents/{store_id_add_docs}", [doc_data])
        if result:
            st.success("Document added to vector store successfully!")
            st.json(result)

    # Aggiunta di documenti dal document store
    st.subheader("Add Documents from Document Store to Vector Store")
    store_id_add_docs_from_store = st.selectbox("Store ID (Add Documents from Document Store)", st.session_state.loaded_store_ids)
    document_collection = st.text_input("Document Collection Name")
    if st.button("Add Documents from Document Store"):
        result = add_documents_from_document_store(store_id_add_docs_from_store, document_collection)
        if result:
            st.success("Documents added from document store to vector store successfully!")
            st.json(result)

        # Sezione per aggiornare documenti
    st.subheader("Update Document in Vector Store")
    store_id_update_docs = st.selectbox("Store ID (Update Document)", st.session_state.loaded_store_ids)
    document_id_update = st.text_input("Document ID (Update)", key="document_id_update")

    if st.button("Load Document for Update"):
        # Carica il documento selezionato
        document = fetch_data(f"/vector_store/documents/{store_id_update_docs}/{document_id_update}")
        if document:
            st.session_state.page_content_update = document.get("page_content", "")
            st.session_state.metadata_update = json.dumps(document.get("metadata", {}))

    if "page_content_update" in st.session_state and "metadata_update" in st.session_state:
        with st.form(key="update_document_form"):
            page_content_update = st.text_area("Page Content", value=st.session_state.page_content_update,
                                               key="page_content_update_form")
            metadata_update = st.text_area("Metadata (JSON format)", value=st.session_state.metadata_update,
                                           key="metadata_update_form")
            submit_update_button = st.form_submit_button(label="Update Document")

        if submit_update_button:
            updated_doc_data = {
                "page_content": page_content_update,
                "metadata": json.loads(metadata_update) if metadata_update else {}
            }
            result = update_document(store_id_update_docs, document_id_update, updated_doc_data)
            if result:
                st.success("Document updated successfully!")
                st.json(result)

    # Sezione per cancellare documenti
    st.subheader("Delete Document from Vector Store")
    store_id_delete_docs = st.selectbox("Store ID (Delete Document)", st.session_state.loaded_store_ids,
                                        key="store_id_delete_docs")
    document_id_delete = st.text_input("Document ID (Delete)", key="document_id_delete")
    if st.button("Delete Document"):
        result = delete_document(store_id_delete_docs, document_id_delete)
        if result:
            st.success("Document deleted successfully!")

    # Caricamento di un vector store in memoria
    st.subheader("Load Vector Store")
    config_id_load = st.selectbox("Select Config ID (Load)", [config['config_id'] for config in st.session_state.vector_store_configs])
    if st.button("Load Vector Store"):
        result = post_data(f"/vector_store/load/{config_id_load}", {})
        if result:
            st.success("Vector store loaded successfully!")
            st.json(result)
            st.session_state.loaded_store_ids = fetch_loaded_store_ids()

    # Offload di un vector store dalla memoria
    st.subheader("Offload Vector Store")
    store_id_offload = st.selectbox("Store ID (Offload)", st.session_state.loaded_store_ids)
    if st.button("Offload Vector Store"):
        result = post_data(f"/vector_store/offload/{store_id_offload}", {})
        if result:
            st.success("Vector store offloaded successfully!")
            st.json(result)
            st.session_state.loaded_store_ids = fetch_loaded_store_ids()

    # Ricerca di documenti nel vector store
    st.subheader("Search Vector Store")
    store_id_search = st.selectbox("Store ID (Search)", st.session_state.loaded_store_ids)
    query = st.text_input("Search Query")
    search_type = st.selectbox("Search Type", ["similarity", "mmr", "similarity_score_threshold"])
    search_kwargs = st.text_area("Search Kwargs (JSON format)")
    if st.button("Search"):
        search_data = {
            "query": query,
            "search_type": search_type,
            "search_kwargs": json.loads(search_kwargs) if search_kwargs else {}
        }
        search_results = post_data(f"/vector_store/search/{store_id_search}", search_data)
        if search_results:
            st.write("Search Results:")
            for result in search_results:
                st.json(result)

    # Filtrare documenti
    st.subheader("Filter Documents in Vector Store")
    store_id_filter_docs = st.selectbox("Store ID (Filter Documents)", st.session_state.loaded_store_ids)
    filter_criteria = st.text_area("Filter Criteria (JSON format)")
    skip = st.number_input("Skip", min_value=0, value=0, step=1)
    limit = st.number_input("Limit", min_value=1, value=10, step=1)
    if st.button("Filter Documents"):
        filter_criteria_json = json.loads(filter_criteria) if filter_criteria else {}
        filtered_docs = filter_documents(store_id_filter_docs, filter_criteria_json, skip, limit)
        if filtered_docs:
            st.write("Filtered Documents:")
            for doc in filtered_docs:
                st.json(doc)

    # Funzionalità di Update Vector Store Config
    st.subheader("Update Vector Store Configuration")
    config_id_update = st.selectbox("Select Config ID (Update)", [config['config_id'] for config in st.session_state.vector_store_configs])

    if config_id_update:
        config_to_update = next(config for config in st.session_state.vector_store_configs if config["config_id"] == config_id_update)
        store_id_update = st.text_input("Store ID (Update)", value=config_to_update.get("store_id", ""), key="store_id_update")
        vector_store_class_update = st.selectbox("Select Vector Store Class (Update)", ["Chroma", "ElasticsearchStore", "ElasticVectorSearch", "FAISS"], index=["Chroma", "ElasticsearchStore", "ElasticVectorSearch", "FAISS"].index(config_to_update.get("vector_store_class", "")))
        params_update = st.text_area("Vector Store Params (JSON format, Update)", value=json.dumps(config_to_update.get("params", {})))
        embeddings_model_class_update = st.selectbox("Select Embeddings Model Class (Update)", ["None", "OpenAIEmbeddings"], index=["None", "OpenAIEmbeddings"].index(config_to_update.get("embeddings_model_class", "None")))
        embeddings_params_update = st.text_area("Embeddings Params (JSON format, Update)", value=json.dumps(config_to_update.get("embeddings_params", {})))
        description_update = st.text_area("Description (Update)", value=config_to_update.get("description", ""))
        custom_metadata_update = st.text_area("Custom Metadata (JSON format, Update)", value=json.dumps(config_to_update.get("custom_metadata", {})))

        if st.button("Update Vector Store"):
            vector_store_update_data = {
                "store_id": store_id_update or None,
                "vector_store_class": vector_store_class_update,
                "params": json.loads(params_update) if params_update else {},
                "embeddings_model_class": embeddings_model_class_update if embeddings_model_class_update != "None" else None,
                "embeddings_params": json.loads(embeddings_params_update) if embeddings_params_update else {},
                "description": description_update,
                "custom_metadata": json.loads(custom_metadata_update) if custom_metadata_update else {}}

            updated_vector_store = put_data(f"/vector_store/configure/{config_id_update}", vector_store_update_data)
            if updated_vector_store:
                st.success("Vector store updated successfully!")
                st.json(updated_vector_store)

    # Funzionalità di Delete Vector Store Config
    st.subheader("Delete Vector Store Configuration")
    config_id_delete = st.selectbox("Select Config ID (Delete)", [config['config_id'] for config in st.session_state.vector_store_configs])
    if st.button("Delete Vector Store"):
        result = delete_data(f"/vector_store/configure/{config_id_delete}")
        if result:
            st.success("Vector store configuration deleted successfully!")

if __name__ == "__main__":
    main()
