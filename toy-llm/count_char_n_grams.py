def count_char_n_grams(text: str, n: int = 3) -> dict[str, int]:
    """
    Counts all sequences of length n characters in the given text.
    
    Args:
        text (str): Input text string.
        n (int): Length of the character sequence (n-gram). Defaults to 3.
        
    Returns:
        dict[str, int]: A dictionary mapping n-grams to their frequencies.
    """
    counts = {}
    if len(text) < n:
        return counts
        
    for i in range(len(text) - n + 1):
        ngram = text[i:i+n]
        if ngram in counts:
            counts[ngram] += 1
        else:
            counts[ngram] = 1
    return counts

if __name__ == "__main__":
    # Test case from requirements
    sample = "KocseaKocsea"
    print(count_char_n_grams(sample, n=4))
