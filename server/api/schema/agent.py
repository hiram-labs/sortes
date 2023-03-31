from pydantic import BaseModel


class Input(BaseModel):
    query: str


class Output(BaseModel):
    class Candidate(BaseModel):
        class Summary(BaseModel):
            best: str
            all: str
            each: list[str]

        rank: int
        query: str
        label: str
        extracted_answers: list[str]
        summary: Summary

    candidates: list[Candidate]
