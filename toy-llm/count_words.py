import re

def count_words(text: str) -> dict[str, int]:
    """
    Splits the text into words using spaces, removes non-alphabetic characters,
    and counts the frequency of each word.
    
    Args:
        text (str): Input text string.
        
    Returns:
        dict[str, int]: A dictionary mapping words to their counts.
    """
    words = text.split()
    counts = {}
    for word in words:
        # Remove non-alphabetic characters
        clean_word = re.sub(r'[^a-zA-Z]', '', word)
        if clean_word:
            if clean_word in counts:
                counts[clean_word] += 1
            else:
                counts[clean_word] = 1
    return counts

if __name__ == "__main__":
    # Test case from requirements
    sample = "Lee has a dog. Jane has a dog."
    print(count_words(sample))
