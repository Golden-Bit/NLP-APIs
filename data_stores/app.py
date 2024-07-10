import base64

import streamlit as st
import requests
from pathlib import Path

API_URL = "http://127.0.0.1:8100"


def list_files(subdir=None):
    params = {"subdir": subdir} if subdir else {}
    response = requests.get(f"{API_URL}/files", params=params)
    if response.status_code == 200:
        files = response.json()
        return files
    else:
        st.error(f"Failed to list files: {response.text}")
        return []


def upload_file(file, subdir=None, description=None, extra_metadata=None):
    files = {"file": file}
    data = {"subdir": subdir, "file_description": description, "extra_metadata": extra_metadata}
    response = requests.post(f"{API_URL}/upload", files=files, data=data)
    if response.status_code == 200:
        st.success("File uploaded successfully")
        return response.json()
    else:
        st.error(f"Failed to upload file: {response.text}")
        return None


st.title("File Management Interface")

# Create a directory
st.header("Create a Directory")
new_directory = st.text_input("Directory path to create")
new_directory_metadata = st.text_area("Metadata for the new directory (JSON format)", "")
if st.button("Create Directory"):
    data = {
        'directory': new_directory,
        'description': "",
        'extra_metadata': new_directory_metadata
    }
    response = requests.post(f"{API_URL}/create_directory", data=data)
    if response.status_code == 200:
        st.success("Directory created successfully!")
        st.json(response.json())
    else:
        st.error("Error creating directory")
        st.json(response.json())

# Delete a directory
st.header("Delete a Directory")
directory_to_delete = st.text_input("Directory path to delete")
if st.button("Delete Directory"):
    response = requests.delete(f"{API_URL}/delete_directory/{directory_to_delete}")
    if response.status_code == 200:
        st.success("Directory deleted successfully!")
        st.json(response.json())
    else:
        st.error("Error deleting directory")
        st.json(response.json())

# Upload a file
st.header("Upload a File")
uploaded_file = st.file_uploader("Choose a file")
subdir = st.text_input("Subdirectory", value="")
description = st.text_input("File Description", value="")
extra_metadata = st.text_area("Extra Metadata (JSON)", value="")

if st.button("Upload File"):
    if uploaded_file:
        metadata = upload_file(uploaded_file, subdir, description, extra_metadata)
        if metadata:
            st.json(metadata)

# List files
st.header("List Files")
list_subdir = st.text_input("Subdirectory to list files from", value="")
if st.button("List Files"):
    files = list_files(list_subdir)
    for file_metadata in files:
        st.json(file_metadata)

# View a file
st.header("View a File")
file_id_to_view = st.text_input("File ID to view")
if st.button("View File"):
    response = requests.get(f"{API_URL}/view/{file_id_to_view}")
    if response.status_code == 200:
        st.success("File retrieved successfully!")
        st.components.v1.html(response.text)
    else:
        st.error("Error retrieving file")
        st.json(response.json())

# Download a file
st.header("Download a File")
file_id_to_download = st.text_input("File ID to download")
if st.button("Download File"):
    response = requests.get(f"{API_URL}/download/{file_id_to_download}")
    if response.status_code == 200:
        st.success("File downloaded successfully!")
        filename = Path(file_id_to_download).name
        b64 = base64.b64encode(response.content).decode()
        href = f'<a href="data:file/octet-stream;base64,{b64}" download="{filename}">Download {filename}</a>'
        st.markdown(href, unsafe_allow_html=True)
    else:
        st.error("Error downloading file")
        st.json(response.json())

# Delete a file
st.header("Delete a File")
file_id_to_delete = st.text_input("File ID to delete")
if st.button("Delete File"):
    response = requests.delete(f"{API_URL}/delete/{file_id_to_delete}")
    if response.status_code == 200:
        st.success("File deleted successfully!")
        st.json(response.json())
    else:
        st.error("Error deleting file")
        st.json(response.json())

# Manage File Metadata
st.header("Manage File Metadata")

# Input fields
file_id_for_metadata = st.text_input("File ID for metadata")
file_description = st.text_area("Description for file", "")
extra_metadata_file = st.text_area("Extra metadata for file (JSON format)", "")

# Save File Metadata button
if st.button("Save File Metadata"):
    # Prepare data payload
    data = {
        'file_id': file_id_for_metadata,
        'file_description': file_description,
        'extra_metadata': extra_metadata_file
    }

    try:
        # Send POST request to API
        response = requests.post(f"{API_URL}/file/metadata", data=data)

        # Handle response
        if response.status_code == 200:
            st.success("File metadata saved successfully!")
            st.json(response.json())
        else:
            st.error(f"Error saving file metadata: {response.status_code}")
            st.json(response.json())

    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")

# Manage Directory Metadata
st.header("Manage Directory Metadata")
directory = st.text_input("Directory for metadata")
description = st.text_area("Description for directory", "")
extra_metadata_dir = st.text_area("Extra metadata for directory (JSON format)", "")

if st.button("Save Directory Metadata"):
    data = {
        'directory': directory,
        'description': description,
        'extra_metadata': extra_metadata_dir
    }
    response = requests.post(f"{API_URL}/directory/metadata", data=data)
    if response.status_code == 200:
        st.success("Directory metadata saved successfully!")
        st.json(response.json())
    else:
        st.error("Error saving directory metadata")
        st.json(response.json())

# Search files
st.header("Search Files")
query = st.text_input("Search query")
subdir_for_search = st.text_input("Subdirectory to search within", "")
if st.button("Search Files"):
    params = {'query': query, 'subdir': subdir_for_search}
    response = requests.get(f"{API_URL}/search/files", params=params)
    if response.status_code == 200:
        st.success("Search completed successfully!")
        st.json(response.json())
    else:
        st.error("Error searching files")
        st.json(response.json())

# Filter files
st.header("Filter Files")
mime_type = st.text_input("MIME type to filter by")
min_size = st.number_input("Minimum file size (bytes)", min_value=0)
max_size = st.number_input("Maximum file size (bytes)", min_value=0)
if st.button("Filter Files"):
    params = {'mime_type': mime_type, 'min_size': min_size, 'max_size': max_size}
    response = requests.get(f"{API_URL}/filter/files", params=params)
    if response.status_code == 200:
        st.success("Filter completed successfully!")
        st.json(response.json())
    else:
        st.error("Error filtering files")
        st.json(response.json())

# List directories
st.header("List Directories")
if st.button("List Directories"):
    response = requests.get(f"{API_URL}/directories")
    if response.status_code == 200:
        st.success("Directories retrieved successfully!")
        st.json(response.json())
    else:
        st.error("Error retrieving directories")
        st.json(response.json())
