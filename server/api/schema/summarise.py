from pydantic import BaseModel


class Input(BaseModel):
    queries: list[str]


class Output(BaseModel):
    summaries: list[str]
