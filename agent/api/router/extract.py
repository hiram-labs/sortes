import logging

from fastapi import APIRouter

from ...model.extract import transformer
from ..schema.extract import Input, Output

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/extractive-question-answer-model",
    tags=["Extractive question and answer ML model endpoint"],
)


@router.post("/", response_model=Output)
async def root(payload: Input):
    return transformer.instance.input(payload.query, payload.label)
