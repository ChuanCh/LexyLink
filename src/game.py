# game logic file.

import pygame
import sys
from bubble import BubbleGame, Gun, Bullet

# Initialize pygame
pygame.init()

# Set up the game window
screen_width = 1200
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height), pygame.HWSURFACE)
pygame.display.set_caption('Bubble Shooter')

# Set up the game clock
clock = pygame.time.Clock()

# Load the alphabet sounds
alphabet_sounds = {
    'A': pygame.mixer.Sound('./sound/aa.wav'),
    'B': pygame.mixer.Sound('./sound/e.wav'),
    'C': pygame.mixer.Sound('./sound/eu.wav'),
    # ...
}

# Create the game objects
game = BubbleGame(screen_width, screen_height)
gun = Gun(alphabet_sounds)
# Create a new bullet
# bullet = Bullet(bubble.x, bubble.y)
# bullet.set_alphabet(bubble.alphabet)

# Set up the font
font = pygame.font.SysFont(None, 36)

# Main game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                game.move_shooter('left')
            elif event.key == pygame.K_RIGHT:
                game.move_shooter('right')
            elif event.key == pygame.K_SPACE:
                game.shoot()
            elif event.unicode.isalpha():
                gun.set_alphabet(event.unicode.upper())

    # Update the game
    game.update()
    game.update_bullets()

    # Draw the game
    screen.fill((0, 0, 0))

    for bubble in game.get_bubbles():
        text = font.render(str(bubble), True, (255, 255, 255))
        screen.blit(text, (bubble.x * 50 + 20, bubble.y * 50 + 20))

    if gun.current_alphabet:
        text = font.render(gun.current_alphabet, True, (255, 255, 255))
        screen.blit(text, (game.get_shooter()[0] * 50 + 20, game.get_shooter()[1] * 50 + 20))

    for bullet in game.bullets:
        text = font.render(bullet.alphabet, True, (255, 255, 255))
        screen.blit(text, (bullet.x * 50 + 20, bullet.y * 50 + 20))

    pygame.display.update()

    # Limit the frame rate
    clock.tick(60)