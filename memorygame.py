import pygame
import sys
import random


pygame.init()
pygame.mixer.init()

screen_width, screen_height = 640, 480
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


card_size = (100, 100)
cards_horizontal = 4
cards_vertical = 3
margin = 20
top_offset = 50
cards = []
selected_cards = []
matched_cards = []
game_over = False


card_images = [pygame.transform.scale(pygame.image.load(f'image{i}.png'), card_size) for i in range(1, 7)] * 2
success_sound = pygame.mixer.Sound('success.mp3')
failure_sound = pygame.mixer.Sound('failure.mp3')
random.shuffle(card_images)

start_ticks = pygame.time.get_ticks()

running = True
while running:
    screen.fill(bg_color)
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
                        pygame.time.wait(500)
                        selected_cards = []

    #screen.fill(bg_color)

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


