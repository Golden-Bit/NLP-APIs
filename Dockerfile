# Usa l'immagine base di Ubuntu 22.04
FROM ubuntu:22.04

# Imposta il maintainer (facoltativo)
LABEL maintainer="tuo_nome@example.com"

# Imposta non-interattivo per evitare richieste di configurazione manuale
ENV DEBIAN_FRONTEND=noninteractive

# Imposta il fuso orario
ENV TZ=Europe/Rome

# Aggiorna i pacchetti e installa Python 3.10, pip, e tzdata
# Minimizza la quantità di pacchetti e pulisci i file temporanei
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3.10-venv \
    python3-pip \
    wget \
    gnupg \
    curl \
    lsb-release \
    ca-certificates \
    tzdata && \
    ln -fs /usr/share/zoneinfo/$TZ /etc/localtime && \
    dpkg-reconfigure --frontend noninteractive tzdata && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Scarica dockerize dal link fornito e imposta i permessi di esecuzione
RUN wget https://github.com/jwilder/dockerize/releases/download/v0.8.0/dockerize-alpine-linux-amd64-v0.8.0.tar.gz && \
    tar -xvzf dockerize-alpine-linux-amd64-v0.8.0.tar.gz && \
    mv dockerize /usr/local/bin/dockerize && \
    chmod +x /usr/local/bin/dockerize && \
    rm dockerize-alpine-linux-amd64-v0.8.0.tar.gz

# Copia il contenuto del repository nella directory /build_app
WORKDIR /build_app
COPY . /build_app

# Installa le dipendenze da requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Imposta la variabile di ambiente LD_LIBRARY_PATH, rimuovi se non necessaria
ENV LD_LIBRARY_PATH="/usr/local/lib:$LD_LIBRARY_PATH"

# Espone la porta per FastAPI
EXPOSE 8100

# Comando per avviare FastAPI con dockerize per attendere MongoDB
#CMD ["dockerize", "-wait", "tcp://mongodb:27017", "-timeout", "30s", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8100", "--workers", "1"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8100", "--workers", "1"]
