import pygame
import sys
import random


pygame.init()


screen_width, screen_height = 640, 480
screen = pygame.display.set_mode((screen_width, screen_height))


bg_color = (30, 30, 30)
hidden_card_color = (255, 255, 255)
matched_color = (0, 255, 0)


card_size = (100, 100)
cards_horizontal = 4
cards_vertical = 3
margin = 20
top_offset = 30
cards = []
selected_cards = []
matched_cards = []
game_over = False


card_images = []
for i in range(1, 7):  
    img = pygame.image.load(f'image{i}.png')
    img = pygame.transform.scale(img, card_size)
    card_images.extend([img, img])  

random.shuffle(card_images)

start_ticks = pygame.time.get_ticks()

running = True
while running:
    seconds = (pygame.time.get_ticks() - start_ticks) // 1000
    minutes = seconds // 60
    seconds = seconds % 60
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            x, y = pygame.mouse.get_pos()
            column = x // (card_size[0] + margin)
            row = (y - top_offset) // (card_size[1] + margin)
            index = row * cards_horizontal + column
            if (index < len(card_images) and 
                index not in matched_cards and 
                index not in selected_cards):
                selected_cards.append(index)
                if len(selected_cards) == 2:
                    if card_images[selected_cards[0]] == card_images[selected_cards[1]]:
                        matched_cards.extend(selected_cards)
                    else:
                        pygame.time.wait(500)
                    selected_cards = []


                    break

    screen.fill(bg_color)

    #cards = []
    for x in range(cards_horizontal):
        for y in range(cards_vertical):
            rect = pygame.Rect(x * (card_size[0] + margin) + margin, y * (card_size[1] + margin) + margin + top_offset, *card_size)
            cards.append(rect)
            if len(matched_cards) == len(card_images) or game_over:
                screen.blit(card_images[cards_horizontal * y + x], rect)
            elif cards_horizontal * y + x in matched_cards or cards_horizontal * y + x in selected_cards:
                screen.blit(card_images[cards_horizontal * y + x], rect)
            else:
                pygame.draw.rect(screen, hidden_card_color, rect)

    if len(matched_cards) == len(card_images):
        game_over = True
        font = pygame.font.SysFont(None, 72)
        text_surf = font.render('You Win!', True, (255, 215, 0))
        text_rect = text_surf.get_rect(center=(screen_width / 2, screen_height / 2))
        screen.blit(text_surf, text_rect)

    font = pygame.font.SysFont(None, 36)
    timer_surf = font.render(f'Time: {minutes:02}:{seconds:02}', True, (255, 255, 255))
    timer_rect = timer_surf.get_rect(topleft=(10, 10))
    screen.blit(timer_surf, timer_rect)

    pygame.display.flip()

pygame.quit()
