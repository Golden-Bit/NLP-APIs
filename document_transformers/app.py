import streamlit as st
import requests
import json
from typing import List, Dict, Any, Union, Optional

# API URL
API_URL = "http://localhost:8103"

# Helper functions for API requests
def fetch_data(endpoint: str, params: Optional[Dict[str, Any]] = None) -> Union[Dict, List[Dict]]:
    try:
        response = requests.get(f"{API_URL}{endpoint}", params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return {}

def post_data(endpoint: str, data: Union[Dict, List[Dict]]) -> Dict:
    try:
        response = requests.post(f"{API_URL}{endpoint}", json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error posting data: {e}")
        return {}

def delete_data(endpoint: str) -> Dict:
    try:
        response = requests.delete(f"{API_URL}{endpoint}")
        response.raise_for_status()
        return {"message": "Success"}
    except requests.exceptions.RequestException as e:
        st.error(f"Error deleting data: {e}")
        return {}

# Sync session variables with the database
def sync_config_ids():
    transformer_configs = fetch_data("/list_transformer_configs")
    transformer_map_configs = fetch_data("/list_transformer_map_configs")

    if transformer_configs:
        st.session_state["transformer_config_ids"] = [config["config_id"] for config in transformer_configs]
    if transformer_map_configs:
        st.session_state["transformer_map_config_ids"] = [config["config_id"] for config in transformer_map_configs]

# Initialize session state
if "transformer_config_ids" not in st.session_state:
    st.session_state["transformer_config_ids"] = []
if "transformer_map_config_ids" not in st.session_state:
    st.session_state["transformer_map_config_ids"] = []

# UI Components
def main():
    st.title("Transformer Configuration Management App")

    # Sync configuration IDs with database
    st.button("Sync with DB", on_click=sync_config_ids, use_container_width=True)

    # List Transformer Configurations
    st.header("List Transformer Configurations")
    with st.form(key="list_transformer_configs_form"):
        skip = st.number_input("Skip", min_value=0, value=0)
        limit = st.number_input("Limit", min_value=0, value=10)
        submit_button = st.form_submit_button(label="List Transformer Configurations", use_container_width=True)

        if submit_button:
            params = {"skip": skip, "limit": limit}
            configs = fetch_data("/list_transformer_configs", params)
            if configs:
                for config in configs:
                    st.json(config)

    # List Transformer Map Configurations
    st.header("List Transformer Map Configurations")
    with st.form(key="list_transformer_map_configs_form"):
        skip = st.number_input("Skip", min_value=0, value=0)
        limit = st.number_input("Limit", min_value=0, value=10)
        submit_button = st.form_submit_button(label="List Transformer Map Configurations", use_container_width=True)

        if submit_button:
            params = {"skip": skip, "limit": limit}
            configs = fetch_data("/list_transformer_map_configs", params)
            if configs:
                for config in configs:
                    st.json(config)

    # Create Transformer Configuration
    st.header("Create New Transformer Configuration")
    with st.form(key="create_transformer_form"):
        config_id = st.text_input("Config ID (leave blank to auto-generate)")
        transformer = st.selectbox("Transformer", ["CharacterTextSplitter", "RecursiveCharacterTextSplitter", "TokenTextSplitter"])
        kwargs = st.text_area("Kwargs (JSON format)", '{"chunk_size": 1, "chunk_overlap": 0, "separator": " "}')
        add_prefix_to_id = st.text_input("Add Prefix to ID", "PREFIX_")
        add_suffix_to_id = st.text_input("Add Suffix to ID", "_SUFFIX")
        add_split_index_to_id = st.checkbox("Add Split Index to ID", value=True)
        output_store = st.text_area("Output Store (JSON format)", '{"collection": "custom_collection"}')
        description = st.text_area("Description", "Example transformer configuration")
        metadata = st.text_area("Metadata (JSON format)", '{"author": "John Doe", "category": "Research"}')
        add_metadata_to_docs = st.text_area("Add Metadata to Docs (JSON format)", '{"custom_key": "custom_value"}')
        submit_button = st.form_submit_button(label="Create Transformer Configuration", use_container_width=True)

        if submit_button:
            try:
                config_data = {
                    "config_id": config_id if config_id else None,
                    "transformer": transformer,
                    "kwargs": json.loads(kwargs) if kwargs else {},
                    "add_prefix_to_id": add_prefix_to_id if add_prefix_to_id else None,
                    "add_suffix_to_id": add_suffix_to_id if add_suffix_to_id else None,
                    "add_split_index_to_id": add_split_index_to_id,
                    "output_store": json.loads(output_store) if output_store else None,
                    "description": description if description else None,
                    "metadata": json.loads(metadata) if metadata else None,
                    "add_metadata_to_docs": json.loads(add_metadata_to_docs) if add_metadata_to_docs else {}
                }
                result = post_data("/configure_transformer", config_data)
                if result:
                    st.success("Configuration created successfully!")
                    #st.json(result)
                    sync_config_ids()  # Sync configuration IDs with database
            except json.JSONDecodeError as e:
                st.error(f"JSON Decode Error: {e}")

    # Create Transformer Map
    st.header("Create New Transformer Map Configuration")
    with st.form(key="create_transformer_map_form"):
        config_id = st.text_input("Config ID (leave blank to auto-generate)")
        transformer_map = st.text_area("Transformer Map (JSON format)", '''
{
    "{\\"$or\\": [{\\"author\\": \\"John Doe\\"}, {\\"type\\": \\"report\\"}], \\"$and\\": [{\\"$or\\": [{\\"created\\": 2023}, {\\"department\\": \\"engineering\\"}]}]}": {
        "transformer": "CharacterTextSplitter",
        "kwargs": {"chunk_size": 1, "chunk_overlap": 0, "separator": " "},
        "add_prefix_to_id": "PREFIX_",
        "add_suffix_to_id": "_SUFFIX",
        "add_split_index_to_id": true,
        "add_metadata_to_docs": {"custom_key": "custom_value"},
        "output_store": {"collection": "custom_collection"}
    }
}
''')
        default_transformer = st.selectbox("Default Transformer", ["CharacterTextSplitter", "RecursiveCharacterTextSplitter", "TokenTextSplitter"])
        default_kwargs = st.text_area("Default Kwargs (JSON format)", '{"chunk_size": 1000, "chunk_overlap": 200}')
        default_add_prefix_to_id = st.text_input("Default Add Prefix to ID", "DEFAULT_PREFIX_")
        default_add_suffix_to_id = st.text_input("Default Add Suffix to ID", "_DEFAULT_SUFFIX")
        default_add_split_index_to_id = st.checkbox("Default Add Split Index to ID", value=True)
        default_add_metadata_to_docs = st.text_area("Default Add Metadata to Docs (JSON format)", '{"default_key": "default_value"}')
        default_output_store = st.text_area("Default Output Store (JSON format)", '{"collection": "default_collection"}')
        description = st.text_area("Description", "Example transformer map configuration")
        metadata = st.text_area("Metadata (JSON format)", '{"department": "engineering"}')
        submit_button = st.form_submit_button(label="Create Transformer Map", use_container_width=True)

        if submit_button:
            try:
                transformer_map_data = {
                    "config_id": config_id if config_id else None,
                    "transformer_map": json.loads(transformer_map) if transformer_map else {},
                    "default_transformer": default_transformer,
                    "default_kwargs": json.loads(default_kwargs) if default_kwargs else {},
                    "default_add_prefix_to_id": default_add_prefix_to_id if default_add_prefix_to_id else None,
                    "default_add_suffix_to_id": default_add_suffix_to_id if default_add_suffix_to_id else None,
                    "default_add_split_index_to_id": default_add_split_index_to_id,
                    "default_add_metadata_to_docs": json.loads(default_add_metadata_to_docs) if default_add_metadata_to_docs else {},
                    "default_output_store": json.loads(default_output_store) if default_output_store else None,
                    "description": description if description else None,
                    "metadata": json.loads(metadata) if metadata else None
                }
                result = post_data("/configure_transformer_map", transformer_map_data)
                if result:
                    st.success("Transformer map configuration created successfully!")
                    #st.json(result)
                    sync_config_ids()  # Sync configuration IDs with database
            except json.JSONDecodeError as e:
                st.error(f"JSON Decode Error: {e}")

    # Transform Documents
    st.header("Transform Documents")
    with st.form(key="transform_form"):
        config_id = st.selectbox("Transformer Map Config ID", st.session_state["transformer_map_config_ids"])
        documents = st.text_area("Documents (JSON format)", '''
[
    {"page_content": "This is a test document by John Doe, created in 2023.", "metadata": {"id": "abc", "author": "John Doe", "created": 2023}},
    {"page_content": "This is a report document in the engineering department.", "metadata": {"id": "def", "type": "report", "department": "engineering"}},
    {"page_content": "This is an unclassified document created in 2022.", "metadata": {"id": "ghi", "category": "general", "created": 2022}}
]
''')
        submit_button = st.form_submit_button(label="Transform Documents", use_container_width=True)

        if submit_button:
            try:
                doc_list = json.loads(documents) if documents else []
                doc_models = [{"page_content": doc["page_content"], "metadata": doc["metadata"]} for doc in doc_list]
                result = post_data(f"/transform_documents/{config_id}", doc_models)
                if result:
                    st.success("Documents transformed successfully!")
                    for doc in result:
                        st.json(doc)
            except json.JSONDecodeError as e:
                st.error(f"JSON Decode Error: {e}")

    # Transform Documents from Store
    st.header("Transform Documents from Store")
    with st.form(key="transform_from_store_form"):
        config_id = st.selectbox("Transformer Map Config ID", st.session_state["transformer_map_config_ids"])
        input_store = st.text_area("Input Store (JSON format)", '{"collection_name": "source_collection"}')
        submit_button = st.form_submit_button(label="Transform from Store", use_container_width=True)

        if submit_button:
            try:
                input_store_data = json.loads(input_store) if input_store else {}
                result = post_data(f"/transform_documents_from_store/{config_id}", input_store_data)
                if result:
                    st.success("Documents transformed successfully from store!")
                    for doc in result:
                        st.json(doc)
            except json.JSONDecodeError as e:
                st.error(f"JSON Decode Error: {e}")

    # Search Transformer Configurations
    st.header("Search Transformer Configurations")
    with st.form(key="search_transformer_form"):
        transformer = st.text_input("Transformer")
        add_prefix_to_id = st.text_input("Add Prefix to ID")
        add_suffix_to_id = st.text_input("Add Suffix to ID")
        add_split_index_to_id = st.selectbox("Add Split Index to ID", [None, True, False])
        metadata = st.text_area("Metadata (JSON format)")
        skip = st.number_input("Skip", min_value=0, value=0)
        limit = st.number_input("Limit", min_value=0, value=10)
        submit_button = st.form_submit_button(label="Search Transformer Configurations", use_container_width=True)

        if submit_button:
            try:
                search_params = {
                    "transformer": transformer if transformer else None,
                    "add_prefix_to_id": add_prefix_to_id if add_prefix_to_id else None,
                    "add_suffix_to_id": add_suffix_to_id if add_suffix_to_id else None,
                    "add_split_index_to_id": add_split_index_to_id if add_split_index_to_id is not None else None,
                    "metadata": json.loads(metadata) if metadata else {},
                    "skip": skip,
                    "limit": limit
                }
                result = post_data("/search_transformer_configs", search_params)
                if result:
                    for config in result:
                        st.json(config)
            except json.JSONDecodeError as e:
                st.error(f"JSON Decode Error: {e}")

    # Search Transformer Map Configurations
    st.header("Search Transformer Map Configurations")
    with st.form(key="search_transformer_map_form"):
        transformer = st.text_input("Transformer")
        add_prefix_to_id = st.text_input("Add Prefix to ID")
        add_suffix_to_id = st.text_input("Add Suffix to ID")
        add_split_index_to_id = st.selectbox("Add Split Index to ID", [None, True, False])
        metadata = st.text_area("Metadata (JSON format)")
        skip = st.number_input("Skip", min_value=0, value=0)
        limit = st.number_input("Limit", min_value=0, value=10)
        submit_button = st.form_submit_button(label="Search Transformer Map Configurations", use_container_width=True)

        if submit_button:
            try:
                search_params = {
                    "transformer": transformer if transformer else None,
                    "add_prefix_to_id": add_prefix_to_id if add_prefix_to_id else None,
                    "add_suffix_to_id": add_suffix_to_id if add_suffix_to_id else None,
                    "add_split_index_to_id": add_split_index_to_id if add_split_index_to_id is not None else None,
                    "metadata": json.loads(metadata) if metadata else {},
                    "skip": skip,
                    "limit": limit
                }
                result = post_data("/search_transformer_map_configs", search_params)
                if result:
                    for config in result:
                        st.json(config)
            except json.JSONDecodeError as e:
                st.error(f"JSON Decode Error: {e}")

    # Delete Transformer Configuration
    st.header("Delete Transformer Configuration")
    with st.form(key="delete_transformer_form"):
        config_id = st.selectbox("Config ID to Delete", st.session_state["transformer_config_ids"])
        submit_button = st.form_submit_button(label="Delete Transformer Configuration", use_container_width=True)
        if submit_button:
            result = delete_data(f"/delete_transformer_config/{config_id}")
            if result:
                st.success("Configuration deleted successfully!")
                sync_config_ids()  # Sync configuration IDs with database

    # Delete Transformer Map Configuration
    st.header("Delete Transformer Map Configuration")
    with st.form(key="delete_transformer_map_form"):
        config_id = st.selectbox("Config ID to Delete", st.session_state["transformer_map_config_ids"])
        submit_button = st.form_submit_button(label="Delete Transformer Map Configuration", use_container_width=True)
        if submit_button:
            result = delete_data(f"/delete_transformer_map_config/{config_id}")
            if result:
                st.success("Transformer map configuration deleted successfully!")
                sync_config_ids()  # Sync configuration IDs with database

if __name__ == "__main__":
    main()
