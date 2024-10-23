import os
import json
from typing import Optional, Dict
from pydantic import BaseModel, Field
from langchain_core.tools import StructuredTool

# Per il processamento dei PDF con pymupdf4llm
import pymupdf4llm
#from pymupdf4llm import extract_and_replace_base64_images

# Per il processamento delle pagine web
import requests
from bs4 import BeautifulSoup

# Modelli Pydantic per operazioni sui documenti
class ReadLocalDocumentModel(BaseModel):
    file_path: str = Field(..., title="File Path", description="Percorso al file locale.")

class CreateLocalDocumentModel(BaseModel):
    file_path: str = Field(..., title="File Path", description="Percorso dove verrà creato il file.")
    content: str = Field(..., title="Content", description="Contenuto da scrivere nel file.")

class DeleteLocalDocumentModel(BaseModel):
    file_path: str = Field(..., title="File Path", description="Percorso al file locale da eliminare.")

class ModifyLocalDocumentModel(BaseModel):
    file_path: str = Field(..., title="File Path", description="Percorso al file locale da modificare.")
    new_content: str = Field(..., title="New Content", description="Nuovo contenuto da scrivere nel file.")

class ReadWebPageModel(BaseModel):
    url: str = Field(..., title="URL", description="URL della pagina web da leggere.")

class DocumentToolKitManager:
    def __init__(self):
        """Inizializza il DocumentToolKitManager."""
        pass

    # Metodi per documenti locali
    def read_local_document(self, file_path: str):
        """Legge e processa un documento locale (PDF o testo)."""
        if not os.path.exists(file_path):
            return f"File non trovato: {file_path}"
        _, ext = os.path.splitext(file_path)
        if ext.lower() == '.pdf':
            # Processa PDF utilizzando pymupdf4llm
            try:
                pymupdf4llm_config = {
                    #"pages": pages,
                    #"hdr_info": hdr_info,
                    #"write_images": write_images,
                    #"embed_images": embed_images,
                    #"image_path": image_path,
                    #"image_format": image_format,
                    #"image_size_limit": image_size_limit,
                    "force_text": True,
                    "page_chunks": True,
                    "margins": [0,0,0,0],
                    "dpi": 150,
                    #"page_width": page_width,
                    #"page_height": page_height,
                    #"table_strategy": table_strategy,
                    #"graphics_limit": graphics_limit,
                    #"fontsize_limit": fontsize_limit,
                    #"ignore_code": ignore_code,
                    #"extract_words": extract_words,
                    "show_progress": True
                }

                # Elaborazione del PDF
                md_output = pymupdf4llm.to_markdown(file_path, **pymupdf4llm_config)
                # md_output è una lista di oggetti per ciascuna pagina
                #images_dict = {}
                #image_counter = 0

                #for page_content in md_output:
                #    if 'text' in page_content:
                #        new_content = page_content['text']
                        #new_content = content
#                        new_content, base64_images, placeholder_mapping = extract_and_replace_base64_images(content)
                        # Aggiorna il contenuto nel md_output
                        #page_content['text'] = new_content
                        #for img in base64_images:
                        #    images_dict[str(image_counter)] = img
                        #    image_counter += 1
                        # Aggiorna images_dict con i placeholder
                        #for idx, placeholder in placeholder_mapping.items():
                        #    images_dict[idx]['placeholder'] = placeholder
                #    else:
                        # Nessun testo presente nella pagina
                #        print(f"Nessun testo trovato nella pagina {page_content.get('metadata', {}).get('page', 'sconosciuta')}")

                # Combina il testo da tutte le pagine
                print(md_output)
                full_text = "\n".join([page['text'] for page in md_output if 'text' in page])

                # Se necessario, puoi anche restituire images_dict per gestire le immagini
                # Per questo esempio, restituiamo solo il testo
                return full_text

            except Exception as e:
                return f"Errore nella lettura del PDF: {e}"
        else:
            # Assume che sia un file di testo
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                # Opzionale: aggiungi logica per estrarre informazioni dal contenuto
                return content
            except Exception as e:
                return f"Errore nella lettura del file: {e}"

    def create_local_document(self, file_path: str, content: str):
        """Crea un documento locale con il contenuto fornito."""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"File creato in: {file_path}"
        except Exception as e:
            return f"Errore nella creazione del file: {e}"

    def delete_local_document(self, file_path: str):
        """Elimina un documento locale."""
        try:
            os.remove(file_path)
            return f"File eliminato: {file_path}"
        except Exception as e:
            return f"Errore nell'eliminazione del file: {e}"

    def modify_local_document(self, file_path: str, new_content: str):
        """Modifica un documento locale con nuovo contenuto."""
        if not os.path.exists(file_path):
            return f"File non trovato: {file_path}"
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return f"File modificato: {file_path}"
        except Exception as e:
            return f"Errore nella modifica del file: {e}"

    # Metodi per pagine web
    def read_web_page(self, url: str):
        """Legge e processa il contenuto di una pagina web."""
        try:
            response = requests.get(url)
            response.raise_for_status()
            # Parse del contenuto della pagina web
            soup = BeautifulSoup(response.content, 'html.parser')
            # Estrae il testo dalla pagina web
            text = soup.get_text(separator=' ', strip=True)
            # Opzionale: aggiungi logica per estrarre informazioni dal testo
            return text
        except Exception as e:
            return f"Errore nella lettura della pagina web: {e}"

    def get_tools(self):
        """Restituisce una lista degli strumenti configurati usando StructuredTool."""
        return [
            StructuredTool(
                name="read_local_document",
                func=self.read_local_document,
                description="Usa questo strumento per leggere e processare un documento locale (file PDF o di testo). Richiede il percorso del file.",
                args_schema=ReadLocalDocumentModel
            ),
            StructuredTool(
                name="create_local_document",
                func=self.create_local_document,
                description="Usa questo strumento per creare un documento locale con il contenuto fornito. Richiede il percorso del file e il contenuto.",
                args_schema=CreateLocalDocumentModel
            ),
            StructuredTool(
                name="delete_local_document",
                func=self.delete_local_document,
                description="Usa questo strumento per eliminare un documento locale. Richiede il percorso del file.",
                args_schema=DeleteLocalDocumentModel
            ),
            StructuredTool(
                name="modify_local_document",
                func=self.modify_local_document,
                description="Usa questo strumento per modificare un documento locale con nuovo contenuto. Richiede il percorso del file e il nuovo contenuto.",
                args_schema=ModifyLocalDocumentModel
            ),
            StructuredTool(
                name="read_web_page",
                func=self.read_web_page,
                description="Usa questo strumento per leggere e processare il contenuto di una pagina web. Richiede l'URL.",
                args_schema=ReadWebPageModel
            )
        ]

# Esempio di utilizzo
#if __name__ == "__main__":
    # Inizializza il DocumentToolKitManager
#    doc_toolkit = DocumentToolKitManager()

    # Esempio: Leggi un documento PDF locale
#    read_doc = ReadLocalDocumentModel(file_path="percorso/al/tuo/documento.pdf")
#    content = doc_toolkit.read_local_document(**read_doc.dict())
#    print(content)

    # Esempio: Leggi una pagina web
#    read_web = ReadWebPageModel(url="https://www.esempio.com")
#    web_content = doc_toolkit.read_web_page(**read_web.dict())
#    print(web_content)
