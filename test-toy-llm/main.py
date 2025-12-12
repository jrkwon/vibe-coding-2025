import random
from typing import Dict, List

# --- Core LLM Functions ---

def count_char_n_grams(text: str, n: int = 4) -> Dict[str, int]:
    """
    Counts the frequency of all character N-grams (sequences of n characters) 
    in a given text.
    
    Args:
        text: The input string.
        n: The length of the character sequence (N-gram). Defaults to 4.

    Returns:
        A dictionary mapping the N-gram (string) to its count (integer).
    """
    ngram_counts: Dict[str, int] = {}
    
    # Iterate from the first character up to the last possible starting point
    for i in range(len(text) - n + 1):
        ngram = text[i:i + n]
        ngram_counts[ngram] = ngram_counts.get(ngram, 0) + 1
    
    return ngram_counts


def next_letter_frequency(prompt: str, counts: Dict[str, int]) -> Dict[str, int]:
    """
    Calculates the frequency of the next possible character following a given prompt 
    based on a dictionary of N-gram counts.
    
    Args:
        prompt: The previous n-1 characters (the history).
        counts: A dictionary where keys are N-grams (length n) and values 
                are their frequencies.

    Returns:
        A dictionary mapping the possible next character (string) to its 
        frequency (integer) following the prompt.
    """
    next_char_freq: Dict[str, int] = {}
    prompt_len = len(prompt)

    # Check all N-grams to see if they start with the prompt
    for ngram, count in counts.items():
        if ngram.startswith(prompt):
            next_char = ngram[-1]
            next_char_freq[next_char] = next_char_freq.get(next_char, 0) + count
    
    return next_char_freq


def generate_next_char(prompt: str, counts: Dict[str, int]) -> str:
    """
    Predicts and randomly selects the next character based on the weighted 
    frequency of N-grams starting with the given prompt.
    
    Args:
        prompt: The history (n-1 characters) to predict from.
        counts: A dictionary of all N-gram counts.

    Returns:
        The randomly chosen next character (string).
    """
    next_options = next_letter_frequency(prompt, counts)

    # Fallback case: If the model has never seen this prompt before
    if not next_options:
        # Fallback to a random choice of common characters/spaces
        fallback_chars = list("abcdefghijklmnopqrstuvwxyz ")
        return random.choice(fallback_chars)
    
    # Weighted Random Sampling: Create a population list where characters 
    # are repeated by their count.
    population: List[str] = []
    for char, count in next_options.items():
        population.extend([char] * count)

    # Randomly choose one character from the weighted list
    return random.choice(population)


def generate_text(seed_text: str, counts: Dict[str, int], n: int, max_length: int) -> str:
    """
    Generates a continuous string of text using the N-gram model.

    Args:
        seed_text: The initial string to start the generation.
        counts: The dictionary of N-gram frequencies.
        n: The length of the N-gram (used to determine prompt length).
        max_length: The maximum length of the generated text.

    Returns:
        The generated text string.
    """
    # Initialize the generated text with the seed
    generated_text = seed_text
    
    # The prompt length is n-1
    prompt_len = n - 1

    for _ in range(max_length - len(seed_text)):
        # 1. Get the current prompt (the last n-1 characters of the generated text)
        prompt = generated_text[-prompt_len:]
        
        # 2. Generate the next character based on the prompt
        next_char = generate_next_char(prompt, counts)
        
        # 3. Append the character to the generated text
        generated_text += next_char
        
    return generated_text


# --- Driver Program (main.py) ---
if __name__ == "__main__":
    # --- Configuration ---
    # Sample song lyrics dataset (as I cannot download files)
    # Lyrics inspired by "Bohemian Rhapsody" and "Hey Jude"
    SONG_LYRICS_DATASET = (
        "Is this the real life? Is this just fantasy? "
        "Caught in a landslide, no escape from reality. "
        "Open your eyes, look up to the skies and see. "
        "I'm just a poor boy, I need no sympathy. "
        "Because I'm easy come, easy go, little high, little low. "
        "Any way the wind blows doesn't really matter to me, to me."
        "Hey Jude, don't make it bad. Take a sad song and make it better."
    )
    
    # N-gram length (n=4 is a common choice for character-level models)
    N_GRAM_N = 4
    
    # Length of generated text (40 to 60 words, roughly 200 to 300 characters)
    MAX_CHARACTERS = 250
    
    # Starting seed for the generation (must be n-1 characters long)
    # Using 'I'm ' as the seed
    SEED_TEXT = SONG_LYRICS_DATASET[:N_GRAM_N - 1] 

    print("--- 🎶 Toy Character N-gram LLM Generator (main.py) ---")
    print(f"Dataset Size: {len(SONG_LYRICS_DATASET)} characters")
    print(f"N-gram Size (n): {N_GRAM_N}")
    print(f"Max Generated Characters: {MAX_CHARACTERS}\n")

    # Step 1: Count all N-grams in the dataset
    print("1. Counting N-grams...")
    ngram_counts = count_char_n_grams(SONG_LYRICS_DATASET, n=N_GRAM_N)
    print(f"   -> Found {len(ngram_counts)} unique {N_GRAM_N}-grams.")

    # Step 2: Generate the text
    print(f"2. Generating Text (Seed: '{SEED_TEXT}')...")
    generated_output = generate_text(
        seed_text=SEED_TEXT, 
        counts=ngram_counts, 
        n=N_GRAM_N, 
        max_length=MAX_CHARACTERS
    )

    # Step 3: Print the result
    print("\n--- 📝 Generated Song Lyrics ---")
    print(generated_output)
    print("-----------------------------------")