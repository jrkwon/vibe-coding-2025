from typing import Dict


def next_letter_frequency(prompt: str, counts: Dict[str, int]) -> Dict[str, int]:
    """Given a prompt of length n-1 and an n-gram counts dict, return next-letter frequencies.

    Parameters:
        prompt: The previous n-1 characters (string) to match against the start of each n-gram.
        counts: Dictionary mapping n-grams (length n) to their frequencies.

    Returns:
        A dictionary mapping the possible next characters (single-character strings)
        to their aggregated frequencies.

    Description:
        For each n-gram in `counts` whose first len(prompt) characters equal `prompt`,
        this function extracts the last character of the n-gram and sums its counts.
    """
    result: Dict[str, int] = {}
    if not prompt or not counts:
        return result
    plen = len(prompt)
    for gram, cnt in counts.items():
        if len(gram) <= plen:
            continue
        if gram[:plen] == prompt:
            next_char = gram[plen]
            result[next_char] = result.get(next_char, 0) + cnt
    return result
