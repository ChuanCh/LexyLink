# Bubble classes.

import random
import pygame


class Bubble:
    def __init__(self, alphabet):
        self.alphabet = alphabet

    def __str__(self):
        return self.alphabet

class BubbleShooter:
    def __init__(self):
        self.bubbles = []
        self.shooter = Bubble(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))

    def add_bubble(self, bubble):
        self.bubbles.append(bubble)

    def shoot(self):
        bubble = Bubble(self.shooter.alphabet)
        self.shooter = Bubble(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
        return bubble

    def remove_bubble(self, bubble):
        self.bubbles.remove(bubble)

    def get_matches(self, bubble):
        matches = set()
        visited = set()
        queue = [bubble]

        while queue:
            bubble = queue.pop(0)
            visited.add(bubble)

            for neighbor in self.get_neighbors(bubble):
                if neighbor.alphabet == bubble.alphabet and neighbor not in visited:
                    queue.append(neighbor)
                    matches.add(neighbor)

        return matches

    def get_neighbors(self, bubble):
        neighbors = []

        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            x, y = bubble.x + dx, bubble.y + dy
            neighbor = self.get_bubble(x, y)

            if neighbor:
                neighbors.append(neighbor)

        return neighbors

    def get_bubble(self, x, y):
        for bubble in self.bubbles:
            if bubble.x == x and bubble.y == y:
                return bubble

        return None

class BubbleGame:
    def __init__(self, screen_width, screen_height):
        self.shooter = BubbleShooter()
        self.bubbles = []
        self.bullets = []
        self.score = 0
        self.time = 30
        # Set up the shooter
        self.shooter_image = pygame.image.load('./src/shooter.png').convert_alpha()
        self.shooter_rect = self.shooter_image.get_rect()
        self.shooter_rect.midbottom = (screen_width // 2, screen_height - 10)

    def update(self):
        # Move the bubbles down
        for bubble in self.bubbles:
            bubble.y += 1

        # Move the bullets up
        for bullet in self.bullets:
            bullet.move()

        # Check for matches
        for bubble in self.bubbles:
            matches = self.shooter.get_matches(bubble)

            if len(matches) >= 2:
                self.score += len(matches) + 1
                self.bubbles.remove(bubble)

                for match in matches:
                    self.bubbles.remove(match)

        # Check for bullet hits
        for bullet in self.bullets:
            bubble = self.get_bubble(bullet.x, bullet.y)

            if bubble:
                self.bullets.remove(bullet)
                self.bubbles.remove(bubble)
                self.score += 10

        # Check for game over
        if any(bubble.y >= 10 for bubble in self.bubbles):
            return False

        # Check for win
        if not self.bubbles:
            return True

        try:
            # do something
            return None
        except:
            #log.error('Error message')
            return None

    def shoot(self):
        bubble = self.shooter.shoot()
        bubble.x, bubble.y = 3, 0
        self.bullets.append(Bullet(bubble.alphabet, bubble.x, bubble.y))
        self.shooter.add_bubble(bubble)

    def move_shooter(self, direction):
        if direction == 'left':
            self.shooter_rect.move_ip(-10, 0)
        elif direction == 'right':
            self.shooter_rect.move_ip(10, 0)

    def get_shooter(self):
        return self.shooter_rect.midtop

    def get_bubbles(self):
        return self.bubbles

    def get_shooter(self):
        return self.shooter.x, self.shooter.y

    def add_bullet(self, bullet):
        self.bullets.append(bullet)

    def get_bullet(self, x, y):
        for bullet in self.bullets:
            if bullet.x == x and bullet.y == y:
                return bullet

        return None

    def remove_bullet(self, bullet):
        self.bullets.remove(bullet)

    def update_bullets(self):
        for bullet in self.bullets:
            if bullet.y < 0:
                self.bullets.remove(bullet)


class Gun:
    def __init__(self, alphabet_sounds):
        self.alphabet_sounds = alphabet_sounds
        self.current_alphabet = None

    def shoot(self):
        if self.current_alphabet is None:
            return None

        bullet = Bullet(self.current_alphabet)
        self.current_alphabet = None
        return bullet

    def set_alphabet(self, alphabet):
        if alphabet in self.alphabet_sounds:
            self.current_alphabet = alphabet

class Bullet:
    def __init__(self, x, y):
        self.alphabet = None
        self.x = x
        self.y = y

    def set_alphabet(self, alphabet):
        self.alphabet = alphabet

    def move(self):
        self.y -= 1