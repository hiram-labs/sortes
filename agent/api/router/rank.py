import logging

from fastapi import APIRouter

from ...model.rank import transformer
from ..schema.rank import Input, Output

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/passage-ranking-model", tags=["Passage ranking ML model endpoint"]
)


@router.post("/", response_model=Output)
async def root(payload: Input):
    return transformer.instance.input(payload.query)
