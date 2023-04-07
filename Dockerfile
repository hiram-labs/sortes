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
RUN set -a && . ./.env && set +a \
    && mkdir -p /run/php

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
    && mkdir -p $(dirname "${PASSAGE_RANK_MODEL_LABELS_PY_LIST_PATH}") \
    && mkdir -p $(dirname "${PASSAGE_RANK_MODEL_OUTPUT_PT_TENSOR_PATH}") \
    && mkdir -p $(dirname "${EXTRACTIVE_Q_A_MODEL_CONTEXTS_PY_LIST_PATH}") \
    && mkdir -p $(dirname "${EXTRACTIVE_Q_A_MODEL_OUTPUT_PT_TENSOR_PATH}") \
    && printf "import os; import pickle;\n\
rank_labels=os.environ['PASSAGE_RANK_MODEL_LABELS_PY_LIST_PATH']\n\
rank_tensors=os.environ['PASSAGE_RANK_MODEL_OUTPUT_PT_TENSOR_PATH']\n\
extract_contexts=os.environ['EXTRACTIVE_Q_A_MODEL_CONTEXTS_PY_LIST_PATH']\n\
extract_tensors=os.environ['EXTRACTIVE_Q_A_MODEL_OUTPUT_PT_TENSOR_PATH']\n\
paths=[rank_labels, rank_tensors, extract_contexts, extract_tensors]\n\
for path in paths:\n\
    with open(path, 'wb') as f:\n\
        pickle.dump(1, f)\n" \
    > tmp.pickel.script \
    && python3 tmp.pickel.script \
    && rm -rf tmp.pickel.script

# setup corpus dir
RUN set -a && . ./.env && set +a \
    && rm -rf ./corpus \
    && mkdir -p "${CORPUS_DIR_PATH}" \
    && mkdir -p $(dirname "${CORPUS_OUTPUT_FILE_PATH}") \
    && chown -R www-data:www-data "${CORPUS_DIR_PATH}" \
    && chown -R www-data:www-data $(dirname "${CORPUS_OUTPUT_FILE_PATH}") \
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
    && git clone https://huggingface.co/philschmid/bart-large-cnn-samsum ${SUMMARISATION_MODEL_DIR_PATH}

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