def count_char_n_grams(text: str, n: int = 3) -> dict:
    """Count character n-grams in a text.

    Parameters:
        text: Input string to extract n-grams from.
        n: Length of each n-gram (default 3).

    Returns:
        A dictionary mapping each character n-gram to its frequency.

    Behavior:
        - Uses Python string slicing `text[i:i+n]` to extract n-grams.
        - If `n` is <= 0 or `text` is shorter than `n`, an empty dict is returned.
        - Handles any characters including repeated characters.
    """
    counts = {}
    if n <= 0 or text is None:
        return counts
    length = len(text)
    if length < n:
        return counts
    for i in range(0, length - n + 1):
        gram = text[i:i + n]
        counts[gram] = counts.get(gram, 0) + 1
    return counts
