"""Given the results of guesses in Wordle, this class
returns the list of words satisfying the conditions."""
from enum import IntEnum


def get_words_list() -> list[str]:
    """Returns a list of words from the file wordle-answers-alphabetical.txt."""

    with open("wordle-answers-alphabetical.txt", "r", encoding="utf-8") as file:

        words = file.read().splitlines()

    return words


class ResColor(IntEnum):  # pylint: disable=missing-docstring

    GRAY = 1
    YELLOW = 2
    GREEN = 3


class WordleHelper:
    """Given the results of guesses in Wordle, this class
    returns the list of words satisfying the conditions."""

    def __init__(self):

        self._words: list[str] = sorted(get_words_list())

        # These attributes represent constraints on the daily word.

        # Letters that are known to be in daily word but whose position is not known.
        # redundant with self._letters_not_at_pos
        # left in for clarity
        self._letters_in_word: set[str] = set()

        # Letters that are known not to be in daily word.
        self._letters_not_in_word: set[str] = set()

        # Letters at correct position.
        self._letters_at_pos: dict[int, str] = {}

        # Letters that are known to be in word but not at pos i.
        self._letters_not_at_pos: dict[int, set[str]] = {i: set() for i in range(5)}

    def add_result(self, guess: str, result: str):
        """guess is the word guessed as a string in lowercase.

        result is the result shown by wordle encoded as a string in this way:

        gray -> 1

        yellow -> 2

        green -> 3

        Example:

        if you guessed 'atone' and the daily word is 'about'

        then guess = 'atone'

        and result = '32211'

                updates the constraints
        """

        for ltr_pos, res_str in enumerate(result):

            res_color = int(res_str)

            letter = guess[ltr_pos]

            if res_color == ResColor.GRAY:

                # Accounting for duplicate letters.
                # Example: if the daily word is 'wheel'
                # and the guess is 'where' then the 1st 'e'
                # will be green and the 2nd 'e' will be gray.

                if letter not in self._letters_in_word:

                    self._letters_not_in_word.add(letter)

            elif res_color == ResColor.YELLOW:

                self._letters_in_word.add(letter)

                self._letters_not_at_pos[ltr_pos].add(letter)

            elif res_color == ResColor.GREEN:

                # Accounting for duplicate letters. See above.

                if letter in self._letters_not_in_word:

                    self._letters_not_in_word.remove(letter)

                self._letters_at_pos[ltr_pos] = letter

    def _enforce_letters_at_pos(self):
        """Removes words from list of words that do not have letters at correct positions"""

        self._words = [word for word in self._words if self._has_letters_at_pos(word)]

    def _has_letters_at_pos(self, word: str) -> bool:

        return all(word[pos] == letter for pos, letter in self._letters_at_pos.items())

    def _enforce_letters_not_at_pos(self):
        # if word[pos] is in self._letters_not_at_pos[pos] for any pos in range(5)

        # then it is not included in returned list of words

        # else it is included.

        # Examples

        # if self._letters_not_at_pos = {0: {'a'} , 1: {'b', 'c'}} then

        # 'apple' would not be included
        # 'ebony' would not be included
        # 'query' would be included

        self._words = [
            word for word in self._words if self._does_not_have_letters_at_pos(word)
        ]

    def _does_not_have_letters_at_pos(self, word: str) -> bool:

        return all(
            word[pos] not in letters
            for pos, letters in self._letters_not_at_pos.items()
        )

    def _enforce_letters_in_word(self):
        """Removes all words from list of words that do not have all letters in daily word"""

        self._words = [word for word in self._words if self._has_letters_in_word(word)]

    def _has_letters_in_word(self, word: str) -> bool:

        return self._letters_in_word.issubset(set(word))

    def _enforce_letters_not_in_word(self):
        """Removes all words from list of words that have letters known to not be in daily word"""

        self._words = [
            word for word in self._words if self._does_not_have_letters(word)
        ]

    def _does_not_have_letters(self, word: str) -> bool:

        return all(letter not in self._letters_not_in_word for letter in word)

    def _update_candidate_words(self):

        self._enforce_letters_at_pos()

        self._enforce_letters_not_at_pos()

        self._enforce_letters_not_in_word()

        self._enforce_letters_in_word()

        self._words = sorted(self._words)

    def get_words(self) -> list[str]:
        """Returns the list of words satisfying the conditions."""

        self._update_candidate_words()

        return self._words
