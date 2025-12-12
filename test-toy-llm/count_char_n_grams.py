def count_char_n_grams(text: str, n: int = 3) -> dict[str, int]:
    """
    Counts the frequency of all character N-grams (sequences of n characters) 
    in a given text.

    Character N-grams are extracted using a sliding window across the text. 
    The count of each unique N-gram is stored.

    Args:
        text: The input string from which N-grams are extracted.
        n: The length of the character sequence (N-gram). Defaults to 3.

    Returns:
        A dictionary mapping the N-gram (string) to its count (integer).
    """
    # Dictionary to store the N-gram counts
    ngram_counts: dict[str, int] = {}
    
    # The loop should iterate up to the index where the start of the N-gram 
    # allows for a sequence of length 'n'. 
    # The last valid starting index is len(text) - n.
    for i in range(len(text) - n + 1):
        # 1. Use string slicing to extract the N-gram
        # The slice text[i:i+n] extracts characters starting at index i, 
        # up to (but not including) index i + n.
        ngram = text[i:i + n]

        # 2. Store counts in a dictionary
        # Check if the N-gram is already in the dictionary
        if ngram in ngram_counts:
            # If it is, increment its count
            ngram_counts[ngram] += 1
        else:
            # If it's not, initialize its count to 1
            ngram_counts[ngram] = 1

    return ngram_counts

# --- Example Usage ---
# Example 1: Standard case
input_text_1 = "KocseaKocsea"
n_1 = 4
result_1 = count_char_n_grams(input_text_1, n=n_1)

print(f"--- Example 1: Character {n_1}-grams ---")
print(f"Input: '{input_text_1}'")
print(f"Output: {result_1}")
# Expected Output includes: {'Kocs': 2, 'ocse': 2, 'csea': 2, 'seaK': 1, 'eaKo': 1, 'aKoc': 1}

# Example 2: Default n=3
input_text_2 = "banana"
result_2 = count_char_n_grams(input_text_2)

print(f"\n--- Example 2: Default Character 3-grams ---")
print(f"Input: '{input_text_2}' (n=3)")
print(f"Output: {result_2}")
# Expected Output: {'ban': 1, 'ana': 2, 'nan': 1}