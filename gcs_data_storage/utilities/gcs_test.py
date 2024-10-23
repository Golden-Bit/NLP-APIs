from storage import GCSFileStorage
import os

# Example usage of GCSFileStorage

# Initialize the GCSFileStorage class with your bucket and service account
bucket_name = 'marta-media'
service_account_json = 'marta-405111-392d32b40de1.json'

gcs_storage = GCSFileStorage(bucket_name, service_account_json)

# Save a file
file_content = b"Hello, this is a test file!"
gcs_storage.save_file('test_folder/test_file.txt', file_content, custom_metadata={'description': 'Test file'})

# Get the file content
downloaded_file = gcs_storage.get_file('test_folder/test_file.txt')
if downloaded_file:
    print(f"File content: {downloaded_file.decode()}")

# Get file metadata
metadata = gcs_storage.get_file_metadata('test_folder/test_file.txt')
print(f"Metadata: {metadata}")

# List all files in the bucket
files = gcs_storage.list_files('test_folder')
print(f"Files: {files}")

# Delete the file
gcs_storage.delete_file('test_folder/test_file.txt')
print("File deleted successfully.")

# List all directories
directories = gcs_storage.list_directories()
print(f"Directories: {directories}")
