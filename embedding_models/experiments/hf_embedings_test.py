from langchain_community.embeddings import HuggingFaceEmbeddings

# Configurazione del modello e delle opzioni
model_name = "intfloat/multilingual-e5-base"  # Modello multilingue

model_kwargs = {
    'device': 'cpu',  # Imposta 'cuda' se utilizzi una GPU e hai installato PyTorch con supporto CUDA
    'trust_remote_code': True  # Permette di caricare modelli da fonti remote
}

encode_kwargs = {
    'normalize_embeddings': True,  # Normalizza le embeddings per ridurre l'influenza della lunghezza del documento
    'batch_size': 16,  # Imposta una dimensione del batch appropriata per la tua configurazione hardware
}

# Inizializzazione di HuggingFaceEmbeddings
hf_embeddings = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)

# Test con alcuni testi
texts = [
    "Hello world",
    "Bonjour le monde",
    "Hola mundo",
    "Hallo Welt",
    "Ciao mondo"
]

# Ottenere gli embeddings per i testi forniti
embeddings = hf_embeddings.embed_documents(texts)

# Visualizzare gli embeddings
for text, embedding in zip(texts, embeddings):
    print(f"Text: {text}")
    print(f"Embedding: {embedding}")