# Guida Dettagliata all'Utilizzo dell'Interfaccia UI e Configurazione del Loader con `pymupdf4llm`

## Introduzione

Questa guida fornisce istruzioni dettagliate su come utilizzare un'applicazione Streamlit per estrarre contenuti da documenti PDF utilizzando la libreria `pymupdf4llm`. L'applicazione permette di configurare vari parametri tramite un'interfaccia utente intuitiva e visualizzare il contenuto estratto in formato Markdown o JSON.

## Panoramica dell'Applicazione

L'applicazione è progettata per:

- **Caricare un documento PDF** attraverso l'interfaccia utente.
- **Configurare i parametri** per l'estrazione del contenuto utilizzando widget specifici.
- **Estrarre il contenuto** del PDF utilizzando la funzione `to_markdown` della libreria `pymupdf4llm`.
- **Visualizzare il contenuto estratto** in formato Markdown o JSON, a seconda delle impostazioni.

## Requisiti Prerequisiti

Assicurati di avere installato le seguenti librerie Python:

- `streamlit`
- `pymupdf`
- `pymupdf4llm`

Puoi installarle utilizzando il seguente comando:

```bash
pip install streamlit pymupdf pymupdf4llm
```

## Codice del Backend

Di seguito è riportato il codice completo dell'applicazione:

```python
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
```

## Come Utilizzare l'Interfaccia UI

### Passo 1: Avvio dell'Applicazione

Per avviare l'applicazione, esegui il seguente comando nel terminale:

```bash
streamlit run app.py
```

Assicurati di sostituire `app.py` con il nome del file che contiene il codice dell'applicazione.

### Passo 2: Caricamento del Documento PDF

- Nella pagina web che si apre, troverai un pulsante "Carica un documento PDF".
- Clicca su "Browse files" e seleziona il file PDF che desideri elaborare.

### Passo 3: Configurazione dei Parametri

Sotto la sezione "Configurazione di pymupdf4llm.to_markdown", troverai vari campi che ti permettono di configurare i parametri per l'estrazione del contenuto.

Per ogni campo, c'è un punto interrogativo che, al passaggio del mouse, mostra una descrizione dettagliata del parametro.

#### Parametri Principali

- **pages**: Inserisci una lista di numeri di pagina (partendo da 0) che desideri processare. Lascia vuoto per processare tutte le pagine.
  - *Esempio*: `[0, 2, 4]` per processare le pagine 1, 3 e 5.

- **write_images**: Seleziona questa opzione se desideri salvare le immagini estratte come file separati.

- **embed_images**: Seleziona questa opzione se desideri incorporare le immagini direttamente nel Markdown come stringhe base64.

- **image_path**: Specifica il percorso della cartella dove verranno salvate le immagini estratte. Necessario se `write_images` è selezionato.

- **image_format**: Scegli il formato delle immagini da salvare (es. 'png', 'jpeg').

- **image_size_limit**: Imposta un limite per la dimensione delle immagini da estrarre. Immagini più piccole di questo valore (in proporzione alla pagina) verranno ignorate.

- **force_text**: Se selezionato, estrarrà il testo anche dalle immagini.

- **page_chunks**: Seleziona questa opzione per segmentare l'output per pagina e visualizzare il risultato come JSON con indentazione.

- **margins**: Specifica i margini da considerare durante l'estrazione. Può essere una lista o una tupla di 1, 2 o 4 valori (sinistra, alto, destra, basso).
  - *Esempio*: `[0, 50, 0, 50]` per impostare un margine superiore e inferiore di 50 punti.

#### Altri Parametri

- **dpi**: Imposta la risoluzione (DPI) per le immagini generate.

- **page_width**: Specifica la larghezza della pagina da assumere se il layout è variabile.

- **page_height**: Specifica l'altezza della pagina da assumere se il layout è variabile.

- **table_strategy**: Scegli la strategia da utilizzare per il rilevamento delle tabelle. Opzioni disponibili:
  - `"lines_strict"`
  - `"text"`
  - `"lines"`
  - `"explicit"`

- **graphics_limit**: Ignora la pagina se contiene più di questo numero di grafici vettoriali.

- **fontsize_limit**: Imposta un limite per la dimensione del font per considerare il testo come codice.

- **ignore_code**: Seleziona questa opzione per ignorare la formattazione per font monospaziati.

- **extract_words**: Seleziona questa opzione per includere l'output tipo "words" nei chunks di pagina.

- **show_progress**: Seleziona questa opzione per mostrare l'avanzamento durante l'elaborazione.

### Passo 4: Avvio dell'Estrazione

- Dopo aver configurato i parametri desiderati, l'applicazione elaborerà automaticamente il documento PDF caricato.
- Se l'elaborazione non si avvia automaticamente, verifica che tutti i campi siano compilati correttamente e che il file PDF sia stato caricato con successo.

### Passo 5: Visualizzazione del Contenuto Estratto

- **Se `page_chunks` è selezionato**: Il contenuto estratto verrà visualizzato come JSON con indentazione nella sezione "Contenuto Estratto (JSON)".

- **Se `page_chunks` non è selezionato**: Il contenuto estratto verrà visualizzato in formato Markdown nella sezione "Contenuto Estratto (Markdown)".

## Dettagli sul Backend e Configurazione del Loader

### Funzione `pymupdf4llm.to_markdown`

La funzione `to_markdown` di `pymupdf4llm` è il cuore dell'applicazione. Questa funzione accetta vari parametri che influenzano l'estrazione e la formattazione del contenuto del PDF.

#### Parametri Principali

- **`pages`**: Lista di numeri di pagina da processare. Se `None`, tutte le pagine verranno elaborate.

- **`hdr_info`**: Utilizzato per identificare gli header nel documento. Può essere `None` o un oggetto personalizzato.

- **`write_images`**: Se `True`, le immagini estratte verranno salvate come file separati.

- **`embed_images`**: Se `True`, le immagini verranno incorporate direttamente nel Markdown come stringhe base64.

- **`image_path`**: Percorso della cartella dove salvare le immagini estratte. Necessario se `write_images` è `True`.

- **`image_format`**: Formato delle immagini da salvare (es. 'png', 'jpeg').

- **`image_size_limit`**: Limite della dimensione delle immagini da estrarre.

- **`force_text`**: Se `True`, estrarrà il testo anche dalle immagini.

- **`page_chunks`**: Se `True`, l'output verrà segmentato per pagina e restituito come una lista di dizionari.

- **`margins`**: Margini da considerare durante l'estrazione.

- **`dpi`**: Risoluzione (DPI) per le immagini generate.

- **`page_width` e `page_height`**: Dimensioni della pagina da assumere se il layout è variabile.

- **`table_strategy`**: Strategia per il rilevamento delle tabelle.

#### Altri Parametri

- **`graphics_limit`**: Limite per il numero di grafici vettoriali.

- **`fontsize_limit`**: Limite della dimensione del font per considerare il testo come codice.

- **`ignore_code`**: Se `True`, ignora la formattazione per font monospaziati.

- **`extract_words`**: Se `True`, include l'output tipo "words" nei chunks di pagina.

- **`show_progress`**: Se `True`, mostra l'avanzamento durante l'elaborazione.

### Gestione dei Parametri nell'Applicazione

- **Validazione dei Dati**: L'applicazione include controlli per assicurarsi che i dati inseriti dall'utente siano validi. Se un campo non è compilato correttamente, viene mostrato un messaggio di errore e l'esecuzione viene interrotta.

- **Widget Specifici**: Ogni parametro è configurabile tramite widget specifici di Streamlit, come `text_input`, `checkbox`, `selectbox`, `number_input` e `slider`.

- **Messaggi Esplicativi**: Ogni campo ha un messaggio di aiuto che fornisce una descrizione dettagliata del parametro. Questi messaggi sono accessibili passando il mouse sul punto interrogativo accanto al campo.

### Esecuzione dell'Estrazione

- **Chiamata alla Funzione**: Una volta che tutti i parametri sono stati configurati, l'applicazione chiama la funzione `to_markdown` passando tutti i parametri sotto forma di dizionario.

- **Gestione delle Immagini**: Se `write_images` è `True`, l'applicazione verifica che `image_path` sia specificato e crea la cartella se non esiste.

- **Visualizzazione del Risultato**: Il risultato dell'estrazione viene visualizzato utilizzando `st.markdown` o `st.json`, a seconda del valore di `page_chunks`.

## Suggerimenti e Considerazioni

- **Utilizzo di `page_chunks`**: Se desideri ottenere informazioni più dettagliate per ciascuna pagina, come metadati, tabelle e immagini, seleziona l'opzione `page_chunks`. Questo restituirà una lista di dizionari con informazioni per ogni pagina.

- **Salvataggio delle Immagini**: Se vuoi salvare le immagini estratte come file separati, assicurati di:
  - Selezionare l'opzione `write_images`.
  - Specificare un percorso valido in `image_path`.
  - Verificare che il formato dell'immagine scelto sia supportato.

- **Estrarre Testo da Immagini**: Se il tuo documento PDF contiene testo all'interno di immagini e desideri estrarlo, assicurati che l'opzione `force_text` sia selezionata.

- **Risoluzione delle Immagini**: Se le immagini estratte risultano di bassa qualità, puoi aumentare il valore di `dpi` per migliorarne la risoluzione.

- **Debug e Risoluzione dei Problemi**: Se riscontri errori durante l'estrazione:
  - Verifica che tutti i campi siano compilati correttamente.
  - Controlla i messaggi di errore forniti dall'applicazione per identificare il problema.
  - Se necessario, riduci il numero di pagine da elaborare specificando un sottoinsieme in `pages`.
