import random
import string
from next_letter_frequency import next_letter_frequency

def generate_next_char(prompt: str, counts: dict[str, int]) -> str:
    """
    Generates the next character based on the prompt and n-gram counts.
    
    Args:
        prompt (str): The previous n-1 characters (context).
        counts (dict[str, int]): Disctionary of n-gram counts.
        
    Returns:
        str: The predicted next character.
    """
    possible_chars_counts = next_letter_frequency(prompt, counts)
    
    if not possible_chars_counts:
        # Return a random letter a-z if no data found
        return random.choice(string.ascii_lowercase)
    
    # Weighted choice: Step 5 requirement
    # keys are characters, values are weights (counts)
    options = list(possible_chars_counts.keys())
    weights = list(possible_chars_counts.values())
    
    # random.choices returns a list, we take the first element
    return random.choices(options, weights=weights, k=1)[0]

if __name__ == "__main__":
    test_counts = {" a d": 2, " a c": 1}
    # Should print 'd' or 'c'
    print(generate_next_char(" a ", test_counts))
