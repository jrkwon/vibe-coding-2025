"""Next-letter frequency from n-gram counts

Provides `next_letter_frequency(prompt, counts)` which, given the previous
`n-1` characters (the `prompt`) and a dictionary of n-gram counts produced
by `count_char_n_grams`, returns a mapping of possible next characters to
their observed frequencies.
"""

from typing import Dict


def next_letter_frequency(prompt: str, counts: Dict[str, int]) -> Dict[str, int]:
    """Compute frequencies of next characters following `prompt`.

    Parameters
    - prompt (str): The previous `n-1` characters. Matches are sought among
      n-gram keys in `counts` where the first `len(prompt)` characters equal
      `prompt`.
    - counts (dict[str, int]): A dictionary mapping n-grams (strings of
      length `n`) to their counts; typically produced by
      `count_char_n_grams(text, n)`.

    Returns
    - dict[str, int]: A dictionary mapping each possible next character
      (the character immediately after `prompt` in a matching n-gram) to
      the summed frequency across all matching n-grams.

    Description
    - Iterates over `counts` keys (n-grams). For each n-gram that starts
      with `prompt`, the character at position `len(prompt)` is taken as the
      next character and its count is added to the result.
    - If `prompt` is empty, the function returns frequencies of the last
      character of every n-gram.
    - The function does not assume a global `n` value other than what is
      implied by the n-gram key lengths in `counts`.
    """

    if not isinstance(prompt, str):
        raise TypeError("prompt must be a string")
    if not isinstance(counts, dict):
        raise TypeError("counts must be a dict mapping n-grams to integers")

    next_freq: Dict[str, int] = {}
    plen = len(prompt)

    if plen == 0:
        # If prompt is empty, consider the last character of every n-gram
        for ngram, cnt in counts.items():
            if not ngram:
                continue
            ch = ngram[-1]
            next_freq[ch] = next_freq.get(ch, 0) + int(cnt)
        return next_freq

    for ngram, cnt in counts.items():
        if len(ngram) <= plen:
            continue
        if ngram.startswith(prompt):
            next_char = ngram[plen]
            next_freq[next_char] = next_freq.get(next_char, 0) + int(cnt)

    return next_freq


if __name__ == "__main__":
    # Demo using the provided example in the task description
    from count_char_n_grams import count_char_n_grams

    text = "Lee has a dog. Jane has a dog. Soomi has a cat."
    n = 4
    counts = count_char_n_grams(text, n)
    prompt = " a "  # previous n-1 characters (3 chars when n=4)

    print("Prompt:", repr(prompt))
    print("Next-letter frequencies:", next_letter_frequency(prompt, counts))
