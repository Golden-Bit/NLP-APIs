import streamlit as st
import json
import os

# Importa pymupdf4llm per l'estrazione in Markdown
import pymupdf4llm

st.title("Estrazione di Contenuti da PDF con pymupdf4llm")

# Configurazione dei parametri tramite widget specifici
st.subheader("Configurazione di pymupdf4llm.to_markdown")

# pages
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

# hdr_info
hdr_info_help = "Informazioni per identificare gli header nel documento. Può essere 'None' o un oggetto personalizzato."
hdr_info = st.text_input(
    "hdr_info",
    value="None",
    help=hdr_info_help
)
if hdr_info.strip().lower() == "none":
    hdr_info = None
# Per semplicità, manteniamo hdr_info come None.

# write_images
write_images_help = "Seleziona se salvare le immagini e i grafici come file separati."
write_images = st.checkbox(
    "write_images",
    value=False,
    help=write_images_help
)

# embed_images
embed_images_help = "Seleziona se incorporare le immagini come stringhe base64 nel Markdown."
embed_images = st.checkbox(
    "embed_images",
    value=False,
    help=embed_images_help
)

# image_path
image_path_help = "Percorso della cartella dove salvare le immagini estratte. Necessario se 'write_images' è True."
image_path = st.text_input(
    "image_path",
    value="",
    help=image_path_help
)

# image_format
image_format_help = "Formato delle immagini da salvare (es. 'png', 'jpeg')."
image_format = st.selectbox(
    "image_format",
    options=["png", "jpeg", "jpg", "tiff"],
    index=0,
    help=image_format_help
)

# image_size_limit
image_size_limit_help = "Limite della dimensione delle immagini (valore tra 0 e 1). Immagini più piccole di questo valore (in proporzione alla pagina) verranno ignorate."
image_size_limit = st.slider(
    "image_size_limit",
    min_value=0.0,
    max_value=1.0,
    value=0.05,
    step=0.01,
    help=image_size_limit_help
)

# force_text
force_text_help = "Se True, estrarrà il testo anche dalle immagini."
force_text = st.checkbox(
    "force_text",
    value=True,
    help=force_text_help
)

# page_chunks
page_chunks_help = "Se True, segmenta l'output per pagina e visualizza il risultato come JSON con indentazione."
page_chunks = st.checkbox(
    "page_chunks",
    value=False,
    help=page_chunks_help
)

# margins
margins_help = "Margini da considerare durante l'estrazione (lista o tupla di 1, 2 o 4 valori: sinistra, alto, destra, basso)."
margins_input = st.text_input(
    "margins",
    value="[0, 50, 0, 50]",
    help=margins_help
)
try:
    margins = json.loads(margins_input)
    if isinstance(margins, list) and (len(margins) in [1, 2, 4]):
        if len(margins) == 1:
            margins = margins * 4
        elif len(margins) == 2:
            margins = [0, margins[0], 0, margins[1]]
        margins = tuple(margins)
    else:
        st.error("Il campo 'margins' deve essere una lista di 1, 2 o 4 numeri.")
        st.stop()
except json.JSONDecodeError:
    st.error("Il campo 'margins' deve essere una lista JSON valida di numeri.")
    st.stop()

# dpi
dpi_help = "Risoluzione (DPI) per le immagini generate."
dpi = st.number_input(
    "dpi",
    min_value=1,
    value=150,
    help=dpi_help
)

# page_width
page_width_help = "Larghezza della pagina da assumere se il layout è variabile."
page_width = st.number_input(
    "page_width",
    min_value=1,
    value=612,
    help=page_width_help
)

# page_height
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

# table_strategy
table_strategy_help = "Strategia da utilizzare per il rilevamento delle tabelle."
table_strategy = st.selectbox(
    "table_strategy",
    options=["lines_strict", "text", "lines", "explicit"],
    index=0,
    help=table_strategy_help
)

# graphics_limit
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

# fontsize_limit
fontsize_limit_help = "Limite della dimensione del font per considerare il testo come codice."
fontsize_limit = st.number_input(
    "fontsize_limit",
    min_value=1,
    value=3,
    help=fontsize_limit_help
)

# ignore_code
ignore_code_help = "Seleziona se ignorare la formattazione per font monospaziati."
ignore_code = st.checkbox(
    "ignore_code",
    value=False,
    help=ignore_code_help
)

# extract_words
extract_words_help = "Includi l'output tipo 'words' nei chunks di pagina."
extract_words = st.checkbox(
    "extract_words",
    value=False,
    help=extract_words_help
)

# show_progress
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

    # Utilizzo di pymupdf4llm.to_markdown con i parametri forniti
    try:
        md_output = pymupdf4llm.to_markdown("temp.pdf", **pymupdf4llm_config)
        # Visualizzazione del contenuto estratto
        if page_chunks:
            st.subheader("Contenuto Estratto (JSON)")
            st.json(md_output)
        else:
            st.subheader("Contenuto Estratto (Markdown)")
            st.markdown(md_output)
    except Exception as e:
        st.error(f"Errore durante l'estrazione: {e}")
        st.stop()
