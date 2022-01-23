from typing import List, Optional
from itertools import product
from collections import Counter
from unittest import mock


COMBINATIONS = ["".join(a) for a in product(['_', 'y', 'g'], repeat=5)]

def get_words_from_file(filename) -> List[str]:
    with open(filename) as f:
        return [x.strip() for x in f.readlines()]

class WordleSolver:
    def __init__(self, all_words: List[str], answer: Optional[str] = None, first_guess: Optional[str] = None, num_chars: int = 5) -> None:
        self.answer = answer
        self.all_words = all_words

        if first_guess:
            self.first_guess = first_guess.lower()
            assert len(first_guess) == num_chars, "first_guess must be the same length as num_chars (default 4)"
        else:
            self.first_guess = None

        self.num_chars = num_chars
        assert num_chars > 0, "num_chars must be positive"

    def evaluate_guess(self, guess: str, answer: str) -> str:
        answer_counter = Counter(answer)
        # get the green ones first
        evaluation = ["_" for _ in range(len(guess))]
        for i, (a, b) in enumerate(zip(guess, answer)):
            if a == b:
                evaluation[i] = "g"
                answer_counter[a] -= 1
        # now the yellow ones
        for letter, count in answer_counter.items():
            indices = [i for i, x in enumerate(guess) if x == letter]
            if len(indices) > 0:
                i = 0
                while i < count and i < len(indices):
                    if evaluation[indices[i]] != 'g':
                        evaluation[indices[i]] = 'y'
                    i += 1
        return "".join(evaluation)

    def calculate_guess_score(self, guess: str, valid_words: List[str]) -> float:
        results = Counter([self.evaluate_guess(guess, word) for word in valid_words])
        return sum([x**2 for x in results.values()])


    def get_best_word(self, valid_words) -> str:
        best_word = ""
        min_score = float("inf")
        for guess_word in self.all_words:
            guess_score = self.calculate_guess_score(guess_word, valid_words)
            if guess_score < min_score:
                min_score = guess_score
                best_word = guess_word
        return best_word

    def filter_results(self, guess, result, prev_valid_words):
        return [word for word in prev_valid_words if self.evaluate_guess(guess, word) == result]

    def solve(self):
        valid_words = self.all_words
        guess = self.first_guess if self.first_guess else self.get_best_word(self.all_words)
        while True:
            print(guess)
            print(valid_words)
            if self.answer:
                guess_result = self.evaluate_guess(guess, self.answer)
            else:
                guess_result = input("What was the result of the guess?\n")
            # filter valid words based on guess_result
            valid_words = self.filter_results(guess, guess_result, valid_words)
            if len(valid_words) == 1:
                guess = valid_words[0]
            else:
                guess = self.get_best_word(valid_words)
        


if __name__ == "__main__":
    all_words = get_words_from_file("wordle-words.txt")
    solver = WordleSolver(all_words, first_guess="raise")
    print(solver.solve())
