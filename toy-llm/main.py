import random
from count_char_n_grams import count_char_n_grams
from generate_next_char import generate_next_char

def main():
    # Configuration
    n = 4  # N-gram size
    dataset_file = "lyrics.txt"
    output_word_target = 50  # Target roughly 40-60 words
    
    # 1. Load Data
    try:
        with open(dataset_file, "r") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: {dataset_file} not found.")
        return

    # 2. Train Model (Count N-grams)
    print(f"Training on {len(text)} characters...")
    counts = count_char_n_grams(text, n)
    print(f"Model trained. Found {len(counts)} n-grams.")
    
    # 3. Generate Text
    # Start with a random n-gram from the text to kick it off
    start_index = random.randint(0, len(text) - n)
    prompt = text[start_index : start_index + n - 1]
    
    generated_text = prompt
    print(f"\n--- Generating Text (Start: '{prompt}') ---")
    
    while True:
        # Get next char
        next_char = generate_next_char(prompt, counts)
        
        # Append to text
        generated_text += next_char
        
        # Slide prompt
        # Logic: prompt is always the last n-1 characters of generate_text
        prompt = generated_text[-(n-1):]
        
        # Check stopping condition (word count)
        # We roughly estimate words by spaces
        word_count = len(generated_text.split(" "))
        if word_count >= output_word_target:
            break
            
    print("\n" + generated_text)
    print(f"\n[Generated {len(generated_text.split(' '))} words]")

if __name__ == "__main__":
    main()
