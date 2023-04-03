import logging
import operator
from functools import reduce

logger = logging.getLogger(__name__)


def agent_response(response: dict):
    if not response["candidates"]:
        return f"The question seems to be outside of my scope."

    question = reduce(operator.getitem, ["candidates", 0, "query"], response)

    rank_1_answer = reduce(
        operator.getitem, ["candidates", 0, "summary", "best"], response
    )
    rank_1_reference = reduce(operator.getitem, ["candidates", 0, "label"], response)

    if len(response["candidates"]) > 1:
        rank_2_answer = reduce(
            operator.getitem, ["candidates", 1, "summary", "best"], response
        )
        rank_2_reference = reduce(
            operator.getitem, ["candidates", 1, "label"], response
        )
    else:
        rank_2_answer = None
        rank_2_reference = None

    if rank_1_answer and rank_1_reference and rank_2_answer and rank_2_reference:
        return (
            f"Here are the top 2 answers I found for the question: *{question}*\n\n"
            f"• {rank_1_answer}\n*Reference:* {rank_1_reference}\n\n"
            f"• {rank_2_answer}\n*Reference:* {rank_2_reference}"
        )
    if rank_1_answer and rank_1_reference and not rank_2_answer and rank_2_reference:
        return (
            f"Here is what I found for the question *{question}*\n\n"
            f"{rank_1_answer}\n*Reference:* {rank_1_reference}\n\n"
            f"This reference may also be useful\n{rank_2_reference}"
        )
    if not rank_1_answer and rank_1_reference and rank_2_answer and rank_2_reference:
        return (
            f"Here is what I found for the question *{question}*\n\n"
            f"{rank_2_answer}\n*Reference:* {rank_2_reference}\n\n"
            f"This reference may also be useful\n{rank_1_reference}"
        )
    if (
        rank_1_answer
        and rank_1_reference
        and not rank_2_answer
        and not rank_2_reference
    ):
        return (
            f"Here is what I found for the question *{question}*\n\n"
            f"{rank_1_answer}\n*Reference:* {rank_1_reference}"
        )
    if (
        not rank_1_answer
        and rank_1_reference
        and not rank_2_answer
        and rank_2_reference
    ):
        return (
            f"I could not extract a meaningful answer for the question: *{question}*\n\n"
            f"However, I found these useful references:\n"
            f"{rank_1_reference}\n"
            f"{rank_2_reference}"
        )
    return f"Sorry I did not find any useful references."
