
import random
import pygame
from enum import Enum


class GameState(Enum):
    SAME_GUESS = 0
    INVALID_GUESS = 1
    NOT_IN_WORD = 2
    IN_WORD = 3


class Colours(Enum):
    WHITE = 255, 255, 255
    RED = 255, 0, 0
    GREEN = 0, 255, 0
    BLUE = 0, 0, 255
    YELLOW = 255, 255, 0
    BLACK = 0, 0, 0


def play(surface):
    """
        Initialize and execute the Hangman game.

        Parameters:
            surface (pygame.Surface): The main surface for rendering graphics.

        The function initializes game-related variables, sets up the game window, and then enters the game loop
        by calling the `game_loop` function with the appropriate parameters.

        Returns:
            None
        """
    font = pygame.font.SysFont('americantypewriter', 30)
    clock = pygame.time.Clock()
    word_length_num = str(random.randrange(3, 6))
    user_text = ""
    new_word = word_length(word_length_num)

    hangman_images = load_hangman_images()
    image_cover = pygame.Rect(0, 150, 800, 300)

    score_array, score_rect_array, output, guessed, letter_array, letter_array_rect = [], [], [], [], [], []
    bad_guess, round_val, letters_guessed = 0, 0, 0
    x_coord = x_length_coord(word_length_num)
    letter_array, letter_array_rect = print_new_word_letters(new_word, x_coord, letter_array, letter_array_rect, font)

    score_array, score_rect_array = new_word_print(new_word, score_array, score_rect_array, output, font, x_coord)

    background_colour = pygame.Color(*Colours.BLACK.value)
    input_rect = pygame.Rect(350, 600, 100, 32)
    color_active = pygame.Color(*Colours.WHITE.value)
    same_guess, same_guess_rect = text_int("Already made this guess", font, 400, 750)
    correct_guess, correct_guess_rect = text_int("Correct guess!", font, 400, 750)
    invalid_guess, invalid_guess_rect = text_int("Invalid guess. Please try again.", font, 400, 750)
    not_in_word, not_in_word_rect = text_int("Sorry, this letter is not in the word!", font, 450, 750)
    text_cover = pygame.Rect(150, 700, 800, 100)

    pygame.display.set_caption('Hangman')
    surface.fill(background_colour)
    pygame.display.flip()
    x = 150

    return_menu = pygame.Rect(50, 700, 100, 50)
    return_menu_text = font.render("MENU", True, pygame.Color(*Colours.BLACK.value))
    return_menu_text_rect = return_menu_text.get_rect(center=return_menu.center)

    running = True

    game_loop(running, round_val, surface, score_array, score_rect_array, bad_guess, text_cover, letters_guessed,
              new_word, input_rect, user_text, guessed, same_guess, same_guess_rect, invalid_guess,
              invalid_guess_rect, not_in_word, not_in_word_rect, image_cover, hangman_images, letter_array,
              letter_array_rect, correct_guess, correct_guess_rect, color_active, font, clock, x, word_length_num,
              return_menu, return_menu_text, return_menu_text_rect)


def game_loop(running, round_val, surface, score_array, score_rect_array, bad_guess, text_cover, letters_guessed,
              new_word, input_rect, user_text, guessed, same_guess, same_guess_rect, invalid_guess,
              invalid_guess_rect, not_in_word, not_in_word_rect, image_cover, hangman_images, letter_array,
              letter_array_rect, correct_guess, correct_guess_rect, color_active, font, clock, x, word_length_num,
              return_menu, return_menu_text, return_menu_text_rect):
    """
        Main game loop for the hangman game.

        Parameters:
            running (bool): Flag indicating whether the game loop should continue running.
            round_val (int): Current round value.
            surface (pygame.Surface): The main surface for rendering graphics.
            score_array (list): List of surfaces representing the underscore for each letter.
            score_rect_array (list): List of rectangles representing the position of each letter's underscore.
            bad_guess (int): Number of incorrect guesses made.
            text_cover (pygame.Rect): Rectangle covering the text area for displaying events.
            letters_guessed (int): Number of letters correctly guessed.
            new_word (str): The word to be guessed in the current round.
            input_rect (pygame.Rect): Rectangle representing the input text area.
            user_text (str): Current user input text.
            guessed (list): List of letters already guessed by the user.
            same_guess (str): Message for when the user makes the same guess again.
            same_guess_rect (pygame.Rect): Rectangle for positioning the same guess message.
            invalid_guess (str): Message for when the user makes an invalid guess.
            invalid_guess_rect (pygame.Rect): Rectangle for positioning the invalid guess message.
            not_in_word (str): Message for when the guessed letter is not in the word.
            not_in_word_rect (pygame.Rect): Rectangle for positioning the 'not in word' message.
            image_cover (pygame.Rect): Rectangle covering the area for displaying hangman images.
            hangman_images (list): List of hangman images for each incorrect guess.
            letter_array (list): List of surfaces representing individual letters in the word.
            letter_array_rect (list): List of rectangles representing the position of each letter.
            correct_guess (str): Message for when the guessed letter is correct.
            correct_guess_rect (pygame.Rect): Rectangle for positioning the correct guess message.
            color_active (tuple): colour of the input box
            font (pygame.Font): Font used for rendering text
            clock (pygame.time.Clock): Pygame clock object for controlling the frame rate.
            x (int): Horizontal position for rendering letters not in the word.
            word_length_num (int): Number of letters in the word to be guessed.
            return_menu (pygame.Rect): Rectangle for the return to menu button.
            return_menu_text (pygame.Surface): Surface for the text on the return to menu button.
            return_menu_text_rect (pygame.Rect): Rectangle for positioning the return to menu text.

            Returns:

        Handles interaction from the user and loops until the game is over
        """
    while running:
        pygame.draw.rect(surface, pygame.Color(*Colours.WHITE.value), return_menu)
        surface.blit(return_menu_text, return_menu_text_rect)

        while round_val < int(word_length_num):
            surface.blit(score_array[round_val], score_rect_array[round_val])
            round_val += 1

        if bad_guess == 10:
            running = False
            game_over_state(surface, font, False, new_word)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                if return_menu.collidepoint(position):
                    running = False
                    menu_state()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    user_text = user_text.lower()
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
                                pygame.draw.rect(surface, pygame.Color(*Colours.BLACK.value), text_cover)
                                running = False
                                game_over_state(surface, font, True, new_word)
                    user_text = ''
                else:
                    user_text += event.unicode

        pygame.draw.rect(surface, color_active, input_rect)
        text_surface = font.render(user_text, True, pygame.Color(*Colours.BLACK.value))
        surface.blit(text_surface, (input_rect.x, input_rect.y))
        input_rect.w = max(1, text_surface.get_width() + 10)
        pygame.display.flip()
        clock.tick(60)

        pygame.display.update()


def menu_state():
    """
        Display the main menu of the Hangman game.

        Parameters:

        Returns:

        This function initializes the game window, creates menu buttons, and enters the menu loop by calling the
        `menu_loop` function with the appropriate parameters.
        """
    surface = pygame.display.set_mode((800, 800))
    font = pygame.font.SysFont('americantypewriter', 30)
    title_font = pygame.font.SysFont('americantypewriter', 60)
    how_to_font = pygame.font.SysFont('americantypewriter', 25)

    play_button = pygame.Rect(275, 250, 250, 50)
    play_button_txt = font.render("PLAY", True, (pygame.Color(*Colours.BLACK.value)))
    play_button_txt_rect = play_button_txt.get_rect(center=play_button.center)

    how_to_button = pygame.Rect(275, 400, 250, 50)
    how_button_txt = font.render("HOW TO PLAY", True, pygame.Color(*Colours.BLACK.value))
    how_button_txt_rect = how_button_txt.get_rect(center=how_to_button.center)

    quit_button = pygame.Rect(275, 550, 250, 50)
    quit_button_text = font.render("QUIT", True, pygame.Color(*Colours.BLACK.value))
    quit_button_txt_rect = quit_button_text.get_rect(center=quit_button.center)

    title, title_rect = text_int("HANGMAN", title_font, 400, 100)

    menu_run = True

    menu_loop(menu_run, surface, play_button, how_to_button, quit_button, play_button_txt, play_button_txt_rect,
              how_button_txt, how_button_txt_rect, quit_button_text, quit_button_txt_rect, title, title_rect, font,
              how_to_font)


def menu_loop(menu_run, surface, play_button, how_to_button, quit_button, play_button_txt, play_button_txt_rect,
              how_button_txt, how_button_txt_rect, quit_button_text, quit_button_txt_rect, title, title_rect, font,
              how_to_font):
    """
        Main loop for the Hangman game menu.

        Parameters:
            menu_run (bool): Flag indicating whether the menu loop should continue running.
            surface (pygame.Surface): The main surface for rendering graphics.
            play_button (pygame.Rect): Rectangle representing the "PLAY" button.
            how_to_button (pygame.Rect): Rectangle representing the "HOW TO PLAY" button.
            quit_button (pygame.Rect): Rectangle representing the "QUIT" button.
            play_button_txt (pygame.Surface): Surface for the text on the "PLAY" button.
            play_button_txt_rect (pygame.Rect): Rectangle for positioning the "PLAY" button text.
            how_button_txt (pygame.Surface): Surface for the text on the "HOW TO PLAY" button.
            how_button_txt_rect (pygame.Rect): Rectangle for positioning the "HOW TO PLAY" button text.
            quit_button_text (pygame.Surface): Surface for the text on the "QUIT" button.
            quit_button_txt_rect (pygame.Rect): Rectangle for positioning the "QUIT" button text.
            title (pygame.Surface): Surface for the title text.
            title_rect (pygame.Rect): Rectangle for positioning the title text.
            font (pygame.Font): Font used for rendering general text.
            how_to_font (pygame.Font): Font used for rendering "How to Play" instructions.

        Returns:
            None

        Handles interactions from users on the starting menu
        """
    while menu_run:
        surface.fill(pygame.Color(*Colours.BLACK.value))
        pygame.draw.rect(surface, pygame.Color(*Colours.WHITE.value), play_button)
        pygame.draw.rect(surface, pygame.Color(*Colours.WHITE.value), how_to_button)
        pygame.draw.rect(surface, pygame.Color(*Colours.WHITE.value), quit_button)

        surface.blit(play_button_txt, play_button_txt_rect)
        surface.blit(how_button_txt, how_button_txt_rect)
        surface.blit(quit_button_text, quit_button_txt_rect)
        surface.blit(title, title_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                if play_button.collidepoint(position):
                    menu_run = False
                    play(surface)
                elif how_to_button.collidepoint(position):
                    menu_run = False
                    surface.fill(pygame.Color(*Colours.BLACK.value))
                    how_to_play(surface, font, how_to_font)

                elif quit_button.collidepoint(position):
                    menu_run = False
        pygame.display.flip()


def how_to_play(surface, title, font):
    """
        Initialises the "How to Play" instructions for the Hangman game.

        Parameters:
            surface (pygame.Surface): The main surface for rendering graphics.
            title (pygame.Surface): Surface for the title text.
            font (pygame.Font): Font used for rendering instructions.

        Returns:
            None
        """

    line1, line1_rect = text_int("HOW TO PLAY", title, 400, 50)
    line2, line2_rect = text_int("Input a letter into the white text box on the screen.", font, 400, 150)
    line3, line3_rect = text_int("Press enter to submit this letter guess.", font, 400, 200)
    line4, line4_rect = text_int("If the guess is correct, it will appear on the screen.", font, 400, 250)
    line5, line5_rect = text_int("If the guess is invalid, a message will appear.", font, 400, 300)
    line6, line6_rect = text_int("If the guess is incorrect, part of the hangman will show.", font, 400, 350)
    line7, line7_rect = text_int("You get 10 incorrect guesses before game over.", font, 400, 400)
    line8, line8_rect = text_int("GOOD LUCK!", font, 400, 550)

    back_button = pygame.Rect(300, 700, 200, 50)
    back_button_text = title.render("BACK", True, pygame.Color(*Colours.BLACK.value))
    back_button_text_rect = back_button_text.get_rect(center=back_button.center)

    running = True

    how_to_loop(running, surface, line1, line2, line3, line4, line5, line6, line7, line8, line1_rect, line2_rect,
                line3_rect, line4_rect, line5_rect, line6_rect, line7_rect, line8_rect, back_button, back_button_text,
                back_button_text_rect)


def how_to_loop(running, surface, line1, line2, line3, line4, line5, line6, line7, line8, line1_rect, line2_rect,
                line3_rect, line4_rect, line5_rect, line6_rect, line7_rect, line8_rect, back_button, back_button_text,
                back_button_text_rect):
    """
        Main loop for displaying the "How to Play" instructions in the Hangman game.

        Parameters:
            running (bool): Flag indicating whether the loop should continue running.
            surface (pygame.Surface): The main surface for rendering graphics.
            line1, line2, line3, line4, line5, line6, line7, line8 (pygame.Surface): Surfaces for rendering each line of
             instructions.
            line1_rect, line2_rect, line3_rect, line4_rect, line5_rect, line6_rect, line7_rect, line8_rect
            (pygame.Rect): Rectangles for positioning each line of instructions.
            back_button (pygame.Rect): Rectangle representing the "BACK" button.
            back_button_text (pygame.Surface): Surface for the text on the "BACK" button.
            back_button_text_rect (pygame.Rect): Rectangle for positioning the "BACK" button text.

        Returns:
            None
        """
    while running:
        surface.fill(pygame.Color(*Colours.BLACK.value))
        surface.blit(line1, line1_rect)
        surface.blit(line2, line2_rect)
        surface.blit(line3, line3_rect)
        surface.blit(line4, line4_rect)
        surface.blit(line5, line5_rect)
        surface.blit(line6, line6_rect)
        surface.blit(line7, line7_rect)
        surface.blit(line8, line8_rect)

        pygame.draw.rect(surface, pygame.Color(*Colours.WHITE.value), back_button)
        surface.blit(back_button_text, back_button_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                if back_button.collidepoint(position):
                    running = False
                    menu_state()
        pygame.display.flip()


def game_over_state(surface, font, win, correct_word):
    """
        Display the game over state with relevant information.

        Parameters:
            surface (pygame.Surface): The main surface for rendering graphics.
            font (pygame.Font): Font used for rendering text.
            win (bool): Flag indicating whether the player won the game.
            correct_word (str): The correct word in the game.

        Returns:
            None
        """
    title_font = pygame.font.SysFont('americantypewriter', 60)
    game_over, game_over_rect = text_int("GAME OVER!", title_font, 400, 50)

    if win:
        win_text, win_text_rect = text_int("You win!", font, 400, 100)
    elif not win:
        win_text, win_text_rect = text_int("You lose!", font, 400, 100)
    else:
        win_text, win_text_rect = text_int("Uh oh, something went wrong", font, 400, 100)

    correct_word_text, correct_word_rect = text_int("The correct word was " + correct_word, font, 400, 200)

    play_again = pygame.Rect(100, 400, 200, 50)
    play_again_text = font.render("PLAY AGAIN", True, pygame.Color(*Colours.BLACK.value))
    play_again_text_rect = play_again_text.get_rect(center=play_again.center)

    menu_button = pygame.Rect(500, 400, 200, 50)
    menu_text = font.render("MENU", True, pygame.Color(*Colours.BLACK.value))
    menu_text_rect = menu_text.get_rect(center=menu_button.center)

    game_over_run = True

    game_over_loop(game_over_run, surface, game_over, game_over_rect, win_text, win_text_rect, correct_word_text,
                   play_again, play_again_text, correct_word_rect, play_again_text_rect, menu_text, menu_button,
                   menu_text_rect)


def game_over_loop(game_over_run, surface, game_over, game_over_rect, win_text, win_text_rect, correct_word_text,
                   play_again, play_again_text, correct_word_rect, play_again_text_rect, menu_text, menu_button,
                   menu_text_rect):
    """
        Main loop for displaying the game over state in the Hangman game.

        Parameters:
            game_over_run (bool): Flag indicating whether the loop should continue running.
            surface (pygame.Surface): The main surface for rendering graphics.
            game_over (pygame.Surface): Surface for the "GAME OVER!" text.
            game_over_rect (pygame.Rect): Rectangle for positioning the "GAME OVER!" text.
            win_text (pygame.Surface): Surface for the "You win!" or "You lose!" text.
            win_text_rect (pygame.Rect): Rectangle for positioning the "You win!" or "You lose!" text.
            correct_word_text (pygame.Surface): Surface for displaying the correct word.
            play_again (pygame.Rect): Rectangle representing the "PLAY AGAIN" button.
            play_again_text (pygame.Surface): Surface for the text on the "PLAY AGAIN" button.
            correct_word_rect (pygame.Rect): Rectangle for positioning the correct word text.
            play_again_text_rect (pygame.Rect): Rectangle for positioning the "PLAY AGAIN" button text.
            menu_text (pygame.Surface): Surface for the text on the "MENU" button.
            menu_button (pygame.Rect): Rectangle representing the "MENU" button.
            menu_text_rect (pygame.Rect): Rectangle for positioning the "MENU" button text.

        Returns:
            None
        """
    while game_over_run:
        surface.fill(pygame.Color(*Colours.BLACK.value))
        surface.blit(game_over, game_over_rect)
        surface.blit(win_text, win_text_rect)
        surface.blit(correct_word_text, correct_word_rect)

        pygame.draw.rect(surface, pygame.Color(*Colours.WHITE.value), play_again)
        surface.blit(play_again_text, play_again_text_rect)

        pygame.draw.rect(surface, pygame.Color(*Colours.WHITE.value), menu_button)
        surface.blit(menu_text, menu_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over_run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                if menu_button.collidepoint(position):
                    game_over_run = False
                    menu_state()
                if play_again.collidepoint(position):
                    game_over_run = False
                    play(surface)
        pygame.display.flip()


def word_length(word_length_val):
    """
        Select a random word of a specified length.

        Parameters:
            word_length_val (str): The desired length of the word.

        Returns:
            str: A randomly selected word of the specified length.
        """
    if word_length_val == "3":
        return three_letter()
    elif word_length_val == "4":
        return four_letter()
    elif word_length_val == "5":
        return five_letter()


def text_int(text1, font1, x, y):
    """
        Create a text surface with a specified font and position.

        Parameters:
            text1 (str): The text to be rendered.
            font1 (pygame.Font): Font used for rendering the text.
            x (int): The x-coordinate for the center of the text surface.
            y (int): The y-coordinate for the center of the text surface.

        Returns:
            tuple: A tuple containing the text surface and its corresponding rectangle.
        """
    letter = font1.render(text1, True, pygame.Color(*Colours.WHITE.value))
    letter_rect = letter.get_rect()
    letter_rect.center = (x, y)
    return letter, letter_rect


def guess(letter, guessed):
    """
        Determine the result of a user's guessed letter.

        Parameters:
            letter (str): The letter guessed by the user.
            guessed (list): List of letters already guessed by the user.

        Returns:
            str or GameState: The result of the guessed letter, either the letter itself,
            GameState.SAME_GUESS if it's already guessed, or GameState.INVALID_GUESS if it's not a valid letter.
        """
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                'u', 'v', 'w', 'x', 'y', 'z']  # An array of the letters in the alphabet
    if letter in guessed:
        return GameState.SAME_GUESS
    elif letter in alphabet:
        return letter
    else:
        return GameState.INVALID_GUESS


def find_word(letter, word):
    """
        Determine whether a guessed letter is present in the target word.

        Parameters:
            letter (str): The letter guessed by the user.
            word (str): The target word.

        Returns:
            GameState: The result of the guessed letter, either GameState.NOT_IN_WORD
            if the letter is not present in the target word, or GameState.IN_WORD if it is present.
        """
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
    """
       Find the positions of a guessed letter in the target word.

       Parameters:
           letter (str): The letter guessed by the user.
           word (str): The target word.

       Returns:
           list: A list containing the positions (indices) of the guessed letter in the target word.
       """
    location = []
    y = 0
    for x in word:
        if x == letter:
            location.append(y)
        y += 1
    return location


def new_word_print(new_word, score_array, score_rect_array, output, font, x_coord):
    """
       Create surfaces and rectangles for each letter in the new word.

       Parameters:
           new_word (str): The new word to be displayed.
           score_array (list): List to store surfaces for each letter in the word.
           score_rect_array (list): List to store rectangles for positioning each letter.
           output (list): List to store the current state of guessed letters.
           font (pygame.Font): Font used for rendering text.
           x_coord (int): Initial x-coordinate for positioning letters.

       Returns:
           tuple: A tuple containing the updated score_array and score_rect_array lists.
       """
    for _ in new_word:
        output.append("_")
        score = font.render('_', True, pygame.Color(*Colours.WHITE.value))
        score_rect = score.get_rect()
        score_rect.center = (x_coord, 500)
        x_coord += 50
        score_array.append(score)
        score_rect_array.append(score_rect)
    return score_array, score_rect_array


def print_new_word_letters(new_word, x_coord, letter_array, letter_array_rect, font):
    """
        Create surfaces and rectangles for each letter in the new word.

        Parameters:
            new_word (str): The new word to be displayed.
            x_coord (int): Initial x-coordinate for positioning letters.
            letter_array (list): List to store surfaces for each letter in the word.
            letter_array_rect (list): List to store rectangles for positioning each letter.
            font (pygame.Font): Font used for rendering text.

        Returns:
            tuple: A tuple containing the updated letter_array and letter_array_rect lists.
        """
    for letter in new_word:
        letter_val, letter_rect = text_int(letter, font, x_coord, 500)
        x_coord += 50
        letter_array.append(letter_val)
        letter_array_rect.append(letter_rect)
    return letter_array, letter_array_rect


def event_text(surface, text, rect, text_cover):
    """
        Display event-related text on the game surface.

        Parameters:
            surface (pygame.Surface): The main surface for rendering graphics.
            text (pygame.Surface): The text to be displayed.
            rect (pygame.Rect): Rectangle for positioning the text.
            text_cover (pygame.Rect): Rectangle used to cover existing text.

        Returns:
            None
        """
    pygame.draw.rect(surface, pygame.Color(*Colours.BLACK.value), text_cover)
    surface.blit(text, rect)


def prepare_letter(letter, x_coord, font):
    """
        Prepare a letter for display with the specified font and position.

        Parameters:
            letter (str): The letter to be prepared.
            x_coord (int): The x-coordinate for the center of the letter surface.
            font (pygame.Font): Font used for rendering the letter.

        Returns:
            tuple: A tuple containing the letter surface and its corresponding rectangle.
        """
    letter_val, letter_rect = text_int(letter, font, x_coord, 100)
    return letter_val, letter_rect


def print_letter(surface, letter, rect):
    """
        Display a letter on the game surface.

        Parameters:
            surface (pygame.Surface): The main surface for rendering graphics.
            letter (pygame.Surface): The letter to be displayed.
            rect (pygame.Rect): Rectangle for positioning the letter.

        Returns:
            None
        """
    surface.blit(letter, rect)


def load_hangman_images():
    """
        Load and return a list of Hangman images from files.

        Returns:
            list: A list of pygame.Surface objects representing Hangman images.
        """
    return [pygame.image.load(f"Hangman-Images/Hangman-{i}.png").convert_alpha() for i in range(1, 11)]


def each_display(x):
    """
        Create a text surface with a specified font and content.

        Parameters:
            x (str): The content of the text to be rendered.

        Returns:
            tuple: A tuple containing the text surface and its corresponding rectangle.
        """
    font2 = pygame.font.SysFont('americantypewriter', 30)
    text3 = font2.render(x, True, pygame.Color(*Colours.WHITE.value))
    text_rect = text3.get_rect()
    return text3, text_rect


def x_length_coord(length):
    """
       Determine the x-coordinate for positioning letters based on the word length.

       Parameters:
           length (str): The length of the word.

       Returns:
           int: The x-coordinate for positioning letters based on the word length.
       """
    if length == "3":
        return 345
    if length == "4":
        return 322
    if length == "5":
        return 295


def three_letter():
    """
        Select and return a random three-letter word.

        Returns:
            str: A randomly selected three-letter word.
        """
    words = ["art", "arm", "aim", "ale", "ape", "all", "are", "any", "and", "ark",
             "bit", "bat", "bot", "bag", "bam", "ban",
             "cat", "can", "car", "cut", "cup", "cop",
             "dig", "den", "dog", "dip", "day",
             "ent", "eye", "end", "egg",
             "fox", "fit", "far", "fun", "for", "god", "him", "has", "had", "his", "hat",
             "her", "inn", "ice", "jam", "kit", "leg", "lip", "lot", "mat", "man", "nip",
             "oil", "out", "owl", "pin", "quo", "rid", "sew",
             "top", "the", "too", "urn", "van", "win", "was", "yap", "you", "zoo"]
    val = random.randrange(0, (len(words) - 1))
    return words[val]


def four_letter():
    """
       Select and return a random four-letter word.

       Returns:
           str: A randomly selected four-letter word.
       """
    words = ["able", "arch", "also", "ache", "anti", "bank", "bars", "been", "bent", "ball", "bark", "bird", "bump",
             "crib", "cart", "call", "cell", "came", "card", "calm", "coat", "city", "cold", "care", "cash", "card",
             "dart", "door", "deal", "duty", "dark", "deep", "damp", "draw", "drop", "dead", "duel", "dull", "down",
             "echo", "exit", "evil", "even", "ever", "east", "edge", "earn", "easy",
             "from", "fork", "funk", "five", "face", "fact", "four", "fair", "feel", "fell", "fire", "fine", "fish",
             "grab", "good", "gear", "game", "girl", "goal", "grow", "give", "gain", "glad", "grey", "grim", "gold",
             "have", "high", "hint", "hype", "hurt", "hike", "hope", "hips", "help", "hill", "home", "half", "hair",
             "iron", "into", "idea", "join", "jump", "just",
             "kill", "kind", "king", "keep", "keen", "lime", "live", "life", "love", "lady", "lack", "line", "list",
             "much", "many", "mind", "miss", "move", "nope", "nose", "open", "only",
             "push", "pull", "pony", "plug", "quip", "rose", "rice",
             "stew", "sell", "sale", "send", "sent", "some", "sort", "tear", "toad", "this",
             "ulna", "undo", "view", "very", "wear", "warm", "will", "west", "with", "year", "zero", "zoom"]
    val = random.randrange(0, (len(words) - 1))
    return words[val]


def five_letter():
    """
        Select and return a random five-letter word.

        Returns:
            str: A randomly selected five-letter word.
        """
    words = ["acorn", "amber", "apple", "annoy", "angry", "aimed", "alpha", "alarm", "alert", "aglow",
             "broom", "blaze", "break", "beach", "broke",
             "cried", "climb", "court", "crush", "creep",
             "diary", "dairy", "dream", "dress",
             "echos", "empty", "early", "earns", "eagle", "eerie", "easel", "eases", "elbow"
             "flame", "front", "funky", "fight",
             "gourd", "grape", "gamer", "gases", "glint", "glows", "grand", "grasp", "grill",
             "hired", "house", "heart", "hello", "happy", "handy", "hyper", "heaps", "hymns", "hoard", "hobby", "holes",
             "index", "itchy", "ideas", "igloo", "issue", "jokes", "jacks", "jaded", "jolly", "jelly", "judge",
             "knock", "kayak", "kicks", "kills", "limbo", "loops", "likes",
             "marks", "nippy", "newly", "naval", "novel", "nerve", "naked", "north",
             "oxbow", "ovals", "owned", "point",
             "prowl", "pants", "proud", "quits", "quilt", "quart", "rants", "round", "royal", "ranch", "stink", "stick",
             "south", "store", "sigma", "tombs", "think", "unify", "ulcer", "upset", "under", "views", "voice", "wound",
             "which", "witch", "yours", "zooms"]

    val = random.randrange(0, (len(words) - 1))
    return words[val]


pygame.init()
menu_state()
