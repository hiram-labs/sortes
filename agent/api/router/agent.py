import logging

from fastapi import APIRouter, Request, Response, status

from ...extract import transformer as extract_transformer
from ...rank import transformer as rank_transformer
from ...summarise import transformer as summarise_transformer
from ...utils import comparator
from ..schema.agent import Input, Output

logger = logging.getLogger(__name__)

SUMMARY_QUERY_PREFIX = "You asked the question: "
SUMMARY_ANSWER_PREFIX = "I got this answer: "
NEWLINE = "\n"


def get_parsed_query(query):
    parsed_query = f"{query.rstrip(' ').rstrip('?')}?"
    logger.info(f"[QUESTION]{NEWLINE}{parsed_query}")
    return parsed_query


def get_top_ranked_labels(query):
    # TODO: compare the score on either take top 2 if close enough* or just the top one
    top_2_ranked_context_labels = rank_transformer.instance.input(query)["rankings"][:2]
    logger.info(f"[RANKINGS]{NEWLINE}{NEWLINE.join(top_2_ranked_context_labels)}")
    return top_2_ranked_context_labels


def get_extractive_answers(query, context_label):
    extract_answers = extract_transformer.instance.input(query, [context_label])[
        "answers"
    ]
    logger.info(f"[CONTEXTS]{NEWLINE}{NEWLINE.join(extract_answers)}")
    return extract_answers


def get_extractive_answers_summary(query, extract_answers):
    summary = dict()
    summary["each"] = summarise_transformer.instance.input(
        [
            f"{SUMMARY_QUERY_PREFIX}{query}{NEWLINE}{SUMMARY_ANSWER_PREFIX}{extract_answer}"
            for extract_answer in extract_answers
        ]
    )["summaries"]
    logger.info(f"[EACH_SUMMARIES]{NEWLINE}{NEWLINE.join(summary['each'])}")
    # TODO: this seems to be blocking the app because it takes too long
    # summary["all"] = (
    #     summarise_transformer.instance.input(
    #         f"{SUMMARY_QUERY_PREFIX}{query}{NEWLINE}{SUMMARY_ANSWER_PREFIX}{' '.join(extract_answers)}"
    #     )["summaries"][0]
    #     if len(extract_answers) > 1
    #     else ""
    # )
    summary["all"] = ""
    logger.info(f"[ALL_SUMMARIES]{NEWLINE}{summary['all']}")
    summary["best"] = (
        # TODO: do a reflection of the summary
        # - strip out non full sentences
        # - compare if the summary is compatible with the context to reduce hallucination
        comparator.first_sentence(summary["each"][0])
        if summary["each"]
        else ""
    )
    return summary


router = APIRouter(
    prefix="/qa-agent",
    tags=["Question and Answer endpoint"],
)


@router.get("/preprocess")
async def preprocess(request: Request):
    rank_transformer.instance.preprocess()
    extract_transformer.instance.preprocess()
    summarise_transformer.instance.preprocess()
    return Response(status_code=status.HTTP_200_OK)


@router.post("/query", response_model=Output)
async def query(payload: Input):
    candidates = list()
    query = get_parsed_query(payload.query)
    labels = get_top_ranked_labels(query)
    for index, label in enumerate(labels):
        answers = get_extractive_answers(query, label)
        summary = get_extractive_answers_summary(query, answers)
        candidates.append(
            dict(
                rank=index + 1,
                query=query,
                label=label,
                extracted_answers=answers,
                summary=summary,
            )
        )
    return dict(candidates=candidates)
