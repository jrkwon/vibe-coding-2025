def count_words(text: str) -> dict:
    """
    Counts the frequency of each 'word' in a given text.

    A 'word' is defined as any sequence of characters separated by a space.
    Punctuation is treated as part of the word (e.g., "dog." and "dog" are distinct).

    Args:
        text: The input string of text.

    Returns:
        A dictionary mapping word (string) to its count (integer).
    """
    # 1. Split the text into words using spaces
    words = text.split(" ")

    # 2. Count how many times each word appears
    # We use a dictionary to store the word counts
    word_counts = {}
    for word in words:
        # Check if the word is already in the dictionary
        if word in word_counts:
            # If it is, increment its count
            word_counts[word] += 1
        else:
            # If it's not, initialize its count to 1
            word_counts[word] = 1

    # 3. Return the dictionary
    return word_counts

# --- Example Usage ---
# Input example: ”Lee has a dog. Jane has a dog."
input_text = "Perfect! I've updated the game, I've the game with your requested changes: sound array capabilities, so no external audio files are needed."
result = count_words(input_text)

print(f"Input: '{input_text}'")
print(f"Output: {result}")
# Expected Output: {'Lee': 1, 'has': 2, 'a': 2, 'dog.': 2, 'Jane': 1}