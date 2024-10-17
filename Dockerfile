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
    tzdata  # <--- Aggiungi tzdata qui

# Imposta il fuso orario
RUN ln -fs /usr/share/zoneinfo/Europe/Rome /etc/localtime && \
    dpkg-reconfigure --frontend noninteractive tzdata

# Aggiungi la chiave pubblica di MongoDB
RUN wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | apt-key add -

# Aggiungi il repository di MongoDB per Ubuntu 22.04 (Jammy)
RUN echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-6.0.list

# Aggiorna i pacchetti e installa MongoDB
RUN apt-get update && apt-get install -y mongodb-org

# Copia il contenuto del repository nella directory /app
WORKDIR /build_app
COPY . /build_app

# Installa le dipendenze dal requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Imposta la variabile di ambiente LD_LIBRARY_PATH
ENV LD_LIBRARY_PATH="/usr/local/lib:$LD_LIBRARY_PATH"

# Espone la porta per FastAPI
EXPOSE 8080

# Comando per avviare MongoDB in background e lanciare FastAPI con uvicorn
CMD mongod --fork --logpath /var/log/mongod.log && uvicorn app.main:app --host 0.0.0.0 --port 8080 --workers 1
