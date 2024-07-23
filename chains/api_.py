from fastapi import FastAPI

from data_stores.api import router as router_1
from document_loaders.api import router as router_2
from document_stores.api import router as router_3
from document_transformers.api import router as router_4
from embedding_models.api import router as router_5
from vector_stores.api import router as router_6
from llms.api import router as router_7
from prompts.api import router as router_8
from tools.api import router as router_9


app = FastAPI()

app.include_router(router_1, prefix="/data_stores", tags=["data_stores"])
app.include_router(router_2, prefix="/document_loaders", tags=["document_loaders"])
app.include_router(router_3, prefix="/document_stores", tags=["document_stores"])
app.include_router(router_4, prefix="/document_transformers", tags=["document_transformers"])
app.include_router(router_5, prefix="/embedding_models", tags=["embedding_models"])
app.include_router(router_6, prefix="/vector_stores", tags=["vector_stores"])
app.include_router(router_7, prefix="/llms", tags=["llms"])
app.include_router(router_8, prefix="/prompts", tags=["prompts"])
app.include_router(router_9, prefix="/tools", tags=["tools"])


# TODO:
#  - [ ]  creare una classe ChainManager
#  - [ ]  usa LCEL di alngchain come logica per l'assemblaggio delle catene
#  - [ ] per ora implementa solo il caso di una catena per QA con retriever
#  - [ ]  creare API con lo scopo di offrire interfaccia per configurare catene in langchain. usa id di elementi
#  riferiti a script importati per caricare le componenti configurate.
#  - [ ]  creare endpoint per configurare una catena (associare id a configurazione, contiene anche id della catena)
#  - [ ]  creare endpoint per modificare una configurazione
#  - [ ]  creare endpoint per eliminare una configurazione
#  - [ ]  creare endpoint per caricare una catena in memoria mediante una configurazione (associare id a catena)
#  - [ ]  creare endpoint per eliminare la catena dalla memoria (unlaod)
#  - [ ]  per ora non creare endpoint adibiti all'esecuzione della catena
#  - [ ]  salvare le configurazioni nel mongo db
#  - [ ]  storare i modelli in un dict predisposto nella classe ChainManager

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8109)

