import json
import base64
from pydantic import BaseModel
import requests
import pytesseract
from PIL import Image
from io import BytesIO
import streamlit as st

# Imposta la chiave API di default (consigliato usare variabili d'ambiente)
DEFAULT_OPENAI_API_KEY = "YOUR_DEFAULT_OPENAI_API_KEY"

# Imposta il percorso di Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Golden Bit\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

# Carica i prompt dal file JSON
prompts_json_path = "experiments/pdfloader_tester/prompts.json"

with open(prompts_json_path, "r", encoding="utf-8") as prompts_json_file:
    PROMPTS = json.load(prompts_json_file)

class CallGptInput(BaseModel):
    prompt_context: str
    text_extracted_ocr: str
    file: str  # Assumiamo che 'file' sia una stringa Base64

def extract_text_ocr(file, psm_value, whitelist) -> str:
    """Estrae testo da un'immagine base64 con PSM e whitelist configurabili."""
    byte = base64.b64decode(file)
    image_pillow = Image.open(BytesIO(byte))

    # Configura pytesseract
    config = f'--dpi 300 --psm {psm_value}'
    if whitelist:
        config += f' -c tessedit_char_whitelist={whitelist}'

    text_extracted_ocr = pytesseract.image_to_string(
        image_pillow,
        lang='eng',
        config=config
    )

    return text_extracted_ocr

def call_gpt(params: CallGptInput,
             max_token: int,
             prompt_id: str,
             openai_api_key: str) -> str:
    """Funzione per chiamare il modello GPT-4 con testo e immagine."""

    # Estrai i dati dai parametri
    prompt_context = params.prompt_context
    text_extracted_ocr = params.text_extracted_ocr
    base64_image = params.file

    # Crea il prompt utilizzando il template dal JSON
    prompt_template = PROMPTS[prompt_id]["content"]
    prompt = prompt_template.format(
        prompt_context=prompt_context,
        text_extracted_ocr=text_extracted_ocr
    )

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"{prompt}"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": max_token
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    json_response = response.json()

    # Gestisci la risposta
    if response.status_code == 200:
        output = json_response["choices"][0]["message"]["content"]
        return output
    else:
        raise Exception(f"Errore: {response.status_code} - {response.text}")

def main():
    st.title("Applicazione di Descrizione Immagini")
    st.write("Carica un'immagine e ottieni una descrizione dettagliata generata utilizzando GPT-4.")

    # Seleziona il Page Segmentation Mode (PSM)
    psm_options = {
        '1 - Automatic OSD': '1',
        '3 - Fully automatic page segmentation': '3',
        '6 - Assume a single uniform block of text': '6',
        '7 - Treat the image as a single text line': '7',
        '8 - Treat the image as a single word': '8',
        '11 - Sparse text': '11'
    }
    psm_option = st.selectbox("Seleziona PSM (Page Segmentation Mode)", list(psm_options.keys()))
    psm_value = psm_options[psm_option]

    # Opzione per la whitelist dei caratteri
    whitelist = st.text_input("Whitelist dei caratteri (opzionale)", value="")

    # Campo per inserire la OpenAI API Key
    openai_api_key_input = st.text_input("Inserisci la tua OpenAI API Key (opzionale)", value="", type="password")

    # Carica l'immagine
    uploaded_file = st.file_uploader("Carica un'immagine", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Immagine caricata", use_column_width=True)

        # Converte l'immagine in base64
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

        # Estrazione OCR
        extracted_text = extract_text_ocr(image_base64, psm_value, whitelist)

        st.write("**Testo estratto (OCR):**")
        st.write(extracted_text)

        # Seleziona il prompt_id tramite menu a tendina nella sezione delle immagini estratte
        prompt_ids = list(PROMPTS.keys())
        prompt_id = st.selectbox("Seleziona il Prompt ID", prompt_ids)

        # Contesto per l'immagine
        context = st.text_area("Fornisci il contesto per l'immagine")

        if st.button("Genera Descrizione"):
            # Utilizza l'API Key inserita dall'utente o quella di default
            if openai_api_key_input:
                openai_api_key = openai_api_key_input
            else:
                openai_api_key = DEFAULT_OPENAI_API_KEY

            # Prepara i parametri per la chiamata a GPT-4
            params = CallGptInput(
                prompt_context=context,
                text_extracted_ocr=extracted_text,
                file=image_base64
            )

            try:
                description = call_gpt(params,
                                       max_token=2500,
                                       prompt_id=prompt_id,
                                       openai_api_key=openai_api_key)
                st.write("**Descrizione Generata:**")
                st.write(description)
            except Exception as e:
                st.error(str(e))

if __name__ == "__main__":
    main()
