"""Generate a next character from n-gram counts.

This module provides `generate_next_char(prompt, counts)` which uses
`next_letter_frequency` to obtain possible next characters given a
`prompt` (the previous n-1 characters) and an n-gram counts dictionary.
It then returns a random next character (uniformly chosen).
"""

from typing import Dict
import random
import string

from next_letter_frequency import next_letter_frequency


def generate_next_char(prompt: str, counts: Dict[str, int]) -> str:
    """Return a randomly chosen next character following `prompt`.

    Parameters
    - prompt (str): The previous `n-1` characters used to look up possible
      continuations in `counts`.
    - counts (dict[str, int]): A dictionary mapping n-grams to their
      frequencies (as returned by `count_char_n_grams`).

    Returns
    - str: A single character string representing the chosen next character.

    Behavior
    - Calls `next_letter_frequency(prompt, counts)` to obtain a dictionary of
      candidate next characters mapped to their observed frequencies.
    - If the returned dictionary is empty, returns a random lowercase letter
      from `a` to `z`.
    - Otherwise, selects and returns a random key from the dictionary
      (uniform selection among possible next characters).
    """

    if not isinstance(prompt, str):
        raise TypeError("prompt must be a string")
    if not isinstance(counts, dict):
        raise TypeError("counts must be a dict mapping n-grams to integers")

    options = next_letter_frequency(prompt, counts)

    if not options:
        return random.choice(string.ascii_lowercase)

    return random.choice(list(options.keys()))


if __name__ == "__main__":
    # Simple demo using the sample text from the previous task
    from count_char_n_grams import count_char_n_grams

    text = "Lee has a dog. Jane has a dog. Soomi has a cat."
    n = 4
    counts = count_char_n_grams(text, n)
    prompt = " a "

    print("Prompt:", repr(prompt))
    # Show a few generated characters
    print("Generated next characters:")
    for i in range(8):
        print(generate_next_char(prompt, counts), end=" ")
    print()
