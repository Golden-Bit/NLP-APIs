import json
import base64
from pydantic import BaseModel, constr
import requests
import pytesseract
from PIL import Image  # Import Image from PIL
from io import BytesIO  # Import BytesIO for handling byte data
import streamlit as st

## imposta la chiave
OPEN_AI_KEY = "...."

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Golden Bit\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

class CallGptInput(BaseModel):
    prompt_context: str
    text_extracted_ocr: str
    file: str  # Assumiamo che 'file' sia una stringa Base64


def extract_text_ocr(file, psm_value, whitelist) -> str:
    """Extract text from a base64-encoded image with configurable PSM and whitelist."""
    byte = base64.b64decode(file)
    image_pillow = Image.open(BytesIO(byte))

    # Build the config string for pytesseract
    config = f'--dpi 300 --psm {psm_value}'
    if whitelist:
        config += f' -c tessedit_char_whitelist={whitelist}'

    text_extracted_ocr = pytesseract.image_to_string(image_pillow,
                                                     lang='eng',
                                                     config=config)

    return text_extracted_ocr
def call_gpt(params: CallGptInput, max_token: int) -> str:
    """ Funzione per chiamare il modello GPT-4o  con testo e immagine. """

    # Estrai i dati dalla classe Pydantic
    prompt_context = params.prompt_context
    text_extracted_ocr = params.text_extracted_ocr
    base64_image = params.file

    ## converti in formato utf-8

    # base64_image= base64_image.encode('utf-8')

    ## Create Prompt

    prompt = """
**Obiettivo:**
Fornire una descrizione tecnica estremamente dettagliata, approfondita e completa dell'immagine fornita, che rappresenta uno schema elettrico o un progetto ingegneristico. La descrizione sarà inserita in una base di conoscenza tecnica, pertanto deve essere precisa, professionale e priva di commenti personali o riferimenti al formato della comunicazione.

**Informazioni disponibili:**

- **Testo estratto dall'OCR:**
  {text_extracted_ocr}

- **Contesto associato all'immagine:**
  {prompt_context}

**Istruzioni:**

1. **Analisi Approfondita dell'Immagine:**
   - **Componenti Tecnici:**
     - Identifica e descrivi dettagliatamente tutti i componenti presenti, inclusi simboli elettrici, circuiti integrati, resistori, condensatori, induttori, interruttori, relè, motori, sensori e qualsiasi altro elemento rilevante.
     - Fornisci le specifiche tecniche di ogni componente, come valori nominali, tolleranze, potenze, tensioni operative e caratteristiche distintive.
   - **Annotazioni e Testi:**
     - Analizza tutte le etichette, note, codici e annotazioni presenti nell'immagine, anche se non completamente catturate dall'OCR, cercando di interpretarle e inserirle nella descrizione.
     - Riporta formule, equazioni o riferimenti tecnici presenti.
   - **Struttura e Layout:**
     - Descrivi la disposizione fisica dei componenti, il layout delle tracce o dei conduttori, la posizione dei connettori e l'organizzazione generale dello schema o del progetto.
     - Evidenzia eventuali sezioni modulari, sottosistemi o blocchi funzionali.

2. **Integrazione Dettagliata delle Informazioni:**
   - **Funzionamento e Principi Operativi:**
     - Spiega in modo approfondito come funziona il circuito o il sistema, descrivendo i principi teorici sottostanti, come leggi elettriche, fenomeni fisici o algoritmi di controllo.
     - Dettaglia il percorso dei segnali elettrici, i flussi di corrente, le interazioni tra componenti attivi e passivi, e le modalità di controllo o retroazione.
   - **Applicazioni e Scopi:**
     - Discerni e descrivi le possibili applicazioni pratiche del progetto, il suo scopo principale e come si inserisce nel contesto ingegneristico più ampio.
     - Considera settori di utilizzo come elettronica di consumo, automazione industriale, telecomunicazioni, energia rinnovabile, ecc.
   - **Normative e Standard Tecnici:**
     - Riferisci eventuali standard, normative o protocolli pertinenti (es. IEC, IEEE, ANSI), e come il progetto li soddisfa o li implementa.
     - Menziona pratiche di sicurezza elettrica, compatibilità elettromagnetica (EMC), efficienza energetica o altre considerazioni normative.

3. **Dettagli su Materiali e Tecnologie:**
   - **Materiali Utilizzati:**
     - Specifica i materiali dei componenti, come tipi di semiconduttori, metalli conduttivi, isolanti, substrati per circuiti stampati (PCB), ecc.
   - **Tecnologie di Produzione:**
     - Descrivi le tecniche di produzione o assemblaggio coinvolte, come montaggio superficiale (SMT), tecnologia a foro passante (THT), litografia, stampa 3D, ecc.
   - **Considerazioni Progettuali:**
     - Approfondisci le scelte progettuali effettuate, come dimensionamento dei componenti, gestione termica, minimizzazione del rumore elettrico, affidabilità e manutenzione.

4. **Stile della Descrizione:**
   - Utilizza terminologia tecnica specifica e appropriata al campo ingegneristico di riferimento.
   - Organizza il testo in modo logico e coerente, con sezioni e sottosezioni chiaramente delineate.
   - Assicurati che la descrizione sia esaustiva, includendo tutti i dettagli possibili per offrire una comprensione completa e approfondita dell'immagine.
   - Mantieni un tono oggettivo e professionale, evitando commenti personali o digressioni non pertinenti.

**Formato Richiesto:**

- **Introduzione Estesa:**
  - Fornisci una panoramica completa dell'immagine, identificando il tipo di schema o progetto (es. schema elettrico di un amplificatore audio, progetto di un sistema di controllo industriale, layout di un circuito stampato per un dispositivo IoT).
  - Introduci il contesto tecnico e l'importanza del progetto nel suo settore specifico.

- **Descrizione Dettagliata Organizzata:**
  - **Componenti e Simboli:**
    - Elenca e descrivi ogni componente, simbolo e notazione, spiegandone la funzione e le caratteristiche tecniche.
  - **Funzionamento del Sistema:**
    - Spiega passo dopo passo come il sistema opera, includendo sequenze operative, logiche di controllo, flussi di dati o energia.
  - **Connessioni e Interfacce:**
    - Dettaglia le connessioni interne ed esterne, tipi di connettori, interfacce di comunicazione (es. UART, SPI, I2C, Ethernet), e protocolli utilizzati.
  - **Considerazioni Tecniche:**
    - Approfondisci aspetti come alimentazione, gestione dei segnali, protezioni elettriche, schermature, sincronizzazione, ecc.
  - **Analisi delle Prestazioni:**
    - Fornisci dati su prestazioni attese, efficienza, precisione, velocità di operazione, limiti operativi e condizioni ambientali.

- **Conclusione Ampia:**
  - Riassumi le caratteristiche chiave e l'importanza del progetto.
  - Indica potenziali sviluppi futuri, miglioramenti possibili o adattamenti ad altre applicazioni.
  - Includi eventuali note su test, validazione, certificazioni o feedback da utilizzi precedenti.

---

*Si prega di fornire una descrizione tecnica estremamente dettagliata dell'immagine seguendo le istruzioni sopra indicate, assicurandosi di estendere la descrizione il più possibile per coprire ogni aspetto rilevante.*
*Scrivi testo in output senza usare i simboli '#' per regolare i font. preserva comunque uno stile analogo per l organizzazione del testo e eventualmente sottolinea in grassetto le informazioni importanti*
---"""

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPEN_AI_KEY}"
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
    json = response.json()

    # Gestisci la risposta
    if response.status_code == 200:
        json_response = response.json()
        output = json_response["choices"][0]["message"]["content"]
        return output
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")


def main():
    st.title("Image Description Application")
    st.write("Upload an image and get a detailed description generated using GPT-4 Vision.")

    # Select Page Segmentation Mode (PSM) options
    psm_option = st.selectbox("Select PSM (Page Segmentation Mode)",
                              ['1 - Automatic OSD',
                               '3 - Fully automatic page segmentation',
                               '6 - Assume a single uniform block of text',
                               '7 - Treat the image as a single text line',
                               '8 - Treat the image as a single word',
                               '11 - Sparse text'])

    # Map user-friendly options to actual PSM values
    psm_value = {
        '1 - Automatic OSD': '1',
        '3 - Fully automatic page segmentation': '3',
        '6 - Assume a single uniform block of text': '6',
        '7 - Treat the image as a single text line': '7',
        '8 - Treat the image as a single word': '8',
        '11 - Sparse text': '11'
    }[psm_option]

    # Additional options (e.g., whitelist of characters)
    whitelist = st.text_input("Whitelist characters (optional)", value="")

    # Image upload
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Convert image to base64
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

        # Set context and OCR extraction
        context = st.text_area("Provide context for the image")
        extracted_text = extract_text_ocr(image_base64, psm_value, whitelist)

        st.write("Extracted Text (OCR):")
        st.write(extracted_text)

        if st.button("Generate Description"):
            # Prepare parameters for GPT-4 call
            params = CallGptInput(
                prompt_context=context,
                text_extracted_ocr=extracted_text,
                file=image_base64
            )

            try:
                description = call_gpt(params, 16000)
                st.write("Generated Description:")
                st.write(description)
            except Exception as e:
                st.error(str(e))


if __name__ == "__main__":
    main()

