# Tiny Toy LLM (character n-gram based)

This small project demonstrates a toy LLM implemented with character n-grams and simple frequency-based sampling.

Files:
- `count_words.py`: Count words by splitting on spaces.
- `count_char_n_grams.py`: Count character n-grams (default n=3).
- `next_letter_frequency.py`: Given a prompt (n-1 chars) and n-gram counts, return next-letter frequencies.
- `generate_next_char.py`: Choose the next character (weighted by frequency).
- `main.py`: Driver to load a sample song lyrics (or `lyrics.txt` if present) and generate 40-60 words.

Run:
```bash
python3 main.py
```

You can place a `lyrics.txt` file in the same folder to use your own dataset.
