from pydantic import BaseModel


class Input(BaseModel):
    query: str


class Output(BaseModel):
    rankings: list
