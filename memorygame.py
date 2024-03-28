import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen setup
screen_width, screen_height = 640, 480
screen = pygame.display.set_mode((screen_width, screen_height))

# Colors
bg_color = (30, 30, 30)
card_color = (255, 255, 255)
matched_color = (0, 255, 0)

# Game variables
card_size = (50, 50)
cards_horizontal = 4
cards_vertical = 3
margin = 10
cards = []
selected_cards = []
matched_cards = []

# Generate card positions and shuffle
card_positions = [(x, y) for x in range(cards_horizontal) for y in range(cards_vertical)]
random.shuffle(card_positions)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Add card selection logic here
            pass

    # Draw background
    screen.fill(bg_color)

    # Draw cards
    for x in range(cards_horizontal):
        for y in range(cards_vertical):
            card_pos = (x * (card_size[0] + margin) + margin, y * (card_size[1] + margin) + margin)
            if (x, y) in matched_cards:
                pygame.draw.rect(screen, matched_color, card_pos + card_size)
            else:
                pygame.draw.rect(screen, card_color, card_pos + card_size)

    pygame.display.flip()

pygame.quit()
