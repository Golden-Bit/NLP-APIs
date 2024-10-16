import streamlit as st
import json
import os
import re
import base64
from io import BytesIO
from PIL import Image

# Importa pymupdf4llm per l'estrazione in Markdown
import pymupdf4llm

from image_analyzer import extract_text_ocr, CallGptInput, call_gpt

st.title("Estrazione di Contenuti da PDF con pymupdf4llm")

# Configurazione dei parametri tramite widget specifici
st.subheader("Configurazione di pymupdf4llm.to_markdown")

# Configurazione dei parametri
pages_help = "Lista opzionale di numeri di pagina (0-based) da processare. Se lasciato vuoto, verranno processate tutte le pagine."
pages_input = st.text_input(
    "pages",
    value="",
    help=pages_help
)
if pages_input.strip() == "":
    pages = None
else:
    try:
        pages = json.loads(pages_input)
        if not isinstance(pages, list):
            st.error("Il campo 'pages' deve essere una lista di numeri interi.")
            st.stop()
    except json.JSONDecodeError:
        st.error("Il campo 'pages' deve essere una lista JSON valida di numeri interi.")
        st.stop()

hdr_info_help = "Informazioni per identificare gli header nel documento. Può essere 'None' o un oggetto personalizzato."
hdr_info = st.text_input(
    "hdr_info",
    value="None",
    help=hdr_info_help
)
if hdr_info.strip().lower() == "none":
    hdr_info = None

write_images_help = "Seleziona se salvare le immagini e i grafici come file separati."
write_images = st.checkbox(
    "write_images",
    value=False,
    help=write_images_help
)

embed_images_help = "Seleziona se incorporare le immagini come stringhe base64 nel Markdown."
embed_images = st.checkbox(
    "embed_images",
    value=True,
    help=embed_images_help
)

image_path_help = "Percorso della cartella dove salvare le immagini estratte. Necessario se 'write_images' è True."
image_path = st.text_input(
    "image_path",
    value="",
    help=image_path_help
)

image_format_help = "Formato delle immagini da salvare (es. 'png', 'jpeg')."
image_format = st.selectbox(
    "image_format",
    options=["png", "jpeg", "jpg", "tiff"],
    index=0,
    help=image_format_help
)

image_size_limit_help = "Limite della dimensione delle immagini (valore tra 0 e 1). Immagini più piccole di questo valore (in proporzione alla pagina) verranno ignorate."
image_size_limit = st.slider(
    "image_size_limit",
    min_value=0.0,
    max_value=1.0,
    value=0.00,
    step=0.01,
    help=image_size_limit_help
)

force_text_help = "Se True, estrarrà il testo anche dalle immagini."
force_text = st.checkbox(
    "force_text",
    value=True,
    help=force_text_help
)

page_chunks_help = "Se True, segmenta l'output per pagina e visualizza il risultato come JSON con indentazione."
page_chunks = st.checkbox(
    "page_chunks",
    value=False,
    help=page_chunks_help
)

margins_help = "Margini da considerare durante l'estrazione (lista o tupla di 1, 2 o 4 valori: sinistra, alto, destra, basso)."
margins_input = st.text_input(
    "margins",
    value="[0, 0, 0, 0]",
    help=margins_help
)
try:
    margins = json.loads(margins_input)
    if isinstance(margins, list) and (len(margins) in [1, 2, 4]):
        if len(margins) == 1:
            margins = margins * 4
        elif len(margins) == 2:
            margins = [margins[0], margins[1], margins[0], margins[1]]
        margins = tuple(margins)
    else:
        st.error("Il campo 'margins' deve essere una lista di 1, 2 o 4 numeri.")
        st.stop()
except json.JSONDecodeError:
    st.error("Il campo 'margins' deve essere una lista JSON valida di numeri.")
    st.stop()

dpi_help = "Risoluzione (DPI) per le immagini generate."
dpi = st.number_input(
    "dpi",
    min_value=1,
    value=300,
    help=dpi_help
)

page_width_help = "Larghezza della pagina da assumere se il layout è variabile."
page_width = st.number_input(
    "page_width",
    min_value=1,
    value=1224,
    help=page_width_help
)

page_height_help = "Altezza della pagina da assumere se il layout è variabile. Lascia vuoto per utilizzare il valore predefinito."
page_height_input = st.text_input(
    "page_height",
    value="",
    help=page_height_help
)
if page_height_input.strip() == "":
    page_height = None
else:
    try:
        page_height = float(page_height_input)
    except ValueError:
        st.error("Il campo 'page_height' deve essere un numero valido o vuoto.")
        st.stop()

table_strategy_help = "Strategia da utilizzare per il rilevamento delle tabelle."
table_strategy = st.selectbox(
    "table_strategy",
    options=["lines_strict", "text", "lines", "explicit"],
    index=0,
    help=table_strategy_help
)

graphics_limit_help = "Ignora la pagina se contiene più di questo numero di grafici vettoriali. Lascia vuoto per nessun limite."
graphics_limit_input = st.text_input(
    "graphics_limit",
    value="",
    help=graphics_limit_help
)
if graphics_limit_input.strip() == "":
    graphics_limit = None
else:
    try:
        graphics_limit = int(graphics_limit_input)
    except ValueError:
        st.error("Il campo 'graphics_limit' deve essere un numero intero o vuoto.")
        st.stop()

fontsize_limit_help = "Limite della dimensione del font per considerare il testo come codice."
fontsize_limit = st.number_input(
    "fontsize_limit",
    min_value=1,
    value=3,
    help=fontsize_limit_help
)

ignore_code_help = "Seleziona se ignorare la formattazione per font monospaziati."
ignore_code = st.checkbox(
    "ignore_code",
    value=False,
    help=ignore_code_help
)

extract_words_help = "Includi l'output tipo 'words' nei chunks di pagina."
extract_words = st.checkbox(
    "extract_words",
    value=False,
    help=extract_words_help
)

show_progress_help = "Mostra l'avanzamento durante l'elaborazione."
show_progress = st.checkbox(
    "show_progress",
    value=False,
    help=show_progress_help
)

# Caricamento del file PDF
uploaded_file = st.file_uploader("Carica un documento PDF", type=["pdf"])

if uploaded_file is not None:
    # Salvataggio temporaneo del file caricato
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Preparazione della configurazione
    pymupdf4llm_config = {
        "pages": pages,
        "hdr_info": hdr_info,
        "write_images": write_images,
        "embed_images": embed_images,
        "image_path": image_path,
        "image_format": image_format,
        "image_size_limit": image_size_limit,
        "force_text": force_text,
        "page_chunks": page_chunks,
        "margins": margins,
        "dpi": dpi,
        "page_width": page_width,
        "page_height": page_height,
        "table_strategy": table_strategy,
        "graphics_limit": graphics_limit,
        "fontsize_limit": fontsize_limit,
        "ignore_code": ignore_code,
        "extract_words": extract_words,
        "show_progress": show_progress
    }

    # Gestione di write_images e image_path
    if write_images and not image_path:
        st.error("Per salvare le immagini, specifica 'image_path' nella configurazione.")
        st.stop()
    if write_images and image_path and not os.path.exists(image_path):
        os.makedirs(image_path)

    # Funzione per estrarre e sostituire le immagini base64 nel Markdown
    def extract_and_replace_base64_images(markdown_text):
        pattern = r'!\[\]\(data:image\/([a-zA-Z]+);base64,([^\)]+)\)'
        images = []
        image_counter = 1

        def replace_func(match):
            nonlocal image_counter
            image_format = match.group(1)
            base64_image = match.group(2)
            images.append({'format': image_format, 'data': base64_image})
            placeholder = f'[Immagine {image_counter}]'
            image_counter += 1
            return placeholder

        new_markdown_text = re.sub(pattern, replace_func, markdown_text)
        return new_markdown_text, images

    # Inizializzazione del dizionario delle immagini
    images_dict = {}
    image_counter = 1

    # Utilizzo di pymupdf4llm.to_markdown con i parametri forniti
    try:
        md_output = pymupdf4llm.to_markdown("temp.pdf", **pymupdf4llm_config)
        print(md_output)

        # Elaborazione dell'output per estrarre le immagini
        if page_chunks:
            # md_output è una lista di oggetti per ciascuna pagina
            for page_content in md_output:
                if 'text' in page_content:
                    content = page_content['text']
                    new_content, base64_images = extract_and_replace_base64_images(content)
                    # Aggiorna il contenuto nel md_output
                    page_content['text'] = new_content
                    for img in base64_images:
                        images_dict[str(image_counter)] = img
                        image_counter += 1
                else:
                    # Nessun testo presente nella pagina
                    st.warning(f"Nessun testo trovato nella pagina {page_content.get('metadata', {}).get('page', 'sconosciuta')}")
        else:
            # md_output è una stringa Markdown
            md_output, base64_images = extract_and_replace_base64_images(md_output)
            for img in base64_images:
                images_dict[str(image_counter)] = img
                image_counter += 1

        # Creazione delle tab per separare il contenuto testuale e le immagini
        tab1, tab2 = st.tabs(["Contenuto Estratto", "Immagini Estratte"])

        # Preparazione dell'output finale
        output_data = {
            'content': md_output,
            'images': images_dict
        }

        with tab1:
            if page_chunks:
                st.subheader("Contenuto Estratto (JSON)")
                st.json(output_data)
            else:
                st.subheader("Contenuto Estratto (Markdown)")
                st.markdown(md_output)

        with tab2:
            if images_dict:
                st.subheader("Immagini Estratte")
                # Creazione di una lista di opzioni per selezionare un'immagine
                image_options = [f"Immagine {key}" for key in images_dict.keys()]
                selected_image = st.selectbox("Seleziona un'immagine", image_options)

                # Estrazione dell'indice selezionato
                selected_key = selected_image.split(" ")[1]
                img_info = images_dict[selected_key]
                base64_data = img_info['data']
                image_format = img_info['format']

                # Mostra l'immagine selezionata
                st.image(f"data:image/{image_format};base64,{base64_data}", use_column_width=True)

                # Aggiungi i parametri per l'OCR
                psm_option = st.selectbox("Select PSM (Page Segmentation Mode)",
                                          ['1 - Automatic OSD',
                                           '3 - Fully automatic page segmentation',
                                           '6 - Assume a single uniform block of text',
                                           '7 - Treat the image as a single text line',
                                           '8 - Treat the image as a single word',
                                           '11 - Sparse text'])

                psm_value = {
                    '1 - Automatic OSD': '1',
                    '3 - Fully automatic page segmentation': '3',
                    '6 - Assume a single uniform block of text': '6',
                    '7 - Treat the image as a single text line': '7',
                    '8 - Treat the image as a single word': '8',
                    '11 - Sparse text': '11'
                }[psm_option]

                whitelist = st.text_input("Whitelist characters (optional)", value="")

                # Campo per il contesto aggiuntivo
                context = st.text_area("Provide context for the image")

                # Bottone per generare la descrizione
                if st.button("Genera Descrizione"):
                    # Estrazione del testo tramite OCR
                    extracted_text = extract_text_ocr(base64_data, psm_value, whitelist)
                    st.write("Testo Estratto (OCR):")
                    st.write(extracted_text)

                    # Preparazione dei parametri per la chiamata a GPT
                    params = CallGptInput(
                        prompt_context=context,
                        text_extracted_ocr=extracted_text,
                        file=base64_data
                    )

                    try:
                        description = call_gpt(params, 16000)
                        st.write("Descrizione Generata:")
                        st.write(description)
                    except Exception as e:
                        st.error(str(e))

                # Visualizzazione del carosello di immagini
                #st.subheader("Galleria Immagini")
                #images_html = '<div style="display: flex; overflow-x: auto;">'
                #for key in images_dict:
                #    img_info = images_dict[key]
                #    base64_img = img_info['data']
                #    img_format = img_info['format']
                #    images_html += f'<img src="data:image/{img_format};base64,{base64_img}" style="margin-right: 10px; max-height:200px;">'
                #images_html += '</div>'
                #st.markdown(images_html, unsafe_allow_html=True)
            else:
                st.info("Nessuna immagine base64 trovata nel documento.")


    except Exception as e:
        st.error(f"Errore durante l'estrazione: {e}")
        st.stop()
