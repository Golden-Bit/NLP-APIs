from google.cloud import storage
from typing import List, Optional, Dict, Any
import json
import os
import mimetypes
import time

class GCSFileStorage:
    """
    Class for managing file storage using Google Cloud Storage.
    """

    def __init__(self, bucket_name: str, service_account_json: str):
        """
        Initialize the GCSFileStorage with a bucket name and service account JSON.

        Args:
            bucket_name (str): The name of the Google Cloud Storage bucket.
            service_account_json (str): Path to the service account JSON file for authentication.
        """
        self.client = storage.Client.from_service_account_json(service_account_json)
        self.bucket = self.client.bucket(bucket_name)
        self.metadata_store_blob = self.bucket.blob("metadata.json")
        self._initialize_metadata_store()

    def _initialize_metadata_store(self):
        """Initialize metadata storage if it doesn't exist."""
        if not self.metadata_store_blob.exists():
            self._save_metadata_store({})

    def _load_metadata_store(self) -> Dict[str, Any]:
        """Load the metadata store from the JSON blob in GCS."""
        if self.metadata_store_blob.exists():
            return json.loads(self.metadata_store_blob.download_as_text())
        return {}

    def _save_metadata_store(self, metadata_store: Dict[str, Any]) -> None:
        """Save the metadata store to the JSON blob in GCS."""
        self.metadata_store_blob.upload_from_string(json.dumps(metadata_store, indent=4))

    def _normalize_key(self, key: str) -> str:
        """Normalize file path to use forward slashes."""
        return key.replace("\\", "/")

    def save_file(self, key: str, content: bytes, custom_metadata: Optional[Dict[str, Any]] = None) -> None:
        """Save a file to GCS and store metadata."""
        key = self._normalize_key(key)
        blob = self.bucket.blob(key)
        blob.upload_from_string(content)
        metadata_store = self._load_metadata_store()
        file_metadata = {
            "size": len(content),
            "custom_metadata": custom_metadata or {},
            "mime_type": mimetypes.guess_type(key)[0],
            "modified_time": time.ctime(),
        }
        metadata_store[key] = file_metadata
        self._save_metadata_store(metadata_store)

    def get_file(self, key: str) -> Optional[bytes]:
        """Retrieve a file from GCS."""
        blob = self.bucket.blob(key)
        if blob.exists():
            return blob.download_as_bytes()
        return None

    def delete_file(self, key: str) -> None:
        """Delete a file from GCS and remove its metadata."""
        blob = self.bucket.blob(key)
        if blob.exists():
            blob.delete()
        metadata_store = self._load_metadata_store()
        if key in metadata_store:
            del metadata_store[key]
        self._save_metadata_store(metadata_store)

    def list_files(self, directory: Optional[str] = None) -> List[str]:
        """List all files in a specific "directory" or globally if no directory is specified."""
        directory = self._normalize_key(directory) if directory else None
        blobs = self.bucket.list_blobs(prefix=directory)
        return [blob.name for blob in blobs]

    def update_file(self, key: str, content: bytes, custom_metadata: Optional[Dict[str, Any]] = None) -> None:
        """Update an existing file in GCS along with its metadata."""
        self.save_file(key, content, custom_metadata)

    def save_file_metadata(self, file_id: str, custom_metadata: Dict[str, Any]) -> None:
        """Save custom metadata for a specific file."""
        metadata_store = self._load_metadata_store()
        if file_id not in metadata_store:
            raise KeyError(f"File '{file_id}' does not exist in metadata store.")
        metadata_store[file_id]['custom_metadata'] = custom_metadata
        self._save_metadata_store(metadata_store)

    def get_file_metadata(self, key: str) -> dict:
        """Retrieve the metadata of a specific file."""
        metadata_store = self._load_metadata_store()
        return metadata_store.get(key, {})

    def save_directory_metadata(self, directory: str, custom_metadata: Dict[str, Any]) -> None:
        """Save metadata for a directory."""
        metadata_store = self._load_metadata_store()
        metadata_store[directory] = custom_metadata
        self._save_metadata_store(metadata_store)

    def get_directory_metadata(self, directory: str) -> dict:
        """Retrieve metadata for a specific directory."""
        metadata_store = self._load_metadata_store()
        return metadata_store.get(directory, {})

    def list_directories(self) -> List[str]:
        """List all simulated directories in GCS."""
        directories = set()
        blobs = self.bucket.list_blobs()
        for blob in blobs:
            directory = os.path.dirname(blob.name)
            if directory:
                directories.add(directory)
        return list(directories)

    def delete_directory_metadata(self, directory: str) -> None:
        """Delete metadata for a specific directory."""
        metadata_store = self._load_metadata_store()
        if directory in metadata_store:
            del metadata_store[directory]
            self._save_metadata_store(metadata_store)
        else:
            raise KeyError(f"Metadata for directory '{directory}' does not exist.")

    def search_files(self, query: str, directory: Optional[str] = None) -> List[str]:
        """Search for files matching the query within a specific directory or globally."""
        metadata_store = self._load_metadata_store()
        results = []
        for key, metadata in metadata_store.items():
            if directory and not key.startswith(directory):
                continue
            if query.lower() in key.lower() or any(query.lower() in str(value).lower() for value in metadata.values()):
                results.append(key)
        return results

    def filter_files(self, mime_type: Optional[str] = None, min_size: Optional[int] = None, max_size: Optional[int] = None) -> List[str]:
        """Filter files based on MIME type and size."""
        metadata_store = self._load_metadata_store()
        results = []
        for key, metadata in metadata_store.items():
            if mime_type and metadata.get("mime_type") != mime_type:
                continue
            size = metadata.get("size")
            if size is not None:
                if min_size is not None and size < min_size:
                    continue
                if max_size is not None and size > max_size:
                    continue
            results.append(key)
        return results
