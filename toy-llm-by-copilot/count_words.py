def count_words(text):
    """
    Splits the input text into words and returns a dictionary
    where keys are words and values are their counts.
    """
    # 1. Convert to lowercase and remove punctuation (a good practice the LLM might include)
    # For simplicity in this example, we'll focus on splitting
    
    # 2. Split the text into a list of words
    words = text.lower().split() 
    
    # 3. Create the word count dictionary
    word_counts = {}
    for word in words:
        # A common, simple way to count:
        word_counts[word] = word_counts.get(word, 0) + 1
        
    return word_counts

# Example
sample_text = "The cat sat on the mat. The cat is happy."
counts = count_words(sample_text)
print(f"Sample Text: '{sample_text}'")
print(f"Word Counts: {counts}")