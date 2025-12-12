def next_letter_frequency(prompt: str, counts: dict[str, int]) -> dict[str, int]:
    """
    Determines the frequency of the next character based on the n-gram counts.
    
    Args:
        prompt (str): The previous n-1 characters.
        counts (dict[str, int]): The n-gram frequencies from count_char_n_grams.
        
    Returns:
        dict[str, int]: A dictionary mapping possible next characters to their frequencies.
    """
    next_chars = {}
    # N is implied by the length of keys in counts. 
    # If keys are length n, prompt should be length n-1.
    
    for ngram, count in counts.items():
        if ngram.startswith(prompt):
            # The next character is the last character of the n-gram
            next_char = ngram[-1]
            if next_char in next_chars:
                next_chars[next_char] += count
            else:
                next_chars[next_char] = count
                
    return next_chars

if __name__ == "__main__":
    # Test case from requirements
    # "Lee has a dog. Jane has a dog. Soomi has a cat." n=4
    # " a d" -> 2, " a c" -> 1
    # We simulate the counts dictionary for the test
    test_counts = {" a d": 2, " a c": 1, "other": 5}
    print(next_letter_frequency(" a ", test_counts))
