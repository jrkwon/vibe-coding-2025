"""Simple text generator using character n-grams.

Reads input text (from `--file` or a built-in sample), computes character
n-gram counts, then generates and prints a short sequence (40–60 chars)
by repeatedly sampling next characters using `generate_next_char`.
"""

import argparse
import os
import random
from typing import Optional

from count_char_n_grams import count_char_n_grams
from generate_next_char import generate_next_char
from next_letter_frequency import next_letter_frequency


SAMPLE_TEXT = (
    "Lee has a dog. Jane has a dog. Soomi has a cat. "
    "KocseaKocsea example text to seed the generator."
)


def load_text(path: Optional[str]) -> str:
    if path:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Input file not found: {path}")
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    # try input.txt in cwd
    # prefer a local `my_way.txt` if present (you can place the lyrics there)
    if os.path.exists("my_way.txt"):
        with open("my_way.txt", "r", encoding="utf-8") as f:
            return f.read()
    if os.path.exists("input.txt"):
        with open("input.txt", "r", encoding="utf-8") as f:
            return f.read()
    return SAMPLE_TEXT


def generate_text(text: str, n: int = 4, min_len: int = 40, max_len: int = 60) -> str:
    counts = count_char_n_grams(text, n)

    # Determine starting prompt (n-1 chars)
    prompt = ""
    if counts:
        # pick a random starting n-gram weighted by frequency
        start_ngram = random.choices(list(counts.keys()), weights=list(counts.values()), k=1)[0]
        prompt = start_ngram[: n - 1]
    else:
        # fallback to random letters
        prompt = "".join(random.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(n - 1))

    target_len = random.randint(min_len, max_len)
    result = prompt

    while len(result) < target_len:
        # Prefer weighted selection from observed continuations
        options = next_letter_frequency(prompt, counts)
        if options:
            chars = list(options.keys())
            weights = [options[c] for c in chars]
            next_ch = random.choices(chars, weights=weights, k=1)[0]
        else:
            # fallback to random lowercase letter
            next_ch = random.choice("abcdefghijklmnopqrstuvwxyz")

        result += next_ch
        # slide window
        if n - 1 > 0:
            prompt = (prompt + next_ch)[- (n - 1) :]
        else:
            prompt = ""

    return result[:target_len]


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate short text using char n-grams")
    parser.add_argument("--file", "-f", help="Path to input text file (optional)")
    parser.add_argument("--n", "-n", type=int, default=4, help="n for n-grams (default: 4)")
    parser.add_argument("--min", type=int, default=40, help="Minimum generated length (default: 40)")
    parser.add_argument("--max", type=int, default=60, help="Maximum generated length (default: 60)")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducible output")
    parser.add_argument("--out", "-o", help="Write generated text to this file (optional)")
    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    text = load_text(args.file)
    generated = generate_text(text, n=args.n, min_len=args.min, max_len=args.max)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(generated)
        print(f"Generated text written to: {args.out}")
    else:
        print(generated)


if __name__ == "__main__":
    main()
