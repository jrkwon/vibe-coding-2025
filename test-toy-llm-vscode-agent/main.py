import os
import random
from count_char_n_grams import count_char_n_grams
from generate_next_char import generate_next_char
from count_words import count_words


SAMPLE_LYRICS = (
    "Twinkle twinkle little star\n"
    "How I wonder what you are\n"
    "Up above the world so high\n"
    "Like a diamond in the sky\n"
)


def load_lyrics(path: str = "lyrics.txt") -> str:
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return SAMPLE_LYRICS


def generate_text_from_ngrams(source_text: str, n: int = 4, min_words: int = 40, max_words: int = 60) -> str:
    counts = count_char_n_grams(source_text, n)
    if not counts:
        # fallback: repeat source a bit
        return (source_text + " ") * (min_words // max(1, len(source_text.split())))

    target_words = random.randint(min_words, max_words)
    # seed: take the first n-1 chars from source (or random if too short)
    if len(source_text) >= n - 1:
        current = source_text[: n - 1]
    else:
        current = "".join(random.choices("abcdefghijklmnopqrstuvwxyz ", k=n - 1))

    # build until we have enough words
    while len(current.split(" ")) < target_words:
        prompt = current[-(n - 1) :]
        nxt = generate_next_char(prompt, counts)
        current += nxt

    # post-process: collapse multiple spaces and strip
    generated = " ".join([w for w in current.split(" ") if w != ""]).strip()
    return generated


def main():
    text = load_lyrics()
    print("Using source text (first 300 chars):\n", text[:300])
    generated = generate_text_from_ngrams(text, n=4, min_words=40, max_words=60)
    print("\n--- Generated Text ---\n")
    print(generated)
    print("\n--- Word Counts in Generated Text ---\n")
    print(count_words(generated))


if __name__ == "__main__":
    main()
