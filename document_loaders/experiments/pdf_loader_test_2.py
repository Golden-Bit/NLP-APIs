from langchain.document_loaders.pdf import PyMuPDFLoader

# Specify the path to your PDF file
pdf_path = "C:\\Users\\Golden Bit\\Downloads\\TKRPDTSgESr5GX18.pdf"

# Create a PyMuPDFLoader instance
loader = PyMuPDFLoader(pdf_path, extract_images=True)

# Load the PDF document
documents = loader.load()

# Process the loaded documents as needed
#for doc in documents:

print(f"\n{'-' * 120}\n".join([doc.page_content for doc in documents]))
