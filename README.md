# NLP-APIs
NLP APIs Read Me File

- Per maggiori informazioni vedere il contenuto della direcotry *docs*
- Per quanto riguarda l'implementazione della **NLP API** si deve considerare come *entry point* lo script *app/main.py*

### Deploy

NLP API (Vedere *docs/nlp_api_docs/*):
    
    uvicorn app.main:app --host 0.0.0.0 --port 8100 --workers 4