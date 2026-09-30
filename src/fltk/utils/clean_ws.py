import re


def clean_ws(text: str | None = None) -> str | None:
    """Clean text by remove layout characters and multiple whitespaces.

    Args:
        text (str | None, optional): String to clean. Defaults to None.

    Returns:
        str | None: Cleaned-up string.
    """
    if not text:
        return None

    # \s matches all whitespace characters: \t, \n, \r, \v, \f, and spaces
    cleaned = re.sub(r"\s+", " ", text).strip()

    # return None when result is empty string
    return cleaned if cleaned else None
