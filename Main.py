import random
import pygame
from enum import Enum


class GameState(Enum):
    SAME_GUESS = 0
    INVALID_GUESS = 1
    NOT_IN_WORD = 2
    IN_WORD = 3


def Play():
    pygame.init()

    surface = pygame.display.set_mode((800, 800))
    font = pygame.font.SysFont('americantypewriter', 30)
    clock = pygame.time.Clock()
    word_length_num = "5"
    user_text = ""
    new_word = word_length(word_length_num)

    hangman_images = load_hangman_images()
    image_cover = pygame.Rect(0, 150, 800, 300)

    score_array, score_rect_array, output, guessed, letter_array, letter_array_rect = [], [], [], [], [], []
    x_coord, bad_guess, round_val, letters_guessed = 322, 0, 0, 0
    letter_array, letter_array_rect = print_new_word_letters(new_word, x_coord, letter_array, letter_array_rect, font)

    score_array, score_rect_array = new_word_print(new_word, score_array, score_rect_array, output, font, x_coord)

    background_colour = (0, 0, 0)
    input_rect = pygame.Rect(400, 600, 50, 32)
    color_active = pygame.Color(255, 255, 255)
    same_guess, same_guess_rect = text_int("Already made this guess", font, 350, 750)
    correct_guess, correct_guess_rect = text_int("Correct guess!", font, 350, 750)
    invalid_guess, invalid_guess_rect = text_int("Invalid guess. Please try again.", font, 350, 750)
    not_in_word, not_in_word_rect = text_int("Sorry, this letter is not in the word!", font, 350, 750)
    real_word, real_word_rect = text_int("Sorry, the word was " + new_word, font, 350, 750)
    correct_word_text, correct_word_text_rect = text_int("You did it! Congrats!", font, 350, 750)
    text_cover = pygame.Rect(0, 700, 800, 100)

    pygame.display.set_caption('Hangman')
    surface.fill(background_colour)
    pygame.display.flip()
    x = 150

    running = True

    game_loop(running, round_val, surface, score_array, score_rect_array, bad_guess, text_cover, real_word,
              real_word_rect, letters_guessed, new_word, correct_word_text, correct_word_text_rect, input_rect,
              user_text, guessed, same_guess, same_guess_rect, invalid_guess, invalid_guess_rect, not_in_word,
              not_in_word_rect, image_cover, hangman_images, letter_array, letter_array_rect, correct_guess,
              correct_guess_rect, color_active, font, clock, x)


def game_loop(running, round_val, surface, score_array, score_rect_array, bad_guess, text_cover, real_word,
              real_word_rect, letters_guessed, new_word, correct_word_text, correct_word_text_rect, input_rect,
              user_text, guessed, same_guess, same_guess_rect, invalid_guess, invalid_guess_rect, not_in_word,
              not_in_word_rect, image_cover, hangman_images, letter_array, letter_array_rect, correct_guess,
              correct_guess_rect, color_active, font, clock, x):
    while running:
        while round_val < 5:
            surface.blit(score_array[round_val], score_rect_array[round_val])
            round_val += 1

        if bad_guess == 10:
            event_text(surface, real_word, real_word_rect, text_cover)
            end_state(running)

        if letters_guessed == len(new_word):
            surface.blit(correct_word_text, correct_word_text_rect)
            end_state(running)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    guess_made = guess(user_text, guessed)
                    guessed.append(guess_made)
                    if guess_made == GameState.SAME_GUESS:
                        event_text(surface, same_guess, same_guess_rect, text_cover)
                    elif guess_made == GameState.INVALID_GUESS:
                        event_text(surface, invalid_guess, invalid_guess_rect, text_cover)
                    else:
                        correct_word = find_word(user_text, new_word)
                        if correct_word == GameState.NOT_IN_WORD:
                            text, text_rect = prepare_letter(user_text, x, font)
                            print_letter(surface, text, text_rect)
                            x += 50
                            event_text(surface, not_in_word, not_in_word_rect, text_cover)
                            if bad_guess <= 9:
                                pygame.draw.rect(surface, (0, 0, 0), image_cover)
                                surface.blit(hangman_images[bad_guess], (322, 175))
                                bad_guess += 1
                        elif correct_word == GameState.IN_WORD:  # in word
                            location = find_location(guess_made, new_word)
                            for num in location:
                                letters_guessed += 1
                                surface.blit(letter_array[num], letter_array_rect[num])
                            if letters_guessed != len(new_word):
                                event_text(surface, correct_guess, correct_guess_rect, text_cover)
                            elif letters_guessed == len(new_word):
                                pygame.draw.rect(surface, (0, 0, 0), text_cover)
                    user_text = ''
                else:
                    user_text += event.unicode

        pygame.draw.rect(surface, color_active, input_rect)
        text_surface = font.render(user_text, True, (0, 0, 0))
        surface.blit(text_surface, (input_rect.x, input_rect.y))
        input_rect.w = max(1, text_surface.get_width() + 10)
        pygame.display.flip()
        clock.tick(60)

        pygame.display.update()


def word_length(word_length_val):
    if word_length_val == "3":
        new_word = three_letter()
    elif word_length_val == "4":
        new_word = four_letter()
    elif word_length_val == "5":
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
        return GameState.SAME_GUESS
    elif letter in alphabet:
        return letter
    else:
        return GameState.INVALID_GUESS


def find_word(letter, word):
    word_array = []
    y = 0
    z = False
    for x in word:
        word_array.append(x)
        if x == letter:
            z = True
        y += 1
    if z is False:
        return GameState.NOT_IN_WORD
    elif z is True:
        return GameState.IN_WORD


def find_location(letter, word):
    location = []
    y = 0
    for x in word:
        if x == letter:
            location.append(y)
        y += 1
    return location


def new_word_print(new_word, score_array, score_rect_array, output, font, x_coord):
    for _ in new_word:
        output.append("_")
        score = font.render('_', True, (255, 255, 255))
        score_rect = score.get_rect()
        score_rect.center = (x_coord, 500)
        x_coord += 50
        score_array.append(score)
        score_rect_array.append(score_rect)
    return score_array, score_rect_array


def print_new_word_letters(new_word, x_coord, letter_array, letter_array_rect, font):
    for letter in new_word:
        letter_val, letter_rect = text_int(letter, font, x_coord, 500)
        x_coord += 50
        letter_array.append(letter_val)
        letter_array_rect.append(letter_rect)
    return letter_array, letter_array_rect


def event_text(surface, text, rect, text_cover):
    pygame.draw.rect(surface, (0, 0, 0), text_cover)
    surface.blit(text, rect)


def prepare_letter(letter, x_coord, font):
    letter_val, letter_rect = text_int(letter, font, x_coord, 100)
    return letter_val, letter_rect


def print_letter(surface, letter, rect):
    surface.blit(letter, rect)


def load_hangman_images():
    return [pygame.image.load(f"Hangman-Images/Hangman-{i}.png").convert_alpha() for i in range(1, 11)]


def each_display(x):
    font2 = pygame.font.SysFont('americantypewriter', 30)
    text3 = font2.render(x, True, (255, 255, 255))
    text_rect = text3.get_rect()
    return text3, text_rect


def end_state(running):
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                Play()


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


Play()
