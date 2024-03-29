import pygame
import sys
import random
import time

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
    options = ["1 Player", "2 Players"]
    options_rects = [pygame.Rect(screen_width / 2 - 100, 300 + i * 100, 200, 50) for i, _ in enumerate(options)]
    title_font = pygame.font.SysFont(None, 60)
    


    while True:
        screen.fill(bg_color)
        title_surf = title_font.render("Select Number of Players", True, button_text_color)
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


pygame.init()
pygame.mixer.init()

screen_width, screen_height = 900, 675
screen = pygame.display.set_mode((screen_width, screen_height))




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



background_image = pygame.image.load('nuggets.png')
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
card_images = [pygame.transform.scale(pygame.image.load(f'image{i}.png'), card_size) for i in range(1, 7)] * 2
success_sound = pygame.mixer.Sound('success.mp3')
failure_sound = pygame.mixer.Sound('failure.mp3')
flip_sound = pygame.mixer.Sound('flip.mp3')
random.shuffle(card_images)


num_players = select_number_of_players(screen, button_font)
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
                            if num_players == 2:
                                current_player = 1 if current_player == 1 else 2
                            
                        else:
                            time.sleep(0.5)
                            failure_sound.play()
                            current_player = 2 if current_player == 1 else 1
                        pygame.time.wait(500)
                        selected_cards = []

        # Right after processing MOUSEBUTTONDOWN events and before drawing the cards
    if num_players == 2 and not game_over:
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
            elif index in selected_cards:
                screen.blit(card_images[index], rect)
            else:
                pygame.draw.rect(screen, hidden_card_color, rect)

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


