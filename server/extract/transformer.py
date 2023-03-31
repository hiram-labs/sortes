import os
import re

import torch
from transformers import (
    AutoModelForQuestionAnswering,
    AutoTokenizer,
    tokenization_utils_base,
)

from ..utils import packer, parser, pickler

BOS_TOKEN_ID = 0
EOS_TOKEN_ID = 2
MAX_WORD_COUNT_PER_CONTEXT = 200
CONTEXT_STRIDE = 75


class Instance:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(
            os.environ["EXTRACTIVE_Q_A_MODEL_DIR_PATH"]
        )
        self.model = AutoModelForQuestionAnswering.from_pretrained(
            os.environ["EXTRACTIVE_Q_A_MODEL_DIR_PATH"]
        )
        self.contexts_pt_tensors = pickler.load(
            os.environ["EXTRACTIVE_Q_A_MODEL_OUTPUT_PT_TENSOR_PATH"]
        )
        self.contexts_labels = pickler.load(
            os.environ["EXTRACTIVE_Q_A_MODEL_CONTEXTS_PY_LIST_PATH"]
        )
        self.current_contexts_labels_index = 0

    def preprocess(self):
        doc_dict = packer.load(os.environ["CORPUS_OUTPUT_FILE_PATH"])
        start = 0
        context_dict = dict()
        for index, end in enumerate(doc_dict["ranges"]):
            data = doc_dict["seqs"][start : start + end]
            context = parser.undo_stride(
                "".join(data),
                int(os.environ["MAX_SEQ_LENGTH"]),
                int(os.environ["DATA_SEQ_STRIDE"]),
            )
            contexts = parser.context_split_with_overlap(
                context, MAX_WORD_COUNT_PER_CONTEXT, CONTEXT_STRIDE
            )
            context_dict[doc_dict["labels"][index]] = dict(
                contexts=contexts, tensors=self.tokenise(contexts)
            )
            start += end
        self.contexts_labels = list(key for key in context_dict.keys())
        self.contexts_pt_tensors = list(
            context_dict[self.contexts_labels[i]]["tensors"]
            for i in range(len(self.contexts_labels))
        )
        pickler.dump(
            os.environ["EXTRACTIVE_Q_A_MODEL_CONTEXTS_PY_LIST_PATH"],
            self.contexts_labels,
        )
        pickler.dump(
            os.environ["EXTRACTIVE_Q_A_MODEL_OUTPUT_PT_TENSOR_PATH"],
            self.contexts_pt_tensors,
        )

    def tokenise(self, query):
        return self.tokenizer(query, padding=True, truncation=True, return_tensors="pt")

    def decode(self, encoded_output):
        return self.tokenizer.decode(encoded_output)

    def model_encode(self, pt_input_ids):
        with torch.no_grad():
            model_output = self.model(**pt_input_ids)
        answer_start_index = model_output.start_logits.argmax()
        answer_end_index = model_output.end_logits.argmax()
        return pt_input_ids.input_ids[0, answer_start_index : answer_end_index + 1]

    def get_context_seq_pt_tensor_at_index(self, index):
        torch_indices = torch.tensor([index])
        input_ids = torch.index_select(
            self.contexts_pt_tensors[self.current_contexts_labels_index]["input_ids"],
            0,
            torch_indices,
        )
        attention_mask = torch.index_select(
            self.contexts_pt_tensors[self.current_contexts_labels_index][
                "attention_mask"
            ],
            0,
            torch_indices,
        )
        return tokenization_utils_base.BatchEncoding(
            dict(
                input_ids=input_ids,
                attention_mask=attention_mask,
            )
        )

    def tensor_concat(self, query_tensor, context_seq_tensor):
        return tokenization_utils_base.BatchEncoding(
            dict(
                input_ids=torch.cat(
                    (query_tensor["input_ids"], context_seq_tensor["input_ids"]), 1
                ),
                attention_mask=torch.cat(
                    (
                        query_tensor["attention_mask"],
                        context_seq_tensor["attention_mask"],
                    ),
                    1,
                ),
            )
        )

    def input(self, query, context_labels):
        answers = list()
        for context_label in context_labels:
            self.current_contexts_labels_index = self.contexts_labels.index(
                context_label
            )
            query_pt_tensor = self.tokenise(query)
            num_of_seqs_in_context = range(
                self.contexts_pt_tensors[self.current_contexts_labels_index][
                    "input_ids"
                ].size()[0]
            )
            for i in num_of_seqs_in_context:
                context_seq_pt_tensor = self.get_context_seq_pt_tensor_at_index(i)
                que_n_ctx_tensor = self.tensor_concat(
                    query_pt_tensor, context_seq_pt_tensor
                )
                encoded_output = self.model_encode(que_n_ctx_tensor)
                answer = self.decode(encoded_output)
                answer = re.sub("<s>", " ", answer)
                answer = answer.strip()
                answers.extend(answer.split("</s>")) if answer else None
        answers = list(set(answer for answer in answers if answer and answer != query))
        return dict(answers=answers)


instance = Instance()
