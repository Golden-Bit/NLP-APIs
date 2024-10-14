
########################################################################################################################
import sys
import platform

# Controlla il sistema operativo
if platform.system() == 'Linux':
    import pysqlite3
    # Sostituisce il modulo sqlite3 con pysqlite3 solo su Linux
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
else:
    pass
########################################################################################################################

from fastapi import FastAPI, HTTPException, Path, Body, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from data_stores.api import router as router_1
from document_loaders.api import router as router_2
from document_stores.api import router as router_3
from document_transformers.api import router as router_4
from embedding_models.api import router as router_5
from vector_stores.api import router as router_6
from llms.api import router as router_7
from prompts.api import router as router_8
from tools.api import router as router_9
from chains.api import router as router_10

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permetti tutte le origini
    allow_credentials=True,
    allow_methods=["*"],  # Permetti tutti i metodi (GET, POST, OPTIONS, ecc.)
    allow_headers=["*"],  # Permetti tutti gli headers
)

app.include_router(router_1, prefix="/data_stores", tags=["data_stores"])
app.include_router(router_2, prefix="/document_loaders", tags=["document_loaders"])
app.include_router(router_3, prefix="/document_stores", tags=["document_stores"])
app.include_router(router_4, prefix="/document_transformers", tags=["document_transformers"])
app.include_router(router_5, prefix="/embedding_models", tags=["embedding_models"])
app.include_router(router_6, prefix="/vector_stores", tags=["vector_stores"])
app.include_router(router_7, prefix="/llms", tags=["llms"])
app.include_router(router_8, prefix="/prompts", tags=["prompts"])
app.include_router(router_9, prefix="/tools", tags=["tools"])
app.include_router(router_10, prefix="/chains", tags=["chains"])

