import os

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from ..utils import comparator

MIN_SUMMARY_LENGTH = 56
MAX_SUMMARY_LENGTH = 142


class Instance:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(
            os.environ["SUMMARISATION_MODEL_DIR_PATH"]
        )
        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            os.environ["SUMMARISATION_MODEL_DIR_PATH"]
        )

    def preprocess(self):
        pass

    def tokenize(self, query):
        return self.tokenizer(query, return_tensors="pt").input_ids

    def decode(self, encoded_output):
        encoded_output_to_list = encoded_output.tolist()[0]
        return self.tokenizer.decode(encoded_output_to_list, skip_special_tokens=True)

    def model_encode(self, encoded_input):
        encoded_input_size_halved = comparator.clamp(
            encoded_input.size()[1] / 2, MIN_SUMMARY_LENGTH, MAX_SUMMARY_LENGTH
        )
        return self.model.generate(
            encoded_input,
            max_new_tokens=encoded_input_size_halved,
            do_sample=False,
        )

    def input(self, queries):
        summaries = list()
        for index in range(len(queries)):
            encoded_input = self.tokenize(queries[index])
            encoded_output = self.model_encode(encoded_input)
            summaries.append(self.decode(encoded_output))
        return dict(summaries=summaries)


instance = Instance()
