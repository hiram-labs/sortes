import re


def clamp(x: int, start: int, end: int) -> int:
    """
    constrain a number x between the boundaries of `start` and `end`
    """
    return max(start, min(end, x))


def first_sentence(text):
    """
    returns the first sentence in a given string
    strategy used is split at period if and only if the next character is uppercase
    this helps prevent abbreviation edge cases like (I am Mr. Owusu.)
    HINT:
        for a more robust look into nltk punkt
    """
    sentences = re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", text)
    return sentences[0] if len(sentences) > 0 else ""
