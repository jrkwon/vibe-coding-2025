def count_words(text: str) -> dict[str, int]:
    """
    Splits the text into words using spaces and counts the frequency of each word.
    
    Args:
        text (str): Input text string.
        
    Returns:
        dict[str, int]: A dictionary mapping words to their counts.
    """
    words = text.split(" ")
    counts = {}
    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
    return counts

if __name__ == "__main__":
    # Test case from requirements
    sample = "Lee has a dog. Jane has a dog."
    print(count_words(sample))
