import random
import pygame


class GUI:

    def initialise(self):
        pygame.init()  # initialises pygame
        surface = pygame.display.set_mode((800, 800))  # sets the box size
        width = surface.get_width()
        height = surface.get_height()
        font = pygame.font.SysFont('americantypewriter', 30)
        pygame.display.set_caption('Hangman')
        background_colour = (0, 0, 0)
        running = True  # sets running to true
        surface.fill(background_colour)
        pygame.display.flip()

        title, text_rect1 = self.text_int('Hangman', font, 400, 20)
        a, a_rect = self.text_int('a', font, 50, 600)
        b, b_rect = self.text_int('b', font, 100, 600)
        c, c_rect = self.text_int('c', font, 150, 600)
        d, d_rect = self.text_int('d', font, 200, 600)
        e, e_rect = self.text_int('e', font, 250, 600)
        f, f_rect = self.text_int('f', font, 300, 600)
        g, g_rect = self.text_int('g', font, 350, 600)

        while running:
            surface.fill((0, 0, 0))
            surface.blit(title, text_rect1)
            surface.blit(b, b_rect)
            surface.blit(c, c_rect)
            surface.blit(d, d_rect)
            surface.blit(e, e_rect)
            surface.blit(f, f_rect)
            surface.blit(g, g_rect)
            mouse = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if width / 2 <= mouse[0] <= width / 2 + 140 and height / 2 <= mouse[1] <= height / 2 + 40:
                        pass

            if width / 2 <= mouse[0] <= width / 2 + 140 and height / 2 <= mouse[1] <= height / 2 + 40:
                pygame.draw.rect(surface, background_colour, [width / 2, height / 2, 140, 40])

            else:
                a = font.render('a', True, (200, 200, 200))
                pygame.draw.rect(surface, background_colour, [width / 2, height / 2, 140, 40])

                # superimposing the text onto our button
            surface.blit(a, (width / 2 + 50, height / 2))

            pygame.display.update()

    @staticmethod
    def text_int(text, font, x, y):
        letter = font.render(text, True, (255, 255, 255))
        letter_rect = letter.get_rect()
        letter_rect.center = (x, y)
        return letter, letter_rect


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
