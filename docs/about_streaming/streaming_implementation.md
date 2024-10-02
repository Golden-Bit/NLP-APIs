
# Documentazione Dettagliata sull'Implementazione dello Streaming in Output 

Lo script Python fornito è un'applicazione chatbot costruita utilizzando **Streamlit**, un framework per creare applicazioni web interattive in Python. Lo script dimostra come integrare lo streaming in output quando si interagisce con un'API che supporta risposte in streaming. Questa documentazione analizzerà il metodo utilizzato per implementare lo streaming in output nello script, fornendo spiegazioni dettagliate e approfondimenti che possono aiutarti ad adattare questo approccio ad altri linguaggi di programmazione.

---

## Panoramica

Lo script esegue le seguenti funzioni chiave:

- Configura un'applicazione web Streamlit per l'interfaccia del chatbot.
- Gestisce i messaggi dell'utente e dell'assistente utilizzando lo stato della sessione.
- Invia gli input dell'utente a un'API esterna tramite richieste HTTP POST.
- Riceve le risposte dell'assistente in modalità streaming.
- Aggiorna l'interfaccia del chatbot in tempo reale man mano che nuovi dati arrivano.

---

## Analisi Dettagliata dell'Implementazione dello Streaming

### 1. Importazione delle Librerie Necessarie

```python
import json
from typing import Any
import requests
import streamlit as st
import copy
from config import chatbot_config
```

- **`json`**: Per l'analisi dei dati JSON.
- **`requests`**: Per effettuare richieste HTTP, incluse quelle con risposte in streaming.
- **`streamlit`**: Per costruire l'interfaccia web interattiva.
- **`copy`**: Per effettuare copie profonde dei messaggi predefiniti.
- **`chatbot_config`**: Parametri di configurazione per il chatbot.

---

### 2. Configurazione e Inizializzazione

#### Impostazione dell'Indirizzo API e Configurazione della Pagina

```python
api_address = chatbot_config["api_address"]

st.set_page_config(
    page_title=chatbot_config["page_title"],
    page_icon=chatbot_config["page_icon"],
    layout="wide",
    initial_sidebar_state="auto",
    menu_items=None
)
```

- **`api_address`**: L'URL base dell'API esterna.
- **`st.set_page_config`**: Configura le impostazioni della pagina Streamlit.

#### Inizializzazione delle Variabili di Stato della Sessione

```python
if "messages" not in st.session_state:
    st.session_state.messages = copy.deepcopy(chatbot_config["messages"])

if "ai_avatar_url" not in st.session_state:
    st.session_state.ai_avatar_url = chatbot_config["ai_avatar_url"]

if "user_avatar_url" not in st.session_state:
    st.session_state.user_avatar_url = chatbot_config["user_avatar_url"]
```

- **`st.session_state.messages`**: Memorizza la cronologia della chat.
- **`st.session_state.ai_avatar_url`**: URL per l'avatar dell'assistente.
- **`st.session_state.user_avatar_url`**: URL per l'avatar dell'utente.

---

### 3. Definizione della Funzione Principale

```python
def main():
    # Visualizza i messaggi esistenti
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message(message["role"], avatar=st.session_state.user_avatar_url):
                st.markdown(message["content"])
        else:
            with st.chat_message(message["role"], avatar=st.session_state.ai_avatar_url):
                st.markdown(message["content"])

    # Gestisce l'input dell'utente
    if prompt := st.chat_input("Say something"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Limita la cronologia dei messaggi agli ultimi 10
        if len(st.session_state.messages) > 10:
            st.session_state.messages = st.session_state.messages[-10:]

        # Visualizza il messaggio dell'utente
        with st.chat_message("user", avatar=st.session_state.user_avatar_url):
            st.markdown(prompt)

        # Prepara a ricevere la risposta dell'assistente
        with st.chat_message("assistant", avatar=st.session_state.ai_avatar_url):
            message_placeholder = st.empty()

            # La logica dello streaming sarà implementata qui
```

- **Visualizzazione dei Messaggi**: Itera sulla cronologia dei messaggi e visualizza ciascun messaggio con l'avatar appropriato.
- **Acquisizione dell'Input Utente**: Utilizza `st.chat_input` per ricevere nuovi messaggi dall'utente.
- **Aggiornamento della Cronologia dei Messaggi**: Aggiunge il nuovo messaggio dell'utente allo stato della sessione.
- **Limitazione della Dimensione della Cronologia**: Mantiene solo gli ultimi 10 messaggi per le prestazioni.
- **Placeholder dei Messaggi**: Crea un placeholder per visualizzare la risposta in streaming dell'assistente.

---

### 4. Preparazione della Richiesta API

```python
s = requests.Session()
full_response = ""
url = "http://34.140.110.56:8100/chains/stream_chain"
payload = {
    "chain_id": "hf-embeddings__chat-openai_qa-chain",
    "query": {
        "input": prompt,
        "chat_history": st.session_state.messages
    },
    "inference_kwargs": {},
}
```

- **`requests.Session()`**: Crea un oggetto sessione per mantenere alcuni parametri tra le richieste.
- **`full_response`**: Una stringa per accumulare la risposta dell'assistente.
- **`url`**: L'endpoint dell'API che supporta lo streaming.
- **`payload`**: I dati inviati all'API, inclusi l'input dell'utente e la cronologia della chat.

---

### 5. Invio della Richiesta e Ricezione della Risposta in Modalità Streaming

```python
non_decoded_chunk = b''
with s.post(url, json=payload, headers=None, stream=True) as resp:
    for chunk in resp.iter_lines():
        if chunk:
            # Elabora ciascun chunk qui
```

- **`stream=True`**: Indica alla libreria `requests` di effettuare lo streaming della risposta.
- **`resp.iter_lines()`**: Restituisce un iteratore che produce una linea alla volta dalla risposta.
- **`non_decoded_chunk`**: Un buffer per accumulare byte che possono rappresentare dati parziali.

---

### 6. Elaborazione di Ciascun Chunk della Risposta

#### Verifica della Presenza di Dati Rilevanti

```python
if chunk.decode().startswith('''  "answer":'''):
```

- **Decodifica del Chunk**: Converte i byte in una stringa per l'ispezione.
- **Filtraggio dei Chunk**: Elabora solo i chunk che contengono il campo `"answer"`.

#### Parsing e Accumulo della Risposta

```python
chunk = "{" + chunk.decode() + "}"
chunk = json.loads(chunk)
chunk = chunk["answer"]
chunk = chunk.encode()
print(chunk)
non_decoded_chunk += chunk
```

- **Ricostruzione di JSON Valido**: Racchiude il chunk tra parentesi graffe per formare un oggetto JSON valido.
- **Caricamento dei Dati JSON**: Analizza la stringa JSON in un dizionario Python.
- **Estrazione della Risposta**: Recupera il valore associato alla chiave `"answer"`.
- **Riconversione in Byte**: Converte la stringa di risposta nuovamente in byte per l'accumulo.
- **Accumulazione dei Chunk**: Aggiunge i byte a `non_decoded_chunk` per gestire dati incompleti.

#### Tentativo di Decodifica e Visualizzazione della Risposta

```python
try:
    full_response += non_decoded_chunk.decode()
    message_placeholder.markdown(full_response + "▌", unsafe_allow_html=True)
    non_decoded_chunk = b''
except UnicodeDecodeError:
    # Sequenza UTF-8 incompleta; attende più dati
    pass
```

- **Decodifica dei Byte Accumulati**: Tenta di decodificare `non_decoded_chunk` in una stringa.
- **Aggiornamento della Risposta Completa**: Aggiunge la stringa decodificata a `full_response`.
- **Aggiornamento dell'Interfaccia Utente**: Visualizza lo stato corrente di `full_response` con un cursore (`▌`).
- **Reset del Buffer dei Chunk**: Pulisce `non_decoded_chunk` dopo una decodifica riuscita.
- **Gestione degli Errori di Decodifica**: Se si verifica un `UnicodeDecodeError`, significa che i dati sono incompleti, quindi lo script attende altri chunk.

---

### 7. Finalizzazione della Visualizzazione della Risposta

```python
message_placeholder.markdown(full_response)
st.session_state.messages.append({"role": "assistant", "content": full_response})
```

- **Rimozione del Cursore**: Aggiorna il placeholder per visualizzare la risposta completa senza il cursore.
- **Aggiornamento della Cronologia dei Messaggi**: Aggiunge la risposta completa dell'assistente allo stato della sessione.

---

## Concetti Chiave e Componenti

### Streaming con `requests`

- **`stream=True`**: Abilita lo streaming del contenuto della risposta. La connessione rimane aperta e i dati possono essere letti in modo incrementale.
- **Vantaggi**:
  - Riduce l'utilizzo della memoria evitando di caricare l'intera risposta in una volta.
  - Consente l'elaborazione e la visualizzazione in tempo reale dei dati.

### Iterazione sui Dati di Risposta

- **`resp.iter_lines()`**: Un modo efficiente per iterare sulle linee nella risposta. Gestisce il buffering dei dati per garantire che le linee non siano suddivise a metà.
- **Elaborazione dei Chunk**: Ogni chunk rappresenta un pezzo di dati che può o meno essere un messaggio completo.

### Gestione di Dati Parziali e Codifica

- **Accumulazione dei Byte**: Poiché i dati possono arrivare in chunk incompleti, i byte vengono accumulati fino a formare una sequenza completa e decodificabile.
- **Sfide di Decodifica**: Le sequenze UTF-8 possono essere suddivise tra chunk, portando a errori di decodifica.
- **Gestione degli Errori**:
  - Utilizza un blocco `try-except` per catturare `UnicodeDecodeError`.
  - Continua ad accumulare dati finché non possono essere decodificati con successo.

### Aggiornamenti in Tempo Reale dell'Interfaccia con Streamlit

- **`st.empty()`**: Crea un placeholder nell'app Streamlit che può essere aggiornato dinamicamente.
- **Visualizzazione della Risposta**:
  - Il placeholder viene aggiornato con la risposta dell'assistente man mano che nuovi dati arrivano.
  - Viene aggiunto un cursore (`▌`) per indicare che la risposta è ancora in corso.
- **Finalizzazione della Visualizzazione**: Una volta ricevuti tutti i dati, il cursore viene rimosso.

---


### Esempi in Altri Linguaggi

#### JavaScript (Node.js)

```javascript
const http = require('http');

const options = {
  hostname: '34.140.110.56',
  port: 8100,
  path: '/chains/stream_chain',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
};

const req = http.request(options, (res) => {
  res.setEncoding('utf8');
  let nonDecodedChunk = '';
  res.on('data', (chunk) => {
    nonDecodedChunk += chunk;
    // Processa nonDecodedChunk per estrarre messaggi completi
    // Aggiorna l'interfaccia utente di conseguenza
  });
});

req.on('error', (e) => {
  console.error(`Problema con la richiesta: ${e.message}`);
});

const payload = JSON.stringify({
  chain_id: 'hf-embeddings__chat-openai_qa-chain',
  query: {
    input: userInput,
    chat_history: chatHistory,
  },
  inference_kwargs: {},
});

req.write(payload);
req.end();
```

- **`http.request`**: Invia una richiesta HTTP con la possibilità di gestire risposte in streaming.
- **Gestori di Eventi**: `res.on('data', callback)` viene utilizzato per elaborare i chunk di dati in arrivo.

#### Java

```java
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.ByteBuffer;
import java.util.concurrent.Flow;

HttpClient client = HttpClient.newHttpClient();

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("http://34.140.110.56:8100/chains/stream_chain"))
    .header("Content-Type", "application/json")
    .POST(HttpRequest.BodyPublishers.ofString(payload))
    .build();

client.sendAsync(request, HttpResponse.BodyHandlers.ofByteArrayConsumer((respInfo) -> {
    return new Flow.Subscriber<ByteBuffer>() {
        private ByteBuffer nonDecodedChunk = ByteBuffer.allocate(1024);

        @Override
        public void onSubscribe(Flow.Subscription subscription) {
            subscription.request(Long.MAX_VALUE);
        }

        @Override
        public void onNext(ByteBuffer item) {
            // Accumula i byte
            nonDecodedChunk.put(item);
            // Tenta di decodificare ed elaborare i dati
            // Aggiorna l'interfaccia utente di conseguenza
        }

        @Override
        public void onError(Throwable throwable) {
            throwable.printStackTrace();
        }

        @Override
        public void onComplete() {
            // Finalizza la visualizzazione della risposta
        }
    };
}));
```

- **`HttpClient` con Async**: Invia la richiesta in modo asincrono e gestisce la risposta in modo non bloccante.
- **Flow API**: Utilizzata per gestire dati in streaming con stream reattivi.

#### C#

```csharp
using System;
using System.Net.Http;
using System.Threading.Tasks;

HttpClient client = new HttpClient();

var request = new HttpRequestMessage(HttpMethod.Post, "http://34.140.110.56:8100/chains/stream_chain")
{
    Content = new StringContent(payload, Encoding.UTF8, "application/json")
};

var response = await client.SendAsync(request, HttpCompletionOption.ResponseHeadersRead);
using var stream = await response.Content.ReadAsStreamAsync();
using var reader = new StreamReader(stream);

string line;
while ((line = await reader.ReadLineAsync()) != null)
{
    // Accumula ed elabora i dati
    // Aggiorna l'interfaccia utente di conseguenza
}
```

- **`HttpCompletionOption.ResponseHeadersRead`**: Garantisce che il contenuto non venga bufferizzato e possa essere letto come stream.
- **Lettura delle Linee**: Legge la risposta linea per linea, simile a `iter_lines()` in Python.

#### Angular (TypeScript)

In Angular, si può utilizzare il servizio `HttpClient` per effettuare richieste HTTP. Tuttavia, per gestire le risposte in streaming, è necessario utilizzare l'API di basso livello `XMLHttpRequest` o le `Fetch API`.

Esempio utilizzando `Fetch API` con `ReadableStream`:

```typescript
import { Component } from '@angular/core';

@Component({
  selector: 'app-chat',
  template: `
    <div>{{ responseText }}</div>
  `,
})
export class ChatComponent {
  responseText = '';

  sendMessage(prompt: string) {
    const url = 'http://34.140.110.56:8100/chains/stream_chain';
    const payload = {
      chain_id: 'hf-embeddings__chat-openai_qa-chain',
      query: {
        input: prompt,
        chat_history: [], // Inserire la cronologia della chat se disponibile
      },
      inference_kwargs: {},
    };

    fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })
      .then((response) => {
        const reader = response.body!.getReader();
        const decoder = new TextDecoder();
        let nonDecodedChunk = '';

        const read = () => {
          reader.read().then(({ done, value }) => {
            if (done) {
              return;
            }
            const chunk = decoder.decode(value);
            nonDecodedChunk += chunk;

            // Processa nonDecodedChunk per estrarre messaggi completi
            // Aggiorna l'interfaccia utente
            this.responseText += nonDecodedChunk;
            nonDecodedChunk = '';

            read();
          });
        };

        read();
      })
      .catch((error) => {
        console.error('Errore:', error);
      });
  }
}
```

- **`fetch`**: Utilizza le Fetch API per effettuare richieste HTTP.
- **`ReadableStream`**: Legge la risposta in streaming tramite un reader.
- **Aggiornamento dell'Interfaccia**: `this.responseText` viene aggiornato man mano che i dati arrivano.

#### PHP

In PHP, per gestire risposte in streaming, si può utilizzare la libreria `cURL` con opzioni di basso livello. Tuttavia, l'ambiente PHP non è ideale per applicazioni client in tempo reale, ma è possibile utilizzare `curl_multi` o `Guzzle` per gestire richieste asincrone.

Esempio utilizzando `Guzzle` con `sink` per lo streaming:

```php
<?php
require 'vendor/autoload.php';

use GuzzleHttp\Client;
use Psr\Http\Message\StreamInterface;

$client = new Client();
$url = 'http://34.140.110.56:8100/chains/stream_chain';

$payload = [
    'chain_id' => 'hf-embeddings__chat-openai_qa-chain',
    'query' => [
        'input' => $userInput,
        'chat_history' => $chatHistory, // Inserire la cronologia della chat se disponibile
    ],
    'inference_kwargs' => [],
];

$response = $client->request('POST', $url, [
    'json' => $payload,
    'stream' => true,
]);

$body = $response->getBody();

while (!$body->eof()) {
    $chunk = $body->read(1024);
    // Accumula ed elabora i dati
    // Aggiorna l'interfaccia utente di conseguenza
    echo $chunk;
}
```

- **`GuzzleHttp\Client`**: Una libreria HTTP client per PHP.
- **`'stream' => true`**: Abilita lo streaming della risposta.
- **Lettura dei Dati**: Utilizza `$body->read()` per leggere i chunk di dati.
- **Aggiornamento dell'Interfaccia**: In un contesto web, potrebbe essere necessario utilizzare tecniche come SSE (Server-Sent Events) o WebSocket per inviare i dati al client in tempo reale.

---

### Considerazioni per l'Adattamento

- **Threading e Concorrenza**: Assicurarsi che gli aggiornamenti dell'interfaccia utente vengano eseguiti nel thread principale se richiesto dal framework.
- **Codifica dei Dati**: Gestire correttamente la codifica dei caratteri per evitare errori durante la decodifica dei byte in stringhe.
- **Gestione del Buffer**: Implementare strategie di buffering efficienti per gestire dati parziali.
- **Gestione degli Errori**: Fornire meccanismi robusti per gestire errori di rete, timeout e incoerenze nei dati.
- **Reattività dell'Interfaccia Utente**: Evitare operazioni bloccanti nel thread dell'interfaccia utente per mantenerla reattiva.
