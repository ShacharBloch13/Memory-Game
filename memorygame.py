import pygame
import sys
import random
import time
from vosk import Model, KaldiRecognizer
import pyaudio
import os
import json
import threading

def select_difficulty(screen, button_font):
    title_font = pygame.font.SysFont(None, 60)  # Increased font size for the title
    button_font = pygame.font.SysFont(None, 50)  # Increased font size for button labels
    title_text = "Denver Nuggets Memory game"
    difficulties = ["Easy", "Mid", "Hard"]
    button_width = 300  # Increase the width for better fit in the larger window
    button_height = 100  # Increase the height for more substantial buttons
    button_start_y = 200  # Starting Y position of the first button
    button_margin = 30  # Space between buttons
    options_rects = [pygame.Rect(screen_width / 2 - button_width / 2, button_start_y + i * (button_height + button_margin), button_width, button_height) for i in range(3)]
    
    while True:
        screen.fill(bg_color)
        title_surf = title_font.render(title_text, True, button_text_color)
        screen.blit(title_surf, (screen_width / 2 - title_surf.get_width() / 2, 100))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(options_rects):
                    if rect.collidepoint(event.pos):
                        return difficulties[i]
                
        for i, rect in enumerate(options_rects):
            pygame.draw.rect(screen, (100, 200, 100), rect)
            text_surf = button_font.render(difficulties[i], True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)
        
        pygame.display.flip()

def select_number_of_players(screen, button_font):
    options = ["1 Player", "2 Players", "Time Attack", "Voice Control"]
    options_rects = [pygame.Rect(screen_width / 2 - 100, 300 + i * 100, 200, 50) for i, _ in enumerate(options)]
    title_font = pygame.font.SysFont(None, 60)
    


    while True:
        screen.fill(bg_color)
        title_surf = title_font.render("Select Mode", True, button_text_color)
        screen.blit(title_surf, (screen_width / 2 - title_surf.get_width() / 2, 200))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(options_rects):
                    if rect.collidepoint(event.pos):
                        return i + 1
                
        for i, rect in enumerate(options_rects):
            pygame.draw.rect(screen, (100, 200, 100), rect)
            text_surf = button_font.render(options[i], True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)
        
        pygame.display.flip()

def display_countdown(screen, remaining_time, screen_width):
    countdown_text = f"Time Left: {remaining_time}s"
    countdown_surf = button_font.render(countdown_text, True, (255, 255, 255))
    countdown_rect = countdown_surf.get_rect(topright=(screen_width - 10, 50))
    screen.blit(countdown_surf, countdown_rect)

def display_game_over_message():
    overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  # Semi-transparent overlay
    screen.blit(overlay, (0, 0))
    font = pygame.font.SysFont(None, 72)
    text_surf = font.render('Loser!', True, (255, 215, 0))
    text_rect = text_surf.get_rect(center=(screen_width / 2 + 130, screen_height / 2 + 130))
    screen.blit(text_surf, text_rect)

def init_vosk():
    global recognizer, stream
    model_path = r"C:\Users\user\Desktop\IDC\YEAR_3\From An Idea To Application\HW\HW1\Memory-Game\vosk-model-small-en-us-0.15"
  # Update with your actual path
    if not os.path.exists(model_path):
        print("Please download the model from the VOSK website and place it in the specified directory.")
        exit(1)
    model = Model(model_path)
    recognizer = KaldiRecognizer(model, 16000)
    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()

def check_cards_match():
    global selected_cards, matched_cards, game_over
    if len(selected_cards) == 2:
        if card_images[selected_cards[0]] == card_images[selected_cards[1]]:
            matched_cards.extend(selected_cards)
            print("Matched cards!")  # Debugging
            if len(matched_cards) == len(card_images):
                game_over = True
        else:
            print("Cards did not match!")  # Debugging
        selected_cards = []
        

def voice_control_thread():
    global recognizer, stream, voice_commands, voice_control_enabled
    while voice_control_enabled:
        data = stream.read(4096, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            text = result.get("text", "").strip().lower()  # Convert to lower case for matching
            print(f"Voice Control Thread recognized: {text}")  # Debugging
            if text in number_words_to_digits:  # Check if the text is a recognized number word
                command = number_words_to_digits[text]
                voice_commands.append(command)
                print(f"Appending command: {command}")  # Debugging

def process_voice_commands():
    global selected_cards, voice_commands, matched_cards, game_over
    while voice_commands:
        command = voice_commands.pop(0)  # Process each command
        if isinstance(command, int):
            if 1 <= command <= len(card_images):  # Validate command range
                selected_card_index = command - 1
                if selected_card_index not in selected_cards and selected_card_index not in matched_cards:
                    selected_cards.append(selected_card_index)
                    print(f"Selected card {command} via voice")
                    # Check for a match or reset selected cards after a delay
                    if len(selected_cards) == 2:
                        pygame.time.wait(1000)  # Delay for user to see the cards
                        check_cards_match()
        elif isinstance(command, str) and command == "reset":
            # Example reset functionality, adapt as needed
            reset_game()

def reset_game():
    global selected_cards, matched_cards, game_over
    selected_cards = []
    matched_cards = []
    game_over = False

pygame.init()
pygame.mixer.init()

screen_width, screen_height = 900, 675
screen = pygame.display.set_mode((screen_width, screen_height))


number_words_to_digits = {
    "one": 1, "two": 2, "three": 3, "for": 4 , "five": 5, #when i say "four" it recognizes it as "for"
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
    "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18,
    "nineteen": 19, "twenty": 20
}



bg_color = (30, 30, 30)
hidden_card_color = (255, 255, 255)
matched_color = (0, 255, 0)
reset_button_color = (100, 200, 100)
play_again_button_color = (100, 100, 200)
button_text_color = (255, 255, 255)
button_font = pygame.font.SysFont(None, 36)
reset_button_rect = pygame.Rect(screen_width - 150, 10, 140, 40)  # Top-right corner
play_again_button_rect = pygame.Rect(screen_width / 2 - 70, screen_height / 2, 140, 40)  # Center

difficulty = select_difficulty(screen, button_font)
image_count = 6 if difficulty == "Easy" else 8 if difficulty == "Mid" else 10

card_size = (100, 100)
cards_horizontal = 4
cards_vertical = 3
margin = 20
top_offset = 50
cards = []
selected_cards = []
matched_cards = []
game_over = False
voice_commands = []
voice_control_enabled = False
recognizer = None
stream = None



background_image = pygame.image.load('nuggets.png')
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
card_images = [pygame.transform.scale(pygame.image.load(f'image{i}.png'), card_size) for i in range(1, 7)] * 2
success_sound = pygame.mixer.Sound('success.mp3')
failure_sound = pygame.mixer.Sound('failure.mp3')
flip_sound = pygame.mixer.Sound('flip.mp3')
random.shuffle(card_images)


mode = select_number_of_players(screen, button_font)
time_limit = 60 if mode == 3 else None
time_passed = 0


if mode == 4:  # 1 Player mode with voice control
    init_vosk()
    running = True
    voice_control_enabled = True
    voice_control_thread_instance = threading.Thread(target=voice_control_thread, daemon=True)
    voice_control_thread_instance.start()

    start_ticks = pygame.time.get_ticks()

    while running:
        screen.blit(background_image, (0, 0))
        seconds = (pygame.time.get_ticks() - start_ticks) // 1000
        minutes = seconds // 60
        seconds = seconds % 60

        process_voice_commands()  # Process voice commands for selecting cards

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                voice_control_enabled = False  # Ensure to stop the voice control thread
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if reset_button_rect.collidepoint(mouse_pos) or (game_over and play_again_button_rect.collidepoint(mouse_pos)):
                    selected_cards = []
                    matched_cards = []
                    game_over = False
                    start_ticks = pygame.time.get_ticks()
                    random.shuffle(card_images)
                    continue

                if not game_over:
                    x, y = mouse_pos
                    column = x // (card_size[0] + margin)
                    row = (y - top_offset) // (card_size[1] + margin)
                    index = row * cards_horizontal + column
                    if 0 <= column < cards_horizontal and 0 <= row < cards_vertical and index not in matched_cards and index not in selected_cards:
                        selected_cards.append(index)
                        if len(selected_cards) == 2:
                            if card_images[selected_cards[0]] == card_images[selected_cards[1]]:
                                matched_cards.extend(selected_cards)
                                success_sound.play()
                            else:
                                failure_sound.play()
                                pygame.time.wait(500)  # Wait half a second
                            selected_cards = []

        if game_over:
            display_game_over_message()
            if play_again_button_rect.collidepoint(pygame.mouse.get_pos()):
                game_over = False
                matched_cards = []
                selected_cards = []
                random.shuffle(card_images)
                start_ticks = pygame.time.get_ticks()

        for x in range(cards_horizontal):
            for y in range(cards_vertical):
                rect = pygame.Rect(x * (card_size[0] + margin) + margin, y * (card_size[1] + margin) + margin + top_offset, *card_size)
                index = y * cards_horizontal + x
                if index in matched_cards or index in selected_cards:
                    screen.blit(card_images[index], rect)
                else:
                    pygame.draw.rect(screen, hidden_card_color, rect)

        if len(matched_cards) == len(card_images):
            game_over = True
            text_surf = font.render('Well done!', True, (255, 215, 0))
            text_rect = text_surf.get_rect(center=(screen_width / 2, (screen_height / 2) -50))
            screen.blit(text_surf, text_rect)

            pygame.draw.rect(screen, play_again_button_color, play_again_button_rect)
            play_again_text_surf = button_font.render('Play Again', True, button_text_color)
            play_again_text_rect = play_again_text_surf.get_rect(center=play_again_button_rect.center)
            screen.blit(play_again_text_surf, play_again_text_rect)

        pygame.draw.rect(screen, reset_button_color, reset_button_rect)
        reset_text_surf = button_font.render('Reset', True, button_text_color)
        reset_text_rect = reset_text_surf.get_rect(center=reset_button_rect.center)
        screen.blit(reset_text_surf, reset_text_rect)

        timer_surf = button_font.render(f'Time: {minutes:02}:{seconds:02}', True, button_text_color)
        timer_rect = timer_surf.get_rect(topleft=(10, 10))
        screen.blit(timer_surf, timer_rect)

        pygame.display.flip()

    stream.stop_stream()
    stream.close()
    pygame.quit()


# In the main game loop, adjust the game logic based on the selected mode
if mode == 3: 
    start_ticks = pygame.time.get_ticks()
    current_time = pygame.time.get_ticks()
    time_passed = (current_time - start_ticks) // 1000
    if time_passed > time_limit:
        game_over = True
        if game_over and play_again_button_rect.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
            # Reset the game state for 'Time Attack' mode
            game_over = False
            matched_cards = []
            selected_cards = []
            start_ticks = pygame.time.get_ticks()
            random.shuffle(card_images)
            time_limit = 60
        #if game_over:
            font = pygame.font.SysFont(None, 72)
            overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))  # Adjust the alpha to make it more or less transparent
            screen.blit(overlay, (0, 0))


current_player = 1  # Tracks the current player (1 or 2)
player_turns = {1: "Player 1's Turn", 2: "Player 2's Turn"}
card_images = [pygame.transform.scale(pygame.image.load(f'image{i}.png'), (100, 100)) for i in range(1, image_count + 1)] * 2
random.shuffle(card_images)

cards_horizontal = 4
cards_vertical = (image_count * 2) // cards_horizontal
top_offset = 50
game_over = False
selected_cards = []
matched_cards = []
start_ticks = pygame.time.get_ticks()

start_ticks = pygame.time.get_ticks()

running = True
while running:
    screen.blit(background_image, (0, 0))
    seconds = (pygame.time.get_ticks() - start_ticks) // 1000
    minutes = seconds // 60
    seconds = seconds % 60
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if reset_button_rect.collidepoint(mouse_pos) or (game_over and play_again_button_rect.collidepoint(mouse_pos)):  # Reset logic
                selected_cards = []
                matched_cards = []
                game_over = False
                start_ticks = pygame.time.get_ticks()  # Restart timer
                random.shuffle(card_images)  # Shuffle cards for a new game
                continue  # Skip remaining logic in this loop iteration

            if not game_over:
                turn_surf = button_font.render(player_turns[current_player], True, button_text_color)
                turn_rect = turn_surf.get_rect(topleft=(10, screen_height - 40))
                screen.blit(turn_surf, turn_rect)
                x, y = mouse_pos
                column = x // (card_size[0] + margin)
                row = (y - top_offset) // (card_size[1] + margin)
                index = row * cards_horizontal + column
                if 0 <= column < cards_horizontal and 0 <= row < cards_vertical and index not in matched_cards and index not in selected_cards:
                    selected_cards.append(index)
                    if len(selected_cards) >= 1:
                        flip_sound.play()
                    if len(selected_cards) == 2:
                        if card_images[selected_cards[0]] == card_images[selected_cards[1]]:
                            matched_cards.extend(selected_cards)
                            time.sleep(0.5)
                            success_sound.play()
                            if mode == 2:
                                current_player = 1 if current_player == 1 else 2
                            
                        else:
                            time.sleep(0.5)
                            failure_sound.play()
                            current_player = 2 if current_player == 1 else 1
                        pygame.time.wait(500)
                        selected_cards = []
    if game_over and mode == 3:
        if len(matched_cards) == len(card_images):  # If the player completed the board
            time_limit -= 5  # Decrease time limit for the next game
            start_ticks = pygame.time.get_ticks()  # Restart the timer
            # Reset game state for a new round
            game_over = False
            matched_cards = []
            selected_cards = []
            random.shuffle(card_images)
        else:
            # Display "You Lost" message and "Play Again" option
            # Handle "Play Again" button press
            display_game_over_message()
            if play_again_button_rect.collidepoint(pygame.mouse.get_pos()):
                time_limit = 60  # Reset time limit
                start_ticks = pygame.time.get_ticks()  # Restart the timer
                game_over = False
                matched_cards = []
                selected_cards = []
                random.shuffle(card_images)

    if mode == 3 and not game_over:
        current_time = pygame.time.get_ticks()
        time_passed = (current_time - start_ticks) // 1000  # Convert milliseconds to seconds
        remaining_time = time_limit - time_passed
        display_countdown(screen, remaining_time, screen_width) #important!!!!

        if remaining_time <= 0:
            game_over = True
            display_game_over_message()


    # else:
    #     display_countdown(screen, remaining_time, screen_width)


        # Right after processing MOUSEBUTTONDOWN events and before drawing the cards
    if mode == 2 and not game_over:
        turn_text = player_turns[current_player]  # Get the current player's turn text
        turn_text_surf = button_font.render(turn_text, True, button_text_color)
        # Position it in the top right corner. Adjust the positioning as needed.
        turn_text_rect = turn_text_surf.get_rect(topright=(screen_width - 10, 50))
        screen.blit(turn_text_surf, turn_text_rect)


    for x in range(cards_horizontal):
        for y in range(cards_vertical):
            rect = pygame.Rect(x * (card_size[0] + margin) + margin, y * (card_size[1] + margin) + margin + top_offset, *card_size)
            index = y * cards_horizontal + x
            if index in matched_cards:
                screen.blit(card_images[index], rect)
                card_number_text = f"{index + 1}"
            elif index in selected_cards:
                screen.blit(card_images[index], rect)
                card_number_text = f"{index + 1}"
            else:
                pygame.draw.rect(screen, hidden_card_color, rect)
                card_number_text = f"{index + 1}"
            
            # Create a text surface for the number
            num_font = pygame.font.SysFont(None, 24)  # Smaller font for the number
            num_text_surf = num_font.render(card_number_text, True, (0, 0, 0))
            num_text_rect = num_text_surf.get_rect(center=rect.center)
            
            # Draw the number on the card
            screen.blit(num_text_surf, num_text_rect)

    if len(matched_cards) == len(card_images):
        game_over = True
        font = pygame.font.SysFont(None, 72)
        text_surf = font.render('Well done!', True, (255, 215, 0))
        text_rect = text_surf.get_rect(center=(screen_width / 2, (screen_height / 2) -50))
        screen.blit(text_surf, text_rect)

        pygame.draw.rect(screen, play_again_button_color, play_again_button_rect)
        play_again_text_surf = button_font.render('Play Again', True, button_text_color)
        play_again_text_rect = play_again_text_surf.get_rect(center=play_again_button_rect.center)
        screen.blit(play_again_text_surf, play_again_text_rect)

    pygame.draw.rect(screen, reset_button_color, reset_button_rect)
    reset_text_surf = button_font.render('Reset', True, button_text_color)
    reset_text_rect = reset_text_surf.get_rect(center=reset_button_rect.center)
    screen.blit(reset_text_surf, reset_text_rect)

    timer_surf = button_font.render(f'Time: {minutes:02}:{seconds:02}', True, button_text_color)
    timer_rect = timer_surf.get_rect(topleft=(10, 10))
    screen.blit(timer_surf, timer_rect)

    pygame.display.flip()

pygame.quit()


