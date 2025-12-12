import random
import string
from typing import Dict
from next_letter_frequency import next_letter_frequency


def generate_next_char(prompt: str, counts: Dict[str, int]) -> str:
    """Generate a next character given a prompt and n-gram counts.

    Parameters:
        prompt: The previous n-1 characters (string) used to look up next-letter options.
        counts: Dictionary mapping n-grams to their frequencies (from count_char_n_grams).

    Returns:
        A single character string chosen randomly. If `next_letter_frequency` returns
        an empty dict, a random lower-case letter from 'a' to 'z' is returned.

    Behavior:
        - Uses `next_letter_frequency` to obtain possible next characters and their counts.
        - Chooses one next character randomly, weighted by the observed frequencies.
    """
    options = next_letter_frequency(prompt, counts)
    if not options:
        return random.choice(string.ascii_lowercase)
    letters = list(options.keys())
    weights = list(options.values())
    # Weighted random choice
    choice = random.choices(letters, weights=weights, k=1)[0]
    return choice
