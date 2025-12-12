from typing import Dict, Any

def next_letter_frequency(prompt: str, counts: Dict[str, int]) -> Dict[str, int]:
    """
    Calculates the frequency of the next possible character following a given prompt 
    based on a dictionary of N-gram counts.

    The prompt must have a length of n-1, where n is the length of the N-grams 
    in the 'counts' dictionary.

    Args:
        prompt: The previous n-1 characters (the history) to predict from.
        counts: A dictionary where keys are N-grams (length n) and values 
                are their frequencies (e.g., from count_char_n_grams).

    Returns:
        A dictionary mapping the possible next character (string) to its 
        frequency (integer) following the prompt.
    """
    next_char_freq: Dict[str, int] = {}
    
    # The length of the prompt (history) is n-1. 
    # This value is used for slicing the N-gram key.
    prompt_len = len(prompt)

    # Iterate over every N-gram and its count in the provided dictionary
    for ngram, count in counts.items():
        # 1. Check if the first n-1 characters of the N-gram match the prompt
        # Use string slicing to extract the first part of the N-gram
        if ngram[:prompt_len] == prompt:
            # 2. Extract the last character, which is the 'next letter'
            next_char = ngram[-1]
            
            # 3. Collect the last character as a key and its count as the value
            # Since the N-gram itself contains the count of this entire sequence,
            # this count is the frequency of the 'next_char' given the 'prompt'.
            
            if next_char in next_char_freq:
                # This should only happen if the prompt is identical and there are 
                # multiple N-grams of length > n that start with 'prompt' + 'next_char'
                # But under the assumption that 'counts' contains N-grams of a fixed length n,
                # this line is mostly for robustness.
                next_char_freq[next_char] += count
            else:
                next_char_freq[next_char] = count

    return next_char_freq

# --- Setup for Example Usage ---
# Use the text from the example: 
# Text: ”Lee has a dog. Jane has a dog. Soomi has a cat."
full_text = "Lee has a dog. Jane has a dog. Soomi has a cat."
n = 4

# Step 1: Create the N-gram counts (simulating the previous function's output)
# We will manually run the logic for n-grams starting with ' a ' for clarity
# Full N-gram count logic (assuming a helper function like count_char_n_grams exists):
def count_char_n_grams_for_test(text: str, n: int) -> dict:
    counts = {}
    for i in range(len(text) - n + 1):
        ngram = text[i:i + n]
        counts[ngram] = counts.get(ngram, 0) + 1
    return counts

all_ngram_counts = count_char_n_grams_for_test(full_text, n=n)

# Step 2: Define the prompt and run the prediction function
prompt = " a d" # Note the leading space! This is a 3-character prompt (n-1)
prompt = " a " # Correct prompt based on example: " a d" appears 2x and " a c" appears 1x.

result = next_letter_frequency(prompt, all_ngram_counts)

print(f"--- Example: Next Letter Frequency (n={n}) ---")
print(f"Full Text: '{full_text}'")
print(f"Prompt (History): '{prompt}'")
print(f"Output: {result}")
# Expected Output: {'d': 2, 'c': 1}
# The two N-grams that match are: ' a d' (2 times) and ' a c' (1 time).