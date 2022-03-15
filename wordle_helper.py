from enum import IntEnum


def get_words() -> list[str]:
    # Load the file.
    with open("wordle-answers-alphabetical.txt", "r") as f:

        words = f.read().splitlines()

    return words


class ResColor(IntEnum):

    GRAY = 1
    YELLOW = 2
    GREEN = 3


class WordleHelper:
    def __init__(self):

        self.words: list[str] = sorted(get_words())

        # These attributes represent constraints on the daily word.

        # Letters that are known to be in daily word but whose position is not known.
        # somewhat redundant with self.letters_not_at_pos
        self.letters_in_word: set[str] = set()

        # Letters that are known not to be in daily word.
        self.letters_not_in_word: set[str] = set()

        # Letters at correct position.
        self.letters_at_pos: dict[int, str] = {}

        # Letters that are known to be in word but not at pos i.
        self.letters_not_at_pos: dict[int, set[str]] = {i: set() for i in range(5)}

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

                """Accounting for duplicate letters.
                Example: if the daily word is 'wheel'
                and the guess is 'where' then the 1st 'e'
                will be green and the 2nd 'e' will be gray.
                """
                if letter not in self.letters_in_word:

                    self.letters_not_in_word.add(letter)

            elif res_color == ResColor.YELLOW:

                self.letters_in_word.add(letter)

                self.letters_not_at_pos[ltr_pos].add(letter)

            elif res_color == ResColor.GREEN:

                if letter in self.letters_not_in_word:

                    self.letters_not_in_word.remove(letter)

                self.letters_at_pos[ltr_pos] = letter

    def enforce_letters_at_pos(self, words: list[str]) -> list[str]:
        """Removes words from list of words that do not have letters at correct positions"""

        return [word for word in words if self.has_letters_at_pos(word)]

    def has_letters_at_pos(self, word: str) -> bool:

        return all(word[pos] == letter for pos, letter in self.letters_at_pos.items())

    def enforce_letters_not_at_pos(self, words: list[str]) -> list[str]:
        """if word[pos] is in self.letters_not_at_pos[pos] for any pos in range(5)

        then it is not included in returned list of words

        else it is included.

        Examples

        if self.letters_not_at_pos = {0: {'a'} , 1: {'b', 'c'}} then

        'apple' would not be included
        'ebony' would not be included
        'query' would be included
        """
        # TODO: think of a better way to word this.

        return [word for word in words if self.does_not_have_letters_at_pos(word)]

    def does_not_have_letters_at_pos(self, word: str) -> bool:

        return all(
            word[pos] not in letters for pos, letters in self.letters_not_at_pos.items()
        )

    def enforce_letters_in_word(self, words: list[str]) -> list[str]:
        """Removes all words from list of words that do not have all letters in daily word"""

        return [word for word in words if self.has_letters_in_word(word)]

    def has_letters_in_word(self, word: str) -> bool:

        return self.letters_in_word.issubset(set(word))

    def enforce_letters_not_in_word(self, words: list[str]) -> list[str]:
        """Removes all words from list of words that have letters known to not be in daily word"""

        return [word for word in words if self.does_not_have_letters(word)]

    def does_not_have_letters(self, word: str) -> bool:

        return all(letter not in self.letters_not_in_word for letter in word)

    def update_candidate_words(self):

        words: list[str] = self.words

        words = self.enforce_letters_at_pos(words)

        words = self.enforce_letters_not_at_pos(words)

        words = self.enforce_letters_not_in_word(words)

        words = self.enforce_letters_in_word(words)

        self.words = sorted(words)

    def get_candidate_words(self) -> list[str]:

        self.update_candidate_words()

        return self.words
