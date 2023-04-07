import os

import numpy as np
import torch
from transformers import AutoModel, AutoTokenizer

from ...utils import packer, pickler


class Instance:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(
            os.environ["PASSAGE_RANK_MODEL_DIR_PATH"]
        )
        self.model = AutoModel.from_pretrained(
            os.environ["PASSAGE_RANK_MODEL_DIR_PATH"]
        )
        self.doc_seqs_pt_tensor = pickler.load(
            os.environ["PASSAGE_RANK_MODEL_OUTPUT_PT_TENSOR_PATH"]
        )
        self.doc_seqs_labels = pickler.load(
            os.environ["PASSAGE_RANK_MODEL_LABELS_PY_LIST_PATH"]
        )

    def preprocess(self):
        doc_dict = packer.load(os.environ["CORPUS_OUTPUT_FILE_PATH"])
        self.doc_seqs_pt_tensor = self.model_encode(doc_dict["seqs"])
        self.doc_seqs_labels = []
        for index, key in enumerate(doc_dict["ranges"]):
            self.doc_seqs_labels.extend([doc_dict["labels"][index] for _ in range(key)])
        pickler.dump(
            os.environ["PASSAGE_RANK_MODEL_OUTPUT_PT_TENSOR_PATH"],
            self.doc_seqs_pt_tensor,
        )
        pickler.dump(
            os.environ["PASSAGE_RANK_MODEL_LABELS_PY_LIST_PATH"], self.doc_seqs_labels
        )

    def cls_pooling(self, model_output):
        return model_output.last_hidden_state[:, 0]

    def model_encode(self, query):
        encoded_input = self.tokenizer(
            query, padding=True, truncation=True, return_tensors="pt"
        )
        with torch.no_grad():
            model_output = self.model(**encoded_input, return_dict=True)
        embeddings = self.cls_pooling(model_output)
        return embeddings

    def input(self, query):
        query_pt_tensor = self.model_encode(query)
        scores = (
            torch.mm(query_pt_tensor, self.doc_seqs_pt_tensor.transpose(0, 1))[0]
            .cpu()
            .tolist()
        )
        sorted_scores_indices = np.argsort(scores)[::-1]
        seqs_rankings = [self.doc_seqs_labels[i] for i in sorted_scores_indices]
        rankings = [
            k for i, k in enumerate(seqs_rankings) if k not in seqs_rankings[:i]
        ]
        return dict(rankings=rankings)


instance = Instance()
