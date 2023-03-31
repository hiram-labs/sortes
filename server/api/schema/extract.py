from pydantic import BaseModel


class Input(BaseModel):
    query: str
    label: list[str]


class Output(BaseModel):
    answers: list[str]
