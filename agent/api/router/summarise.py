import logging

from fastapi import APIRouter

from ...model.summarise import transformer
from ..schema.summarise import Input, Output

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/abstractive-summarisation-model",
    tags=["Abstractive summarisation ML model endpoint"],
)


@router.post("/", response_model=Output)
async def root(payload: Input):
    return transformer.instance.input(payload.queries)
