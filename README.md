## Sortes

A question and answer agent powered by transformer architecture and exposed through RESTful API.

### Requirements

- Node 14
- PHP 7.3.11
- Python 3.9
- Pipenv version 2021.5.29
- Docker

### Models

- [passage ranking](https://huggingface.co/sentence-transformers/msmarco-distilbert-base-tas-b)
- [extraction](https://huggingface.co/deepset/tinyroberta-squad2)
- [summarisation](https://huggingface.co/philschmid/bart-large-cnn-samsum)

### Setup

At the root of the project:

```
    git clone
    cd qa_engine
    pipenv install --dev
    pipenv shell
```

### Running

At the root of the project:

```
pipenv shell
chmod +x ./run      # only required to be executed onces
./run build:cli     # build the cli binary
./run clean:cli     # build the cli binary
./run exec:cli      # execute the cli binary
./run exec:api      # starts fast api server
./run exec:slack    # starts slack bot
```

### Corpus

> **_IMPORTANT_** — There is a corpus size limit of 5MB at the moment and document size limit of 0.5MB

All the documents to be used by the model should go into the corpus folder.
There is a strict naming convention that is a 3 digit prefix and a description with the `.txt` extension appended.

```
000-short-description
```

The very first line of the file is reserved for the associated link. Which will be used to label the document. The first line should only be packed with the link follow by a link break and nothing else.

```
https://some.link.to.be.associated.com

Lorem ipsum dolor sit amet, consectetur
adipiscing elit, sed do eiusmod tempor
incididunt ut labore et dolore magna
aliqua. Ut enim ad minim
....
```

### Commits

Use the below commit prefixes.

- feat: _some commit message_
- ref: _some commit message_
- fix: _some commit message_
- chore: _some commit message_
