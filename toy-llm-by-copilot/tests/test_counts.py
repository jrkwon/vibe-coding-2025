import unittest

from count_words import count_words
from count_char_n_grams import count_char_n_grams


class TestCountWords(unittest.TestCase):
    def test_basic_counts(self):
        text = "The cat sat on the mat. The cat is happy."
        expected = {
            "the": 3,
            "cat": 2,
            "sat": 1,
            "on": 1,
            "mat.": 1,
            "is": 1,
            "happy.": 1,
        }
        self.assertEqual(count_words(text), expected)

    def test_empty_text(self):
        self.assertEqual(count_words(""), {})


class TestCountCharNGrams(unittest.TestCase):
    def test_example_kocsea(self):
        text = "KocseaKocsea"
        expected = {
            "Kocs": 2,
            "ocse": 2,
            "csea": 2,
            "seaK": 1,
            "eaKo": 1,
            "aKoc": 1,
        }
        self.assertEqual(count_char_n_grams(text, n=4), expected)

    def test_default_n(self):
        self.assertEqual(count_char_n_grams("aaaa"), {"aaa": 2})

    def test_n_greater_than_length(self):
        self.assertEqual(count_char_n_grams("hi", n=3), {})

    def test_invalid_n_type(self):
        with self.assertRaises(TypeError):
            count_char_n_grams("abc", n="3")

    def test_invalid_n_value(self):
        with self.assertRaises(ValueError):
            count_char_n_grams("abc", n=0)


if __name__ == "__main__":
    unittest.main()
