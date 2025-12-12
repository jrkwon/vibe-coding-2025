import random
from typing import Dict, Any, List

# --- Helper Function (from the previous task) ---
def next_letter_frequency(prompt: str, counts: Dict[str, int]) -> Dict[str, int]:
    """
    Calculates the frequency of the next possible character following a given prompt 
    based on a dictionary of N-gram counts. (Used internally by generate_next_char).
    """
    next_char_freq: Dict[str, int] = {}
    prompt_len = len(prompt)

    for ngram, count in counts.items():
        if ngram[:prompt_len] == prompt:
            next_char = ngram[-1]
            next_char_freq[next_char] = next_char_freq.get(next_char, 0) + count
    
    return next_char_freq

# --- Main Function ---
def generate_next_char(prompt: str, counts: Dict[str, int]) -> str:
    """
    Predicts and randomly selects the next character based on the frequency 
    of N-grams starting with the given prompt.

    Args:
        prompt: The history (n-1 characters) to predict from.
        counts: A dictionary of all N-gram counts (from count_char_n_grams).

    Returns:
        The randomly chosen next character (string).
    """
    # 1. Call next_letter_frequency() to get next-letter options
    next_options = next_letter_frequency(prompt, counts)

    # 2. If the returned dictionary is empty
    if not next_options:
        # If the model has never seen this prompt before, 
        # randomly return a letter a–z (or a space for better flow)
        
        # A simple list of common characters (including space) for out-of-vocabulary fallback
        fallback_chars = list("abcdefghijklmnopqrstuvwxyz ")
        return random.choice(fallback_chars)
    
    # 3. If not empty, randomly choose one of the dictionary’s keys and return it.
    
    # To sample based on frequency, we create a "population" list where 
    # each character is repeated by its count.
    population: List[str] = []
    
    for char, count in next_options.items():
        # Extend the population list by adding the character 'count' times
        population.extend([char] * count)

    # Randomly choose one character from this weighted list
    return random.choice(population)


# --- Example Usage Setup ---
# Simulate the full process (requires a function for initial N-gram counts)
def count_char_n_grams_for_test(text: str, n: int) -> dict:
    counts = {}
    for i in range(len(text) - n + 1):
        ngram = text[i:i + n]
        counts[ngram] = counts.get(ngram, 0) + 1
    return counts

# Example Text & Parameters
full_text = "Lee has a dog. Jane has a dog. Soomi has a cat."
n = 4
all_ngram_counts = count_char_n_grams_for_test(full_text, n=n)

# Prompt is " a " (n-1 = 3 characters)
prompt = " a "

# Running the generation 5 times to show random sampling
print(f"--- Example: Generate Next Character (n={n}) ---")
print(f"Full Text: '{full_text}'")
print(f"Prompt (History): '{prompt}'")
print(f"Possible Next Options: {next_letter_frequency(prompt, all_ngram_counts)}")
print("5 Generations (Expected 'd' ~67%, 'c' ~33%):")

generations = [generate_next_char(prompt, all_ngram_counts) for _ in range(5)]
print(f"Results: {generations}")