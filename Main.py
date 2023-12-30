import random
import pygame


class GUI:
    def initialise(self):
        pygame.init()
        pygame.display.set_mode((400, 500))
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False


class Game:
    # Initialise the Word class
    def __init__(self):
        self.word = Word()
        self.output = []

    # Runs the game
    def start(self):
        bad_guess = 0
        print("Welcome to Hangman!")
        word_length = input("Please choose a level. Choose a word length from 3 - 5 by inputting the correct "
                            "value: ")
        new_word = self.word_length(word_length)
        for _ in new_word:
            self.output.append("_ ")
        print(self.output)
        while "_ " in self.output:
            guess = input("Please guess a letter: ")
            x = self.guess(guess)
            if x == guess:
                z = self.find_word(guess, new_word)
                if z == 0:
                    print("Incorrect. This letter is not in the word")
                    bad_guess += 1
                    print(str(bad_guess) + " incorrect guesses of 10")
                elif z == 1:
                    print(str(self.output))
            elif bad_guess == 10:
                print("Sorry, too many incorrect guesses. The word was " + new_word)
                exit()
            elif x == 0:
                print("You have already guessed this letter.")
            elif x == 1:
                print("Invalid input.")
        print("Congratulations! You did it!")
        print("The word was " + new_word)

    # Sets the length of the word required
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
        return new_word  # Returns the chosen word

    @staticmethod
    def guess(letter):
        alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                    'u', 'v', 'w', 'x', 'y', 'z']  # An array of the letters in the alphabet
        guessed = []  # An array of all guessed letters
        if letter in guessed:
            return 0
        elif letter in alphabet:
            guessed.append(letter)
            return letter
        else:
            return 1

    def find_word(self, letter, word):
        word_array = []
        y = 0
        z = False
        for x in word:
            word_array.append(x)
            if x == letter:
                self.output[y] = letter + " "
                z = True
            y += 1
        if z is False:
            return 0
        elif z is True:
            return 1


class Word:
    @staticmethod
    def three_letter():
        words = ["art", "bag", "cat", "dig", "eye", "fox", "god", "him", "inn", "jam", "kit", "leg", "mat", "nip",
                 "oil", "pin", "quo", "rid", "sew", "top", "urn", "van", "win", "yap", "zoo"]
        val = random.randrange(0, (len(words) - 1))
        return words[val]

    @staticmethod
    def four_letter():
        words = ["able", "bank", "crib", "dart", "echo", "from", "grab", "high", "jump", "kill", "lime", "nope", "open",
                 "pony", "quip", "rose", "stew", "tear", "ulna", "view", "wear", "year", "zero", "zoom"]
        val = random.randrange(0, (len(words) - 1))
        return words[val]

    @staticmethod
    def five_letter():
        words = ["acorn", "broom", "blaze", "break", "beach", "cried", "climb", "court", "diary", "dairy", "echos",
                 "flame", "gourd", "hired", "index", "itchy", "jokes", "knock", "kayak", "limbo",
                 "marks", "nippy", "newly", "naval", "novel", "nerve", "naked", "oxbow", "ovals" "owned", "point",
                 "prowl", "pants", "proud", "quits", "quilt", "quart", "rants", "round", "ranch", "stink", "stick",
                 "store", "turnt", "tombs", "unify", "ulcer", "upset", "under", "views", "voice", "wound", "yours",
                 "zooms"]
        val = random.randrange(0, (len(words) - 1))
        return words[val]


if __name__ == '__main__':
    game = Game()
    # game.start()
    gui = GUI()
    gui.initialise()
