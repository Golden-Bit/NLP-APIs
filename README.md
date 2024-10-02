# NLP-APIs
NLP APIs Read Me File

- Per maggiori informazioni vedere il contenuto della direcotry *docs*
- Per quanto riguarda l'implementazione della **NLP API** si deve considerare come *entry point* lo script *chains/api.py*
- Per l'implementazione della **RAG API** vedere *experiments/rag_api.py*

### Deploy

NLP API (Vedere *docs/nlp_api_docs/*):
    
    uvicorn chains.api:app --host 0.0.0.0 --port 8100 --workers 4 

RAG API (Vedere *docs/rag_api_docs/*):

    uvicorn experiments.rag_api:app --host 0.0.0.0 --port 8080 --workers 4 