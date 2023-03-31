FROM debian:stable-slim

# update package manager
RUN apt-get update

# install all dependencies available in debian repo
RUN apt-get install -y \
    make \
    gcc \
    git \
    curl \
    gnupg2 \
    supervisor \
    python3 \
    python3-pip \
    nginx

# install nodejs 14 from nodejs repo
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash \
    && apt-get install nodejs && rm -rf /var/lib/apt/lists/*

# copy all files and set the dest as working dir
COPY . /usr/home/sortes
WORKDIR /usr/home/sortes

# setup caches dir
RUN set -a && . ./.env && set +a \
    && rm -rf ./cache \
    && mkdir -p "${PASSAGE_RANK_MODEL_DIR_PATH}" \
    && mkdir -p "${EXTRACTIVE_Q_A_MODEL_DIR_PATH}"

# setup corpus dir
RUN set -a && . ./.env && set +a \
    && rm -rf ./corpus \
    && mkdir -p "${CORPUS_DIR_PATH}" \
    && mkdir -p $(dirname "${CORPUS_OUTPUT_FILE_PATH}") \
    && touch "${CORPUS_OUTPUT_FILE_PATH}"

# setup sortes cli
RUN set -a && . ./.env && set +a \
    && ./run clean:cli \
    && ./run build:cli \
    && cp ./cli/bin/sortes /usr/local/bin/sortes \
    && rm -rf ./cli

# setup python environment
RUN set -a && . ./.env && set +a \
    && pip install pipenv \
    && pipenv requirements > requirements.txt \
    && pip3 install -r requirements.txt --no-cache-dir \
    && pip3 uninstall pipenv -y \
    && rm -rf Pipfile*

ENTRYPOINT ["sh"]