# NLP-APIs
NLP APIs Read Me File

- Per maggiori informazioni vedere il contenuto della direcotry *docs*
- Per quanto riguarda l'implementazione della **NLP API** si deve considerare come *entry point* lo script *app/main.py*

## Deploy 
### **Dockerfile**

```Dockerfile
# Usa l'immagine base di Ubuntu 22.04
FROM ubuntu:22.04

# Imposta il maintainer (facoltativo)
LABEL maintainer="tuo_nome@example.com"

# Imposta non-interattivo per evitare richieste di configurazione manuale
ENV DEBIAN_FRONTEND=noninteractive

# Aggiorna i pacchetti e installa Python 3.10, pip, MongoDB e tzdata
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3.10-venv \
    python3-pip \
    wget \
    gnupg \
    software-properties-common \
    curl \
    lsb-release \
    ca-certificates \
    tzdata

# Imposta il fuso orario
RUN ln -fs /usr/share/zoneinfo/Europe/Rome /etc/localtime && \
    dpkg-reconfigure --frontend noninteractive tzdata

# Aggiungi la chiave pubblica di MongoDB
RUN wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | apt-key add -

# Aggiungi il repository di MongoDB per Ubuntu 22.04 (Jammy)
RUN echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-6.0.list

# Aggiorna i pacchetti e installa MongoDB
RUN apt-get update && apt-get install -y mongodb-org

# Crea la directory per i dati di MongoDB
RUN mkdir -p /data/db /var/log/mongodb && chown -R mongodb:mongodb /data/db

# Copia il contenuto del repository nella directory /build_app
WORKDIR /build_app
COPY . /build_app

# Installa le dipendenze dal requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Imposta la variabile di ambiente LD_LIBRARY_PATH
ENV LD_LIBRARY_PATH="/usr/local/lib:$LD_LIBRARY_PATH"

# Espone la porta per FastAPI
EXPOSE 8100

# Comando per avviare MongoDB in background e lanciare FastAPI con uvicorn
CMD mongod --fork --logpath /var/log/mongodb/mongod.log --dbpath /data/db && uvicorn app.main:app --host 0.0.0.0 --port 8100 --workers 8
```

### **Esegui il Docker**

Dopo aver modificato il `Dockerfile`, esegui i seguenti comandi per costruire l'immagine e avviare il container.

#### A. **Costruire l'immagine**

```bash
docker build -t my_fastapi_app .
```

#### B. **Avviare il container**

```bash
docker run -d -p 8100:8100 --name fastapi_app my_fastapi_app
```

### **Accedere all'API**

L'API sarà disponibile su `http://localhost:8100` se stai eseguendo il container localmente. Puoi accedere alla tua API utilizzando un browser o un client HTTP come `curl` o `Postman`.
