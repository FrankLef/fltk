import re


def clean_ws(text: str | None = None) -> str | None:
    """Clean text by remove layout characters and multiple whitespaces.

    Args:
        text (str): String to clean.

    Returns:
        str: Cleaned-up text.
    """
    if not text:
        return None

    # \s matches all whitespace characters: \t, \n, \r, \v, \f, and spaces
    cleaned = re.sub(r"\s+", " ", text).strip()

    # return None when result is empty string
    return cleaned if cleaned else None
