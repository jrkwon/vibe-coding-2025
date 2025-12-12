"""Character n-gram counter

This module provides a single function `count_char_n_grams` which counts
all character n-grams of length `n` in a given input string.
"""

def count_char_n_grams(text: str, n: int = 3) -> dict[str, int]:
    """Count character n-grams in `text`.

    Parameters
    - text (str): The input string in which to count n-grams. Can contain any
      characters, including repeated characters and whitespace.
    - n (int): The length of each n-gram. Defaults to 3.

    Returns
    - dict[str, int]: A dictionary mapping each n-gram (substring of length
      `n`) to the number of times it appears in `text`.

    Behavior
    - Uses string slicing `text[i:i+n]` to extract overlapping n-grams.
    - Counts all n-grams that start at positions `0 .. len(text)-n`.
    - If `n <= 0` a `ValueError` is raised.
    - If `n` is greater than the length of `text`, an empty dictionary is
      returned.

    Example
    >>> count_char_n_grams("KocseaKocsea", n=4)
    {'Kocs': 2, 'ocse': 2, 'csea': 2, 'seaK': 1, 'eaKo': 1, 'aKoc': 1}
    """

    if not isinstance(n, int):
        raise TypeError("n must be an integer")
    if n <= 0:
        raise ValueError("n must be a positive integer")

    length = len(text)
    if n > length:
        return {}

    counts: dict[str, int] = {}
    # iterate over all valid start indices and slice
    for i in range(length - n + 1):
        ngram = text[i:i + n]
        counts[ngram] = counts.get(ngram, 0) + 1

    return counts


if __name__ == "__main__":
    # quick demonstration
    sample = "KocseaKocsea"
    n = 4
    print("Sample:", sample)
    print("n:", n)
    print("Counts:")
    for k, v in count_char_n_grams(sample, n).items():
        print(f"{k!r}: {v}")
