import random


class Game:
    # Initialise the Word class
    def __init__(self):
        self.word = Word()

    def game(self):
        pass

    # Runs the game
    def start(self):
        print("Welcome to Hangman!")
        word_length = input(print("Please choose a level. Choose a word length from 3 - 5 by inputting the correct "
                                  "value: "))
        new_word = self.word_length(word_length)
        guess = input(print("Please guess a letter: "))

    def word_length(self, word_length):
        new_word = 0
        if word_length == "3":
            new_word = self.word.three_letter()
        elif word_length == "4":
            new_word = self.word.four_letter()
        elif word_length == "5":
            new_word = self.word.five_letter()
        else:
            print("Error")
            exit()
        return new_word

    def guess(self, letter):
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                   'u', 'v', 'w', 'x', 'y', 'z']
        guessed = []
        if letter in guessed:
            return 0
        elif letter in letters:
            return letter
        else:
            return 1


class Word:
    @staticmethod
    def three_letter():
        words = ["art", "bag"]
        val = random.randrange(0, 1)
        return words[val]

    @staticmethod
    def four_letter():
        words = ["able", "bank"]
        val = random.randrange(0, 1)
        return words[val]

    @staticmethod
    def five_letter():
        words = ["acorn", "broom"]
        val = random.randrange(0, 1)
        return words[val]


if __name__ == '__main__':
    game = Game()
    game.start()
