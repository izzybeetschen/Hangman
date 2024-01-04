import random
import pygame


def Play():
    pygame.init()

    surface = pygame.display.set_mode((800, 800))
    font = pygame.font.SysFont('americantypewriter', 30)
    clock = pygame.time.Clock()
    word_length_num = "5"
    new_word = word_length(word_length_num)

    user_text = ''
    output = []
    guessed = []  # An array of all guessed letters
    bad_guess = 0
    round_val = 0
    x_coord = 300
    score_array = []
    score_rect_array = []
    for _ in new_word:
        output.append("_")
        score = font.render('_', True, (255, 255, 255))
        score_rect = score.get_rect()
        score_rect.center = (x_coord, 500)
        x_coord += 50
        score_array.append(score)
        score_rect_array.append(score_rect)

    background_colour = (0, 0, 0)
    input_rect = pygame.Rect(350, 600, 50, 32)
    color_active = pygame.Color(255, 255, 255)
    color_passive = pygame.Color(200, 200, 200)
    same_guess = font.render('Already made this guess', True, (255, 255, 255))
    same_guess_overwrite = font.render('Already made this', True, (0, 0, 0))
    same_guess_rect = same_guess.get_rect()
    same_guess_rect.center = (350, 750)

    pygame.display.set_caption('Hangman')
    surface.fill(background_colour)
    pygame.display.flip()

    running = True
    active = False
    guessed_text = False

    while running:
        while round_val < 5:
            surface.blit(score_array[round_val], score_rect_array[round_val])
            round_val += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif bad_guess >= 10:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    guess_made = guess(user_text, guessed)
                    guessed.append(guess_made)
                    guessed_text = False
                    if guess_made == 0:
                        guessed_text = True
                        surface.blit(same_guess, same_guess_rect)
                    elif guess_made == 1:
                        guessed_text = False
                    else:
                        guessed_text = False
                    user_text = ''
                else:
                    user_text += event.unicode

        if active:
            color = color_active
        else:
            color = color_passive

        pygame.draw.rect(surface, color, input_rect)
        text_surface = font.render(user_text, True, (0, 0, 0))
        surface.blit(text_surface, (input_rect.x, input_rect.y))
        input_rect.w = max(1, text_surface.get_width() + 10)
        pygame.display.flip()
        clock.tick(60)

        pygame.display.update()


def word_length(word_length):
    new_word = 0
    if word_length == "3":
        new_word = three_letter()
    elif word_length == "4":
        new_word = four_letter()
    elif word_length == "5":
        new_word = five_letter()
    else:
        print("Error")
        exit()
    return new_word  # Returns the chosen word


def text_int(text1, font1, x, y):
    letter = font1.render(text1, True, (255, 255, 255))
    letter_rect = letter.get_rect()
    letter_rect.center = (x, y)
    return letter, letter_rect


def guess(letter, guessed):
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                'u', 'v', 'w', 'x', 'y', 'z']  # An array of the letters in the alphabet
    if letter in guessed:
        return 0
    elif letter in alphabet:
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


def each_display(x):
    font2 = pygame.font.SysFont('americantypewriter', 30)
    text3 = font2.render(x, True, (255, 255, 255))
    text_rect = text3.get_rect()
    return text3, text_rect


def three_letter():
    words = ["art", "bag", "cat", "dig", "eye", "fox", "god", "him", "inn", "jam", "kit", "leg", "mat", "nip",
             "oil", "pin", "quo", "rid", "sew", "top", "urn", "van", "win", "yap", "zoo"]
    val = random.randrange(0, (len(words) - 1))
    return words[val]


def four_letter():
    words = ["able", "bank", "crib", "dart", "echo", "from", "grab", "high", "jump", "kill", "lime", "nope", "open",
             "pony", "quip", "rose", "stew", "tear", "ulna", "view", "wear", "year", "zero", "zoom"]
    val = random.randrange(0, (len(words) - 1))
    return words[val]


def five_letter():
    words = ["acorn", "broom", "blaze", "break", "beach", "cried", "climb", "court", "diary", "dairy", "echos",
             "flame", "gourd", "hired", "index", "itchy", "jokes", "knock", "kayak", "limbo",
             "marks", "nippy", "newly", "naval", "novel", "nerve", "naked", "oxbow", "ovals" "owned", "point",
             "prowl", "pants", "proud", "quits", "quilt", "quart", "rants", "round", "ranch", "stink", "stick",
             "store", "turnt", "tombs", "unify", "ulcer", "upset", "under", "views", "voice", "wound", "yours",
             "zooms"]
    val = random.randrange(0, (len(words) - 1))
    return words[val]


"""class Game:
    # Initialise the Word class
    def __init__(self):
        self.output = []

    # Runs the game
    def start(self):
        bad_guess = 0
        word_length = "5"
        new_word = self.word_length(word_length)
        for _ in new_word:
            self.output.append("_")
        while "_" in self.output:
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


if __name__ == '__main__':
    game = Game()
    game.start() """

Play()
