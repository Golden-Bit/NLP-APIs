# Usa l'immagine base di Ubuntu 22.04
FROM ubuntu:22.04

# Imposta il maintainer (facoltativo)
LABEL maintainer="tuo_nome@example.com"

# Imposta non-interattivo per evitare richieste di configurazione manuale
ENV DEBIAN_FRONTEND=noninteractive

# Aggiorna i pacchetti e installa Python 3.10, pip e tzdata
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

# Copia il contenuto del repository nella directory /build_app
WORKDIR /build_app
COPY . /build_app

# Installa le dipendenze dal requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Imposta la variabile di ambiente LD_LIBRARY_PATH
ENV LD_LIBRARY_PATH="/usr/local/lib:$LD_LIBRARY_PATH"

# Espone la porta per FastAPI
EXPOSE 8777

# Comando per avviare FastAPI con uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8777", "--workers", "1"]
