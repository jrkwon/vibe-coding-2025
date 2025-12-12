def count_words(text: str) -> dict:
    """Count words in a text by splitting on spaces.

    Parameters:
        text: Input string to count words from.

    Returns:
        A dictionary mapping each word (split by a single space) to its frequency.

    Note:
        This intentionally does not handle punctuation — tokens like "dog." and "dog"
        are treated as distinct as per the exercise requirements.
    """
    counts = {}
    if text is None:
        return counts
    # Split on any whitespace (spaces, newlines, tabs) and ignore empty tokens
    words = text.split()
    for w in words:
        token = w
        counts[token] = counts.get(token, 0) + 1
    return counts
