# Usa l'immagine base di Ubuntu 22.04
FROM ubuntu:22.04

# Imposta il maintainer (facoltativo)
LABEL maintainer="tuo_nome@example.com"

# Aggiorna i pacchetti e installa Python 3.10, pip, e MongoDB
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3.10-venv \
    python3-pip \
    wget \
    gnupg \
    software-properties-common \
    curl \
    lsb-release \
    ca-certificates

# Aggiungi la chiave pubblica di MongoDB
RUN wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | apt-key add -

# Aggiungi il repository di MongoDB per Ubuntu 22.04
RUN echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-6.0.list

# Aggiorna e installa MongoDB
RUN apt-get update && apt-get install -y mongodb-org

# Copia il contenuto del repository nella directory /app
WORKDIR /api
COPY . /api

# Installa le dipendenze dal requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Imposta la variabile di ambiente LD_LIBRARY_PATH
ENV LD_LIBRARY_PATH="/usr/local/lib:$LD_LIBRARY_PATH"

# Avvia il servizio MongoDB
RUN systemctl enable mongod
RUN systemctl start mongod

# Comando di default per avviare il container
CMD ["bash"]
