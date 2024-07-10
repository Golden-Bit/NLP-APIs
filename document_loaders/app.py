import streamlit as st
import requests
import json

API_URL = "http://localhost:8101"  # Ensure this URL matches your FastAPI server's address

def fetch_data(endpoint, params=None):
    """Function to fetch data from the API."""
    try:
        response = requests.get(f"{API_URL}{endpoint}", params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Error retrieving data: {e}")
        return {}

def post_data(endpoint, data):
    """Function to send data to the API."""
    try:
        response = requests.post(f"{API_URL}{endpoint}", json=data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Error sending data: {e}")
        return {}

def delete_data(endpoint):
    """Function to delete configurations via the API."""
    try:
        response = requests.delete(f"{API_URL}{endpoint}")
        response.raise_for_status()
        return {"message": "Success"}
    except requests.RequestException as e:
        st.error(f"Error deleting: {e}")
        return {}

def main():
    st.title("Document Loader Configuration Management")

    # Sync configuration IDs from the database
    def sync_config_ids():
        configs = fetch_data("/list_configs")
        if configs:
            st.session_state["config_ids"] = [config["config_id"] for config in configs]

    if "config_ids" not in st.session_state:
        st.session_state["config_ids"] = []
        sync_config_ids()

    st.button("Sync with DB", on_click=sync_config_ids, use_container_width=True)

    st.header("Create New Loader Configuration")
    with st.form("create_loader_config_form"):
        config_id = st.text_input("Configuration ID (leave blank to auto-generate)")
        path = st.text_input("Documents Path", "/path/to/documents")
        loader_map = st.text_area("Loader Mapping (JSON format)", '{"*.txt": "TextLoader", "*.html": "BSHTMLLoader"}')
        loader_kwargs_map = st.text_area("Loader Parameters (JSON format)", '{"*.csv": {"delimiter": ","}}')
        metadata_map = st.text_area("Metadata Mapping (JSON format)", '{"*.txt": {"author": "John Doe"}}')
        recursive = st.checkbox("Recursive Loading", value=True)
        max_depth = st.number_input("Maximum Depth", min_value=1, value=5)
        silent_errors = st.checkbox("Ignore Errors", value=True)
        show_progress = st.checkbox("Show Progress", value=True)
        use_multithreading = st.checkbox("Use Multithreading", value=True)
        max_concurrency = st.number_input("Maximum Concurrency", min_value=1, value=8)
        submit_button = st.form_submit_button("Create Configuration", use_container_width=True)

        if submit_button:
            config_data = {
                "config_id": config_id if config_id else None,
                "path": path,
                "loader_map": json.loads(loader_map),
                "loader_kwargs_map": json.loads(loader_kwargs_map) if loader_kwargs_map else {},
                "metadata_map": json.loads(metadata_map) if metadata_map else {},
                "recursive": recursive,
                "max_depth": max_depth,
                "silent_errors": silent_errors,
                "show_progress": show_progress,
                "use_multithreading": use_multithreading,
                "max_concurrency": max_concurrency
            }
            result = post_data("/configure_loader", config_data)
            if result:
                st.success("Configuration created successfully!")
                sync_config_ids()

    st.header("List All Configurations")
    with st.form("list_configs_form"):
        submit_button = st.form_submit_button("View Configurations", use_container_width=True)
        if submit_button:
            configs = fetch_data("/list_configs")
            if configs:
                for config in configs:
                    st.json(config)

    st.header("View Configuration Details")
    with st.form("get_config_form"):
        config_id = st.selectbox("Select Configuration ID", st.session_state["config_ids"])
        submit_button = st.form_submit_button("View Configuration", use_container_width=True)

        if submit_button:
            config_details = fetch_data(f"/get_config/{config_id}")
            if config_details:
                st.json(config_details)

    st.header("Load Documents")
    with st.form("load_documents_form"):
        config_id = st.selectbox("Choose Configuration ID", st.session_state["config_ids"])
        submit_button = st.form_submit_button("Load Documents", use_container_width=True)

        if submit_button:
            result = post_data(f"/load_documents/{config_id}", {})
            if result:
                st.success("Documents loaded successfully!")
                st.json(result)

    st.header("Delete Loader Configuration")
    with st.form("delete_loader_config_form"):
        config_id = st.selectbox("Configuration ID to Delete", st.session_state["config_ids"])
        submit_button = st.form_submit_button("Delete Configuration", use_container_width=True)
        if submit_button:
            result = delete_data(f"/delete_config/{config_id}")
            if result:
                st.success("Configuration deleted successfully!")
                sync_config_ids()

if __name__ == "__main__":
    main()
