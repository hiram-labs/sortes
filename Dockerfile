FROM debian:stable-slim

ENV DEBIAN_FRONTEND noninteractive
ENV NGINX_SERVER_NAME localhost
ENV NGINX_PORT 8080

# install third party apt repositories
RUN curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash \
    && curl -sL https://deb.nodesource.com/setup_14.x | bash 

# update package manager
RUN apt-get update

# install all dependencies available in debian repo
RUN apt-get install -y \
    make \
    gcc \
    git \
    git-lfs \
    curl \
    gnupg2 \
    gettext-base \
    supervisor \
    python3 \
    python3-pip \
    nodejs \
    php7.4-fpm \
    nginx


# copy all files and set the dest as working dir
COPY . /usr/home/sortes
WORKDIR /usr/home/sortes

# setup php-fpm config
RUN mkdir -p /run/php

# setup nginx
RUN set -a && . ./.env && set +a \
    && envsubst < ./nginx.conf > ./sortes.conf \
    && rm -rf ./nginx.conf \
    && mv ./sortes.conf /etc/nginx/conf.d

# setup supervisord config
RUN set -a && . ./.env && set +a \
    && mv ./supervisord.conf ./sortes.conf \
    && mv ./sortes.conf /etc/supervisor/conf.d

# setup caches dir
RUN set -a && . ./.env && set +a \
    && rm -rf ./cache \
    && mkdir -p "${PASSAGE_RANK_MODEL_DIR_PATH}" \
    && mkdir -p "${EXTRACTIVE_Q_A_MODEL_DIR_PATH}"

# setup corpus dir
RUN set -a && . ./.env && set +a \
    && rm -rf ./corpus \
    && mkdir -p "${CORPUS_DIR_PATH}" \
    && chown -R www-data:www-data "${CORPUS_DIR_PATH}" \
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

# download models
RUN set -a && . ./.env && set +a \
    && git clone https://huggingface.co/sentence-transformers/msmarco-distilbert-base-tas-b ${PASSAGE_RANK_MODEL_DIR_PATH} \
    && git clone https://huggingface.co/deepset/tinyroberta-squad2 ${EXTRACTIVE_Q_A_MODEL_DIR_PATH} \
    && git clone git clone https://huggingface.co/philschmid/bart-large-cnn-samsum ${SUMMARISATION_MODEL_DIR_PATH}

# clean up
RUN apt-get -y remove --purge \
    make \
    gcc \
    git \
    git-lfs \
    curl \
    gnupg2 \
    gettext-base \
    && apt-get -y autoremove \
    && apt-get -y clean \
    && rm -rf /var/lib/apt/lists/*

EXPOSE ${NGINX_PORT}

ENTRYPOINT ["./run", "prod"]