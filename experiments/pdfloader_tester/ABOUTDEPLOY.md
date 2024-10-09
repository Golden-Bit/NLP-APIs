### 1. Eseguire l'Applicazione

Per avviare l'applicazione utilizzando Streamlit con l'host `0.0.0.0` e la porta `8075`, esegui il seguente comando nel terminale:

```bash
streamlit run experiments/pdfloader_tester/app.py --server.address=0.0.0.0 --server.port=8075
```

**Spiegazione dei parametri:**

- `experiments/pdfloader_tester/app.py`: Questo è il percorso al file principale dell'applicazione Streamlit che desideri eseguire. Assicurati di sostituire questo percorso con quello corretto se il tuo file si trova in una directory diversa.
  
- `--server.address=0.0.0.0`: Questo parametro indica a Streamlit di accettare connessioni da qualsiasi indirizzo IP. È particolarmente utile se desideri accedere all'applicazione da altri dispositivi sulla stessa rete locale o se stai eseguendo l'applicazione su un server remoto.
  
- `--server.port=8075`: Specifica la porta su cui l'applicazione sarà in ascolto. La porta `8075` è arbitraria e può essere cambiata se necessario. Assicurati che la porta scelta non sia già in uso da un altro servizio sul tuo sistema.

**Note aggiuntive:**

- **Diritti di amministratore**: In alcuni sistemi operativi, potrebbe essere necessario avere diritti di amministratore per eseguire applicazioni su determinate porte (solitamente quelle inferiori a 1024). La porta `8075` generalmente non richiede privilegi speciali.
  
- **Ambiente virtuale**: Se hai creato un ambiente virtuale Python, assicurati che sia attivato prima di eseguire il comando sopra, in modo che tutte le dipendenze siano correttamente riconosciute.

### 2. Accedere all'Applicazione

Una volta avviata l'applicazione, nel terminale dovresti vedere un output simile a questo:

```
You can now view your Streamlit app in your browser.

  Network URL: http://0.0.0.0:8075
  External URL: http://<TUO_IP_LOCALE>:8075
```

**Per accedere all'applicazione:**

- **Dal dispositivo locale (il computer su cui l'applicazione sta girando):**

  - Apri un browser web (come Chrome, Firefox o Safari).
  - Nella barra degli indirizzi, digita `http://localhost:8075` o `http://127.0.0.1:8075` e premi Invio.
  - Dovresti vedere l'interfaccia utente dell'applicazione apparire nel browser.

- **Da un altro dispositivo sulla stessa rete locale:**

  - Individua l'indirizzo IP locale del computer su cui l'applicazione sta girando. Puoi ottenerlo eseguendo `ipconfig` (su Windows) o `ifconfig` (su Unix/Linux/macOS) nel terminale e cercando l'indirizzo associato alla tua connessione di rete.
  - Apri un browser web sul dispositivo da cui vuoi accedere all'applicazione.
  - Nella barra degli indirizzi, digita `http://<TUO_IP_LOCALE>:8075`, sostituendo `<TUO_IP_LOCALE>` con l'indirizzo IP ottenuto (ad esempio, `http://192.168.1.100:8075`) e premi Invio.
  - Dovresti ora poter interagire con l'applicazione dal dispositivo remoto.

**Assicurazioni:**

- **Firewall e Sicurezza di Rete:**

  - Assicurati che il firewall del computer su cui l'applicazione sta girando non blocchi la porta `8075`. Potrebbe essere necessario aggiungere un'eccezione per questa porta nelle impostazioni del firewall.
  - Se stai utilizzando una rete aziendale o pubblica, potrebbero esserci restrizioni aggiuntive che impediscono l'accesso. In tal caso, consulta l'amministratore di rete.

- **Stabilità dell'Applicazione:**

  - Lascia aperto il terminale o la finestra del comando in cui l'applicazione sta girando. Chiudere questa finestra terminerà l'applicazione.
  - Se desideri eseguire l'applicazione in background o come servizio, considera l'uso di strumenti come `nohup`, `screen` o la configurazione di un servizio di sistema (ad esempio, con `systemd` su Linux).

**Esempio di Accesso:**

Supponendo che l'indirizzo IP locale del tuo computer sia `192.168.1.10`, per accedere all'applicazione da un altro dispositivo sulla stessa rete, apri un browser e vai a:

```
http://192.168.1.10:8075
```

**Suggerimenti:**

- **Browser Compatibili:** Assicurati di utilizzare un browser aggiornato per garantire la compatibilità con le funzionalità di Streamlit.
  
- **Ricaricamento Automatico:** Streamlit supporta il ricaricamento automatico quando il codice viene modificato. Tuttavia, questo è utile solo durante lo sviluppo sul dispositivo locale.

Con questi passaggi, dovresti essere in grado di eseguire e accedere all'applicazione Streamlit su qualsiasi dispositivo collegato alla tua rete, permettendoti di sfruttare appieno le funzionalità di estrazione dei contenuti PDF offerte da `pymupdf4llm`.