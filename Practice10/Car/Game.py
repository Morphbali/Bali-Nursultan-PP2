# Imports
import pygame
import sys
import random
import time
from pygame.locals import *

# Initializing pygame
pygame.init()
pygame.mixer.init()

# FPS settings
FPS = 60
FramePerSec = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
WHITE = (255, 255, 255)

# Screen settings
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Game variables
SPEED = 5              # Enemy and coin falling speed
SCORE = 0              # Score increases when enemy passes the player
COINS = 0              # Total coin value collected by player
COINS_FOR_SPEED = 5    # Enemy speed increases after every 5 collected coin points
LAST_SPEED_LEVEL = 0   # Stores previous speed level to avoid increasing speed every frame

# Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Loading images
background = pygame.image.load("AnimatedStreet.png")

# Creating display
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer Practice 11")

# Background music
pygame.mixer.music.load("background.wav")
pygame.mixer.music.play(-1)


# ===== ENEMY CLASS =====
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.reset_position()

    # Places enemy at a random X position above the screen
    def reset_position(self):
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -50)

    # Moves enemy down every frame
    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)

        # If enemy leaves the screen, score increases and enemy respawns
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.reset_position()


# ===== COIN CLASS =====
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.weight = 1
        self.image = None
        self.rect = None
        self.create_random_coin()

    # Creates a coin with random weight: 1, 2, or 3
    def create_random_coin(self):
        self.weight = random.choice([1, 2, 3])

        # Bigger weight means bigger coin and more points
        if self.weight == 1:
            radius = 10
            color = YELLOW
        elif self.weight == 2:
            radius = 13
            color = ORANGE
        else:
            radius = 16
            color = WHITE

        # Draw coin as a circle on transparent surface
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)

        self.rect = self.image.get_rect()
        self.reset_position()

    # Places coin at random X position above the screen
    def reset_position(self):
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), random.randint(-600, -50))

    # Moves coin down every frame
    def move(self):
        self.rect.move_ip(0, SPEED)

        # If coin leaves the screen, create a new random coin
        if self.rect.top > SCREEN_HEIGHT:
            self.create_random_coin()


# ===== PLAYER CLASS =====
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    # Moves player left and right using keyboard arrows
    def move(self):
        pressed_keys = pygame.key.get_pressed()

        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)

        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)


# ===== OBJECTS =====
P1 = Player()
E1 = Enemy()

# Several coins are created, so they appear randomly on the road
coin1 = Coin()
coin2 = Coin()
coin3 = Coin()

# Sprite groups
players = pygame.sprite.Group()
players.add(P1)

enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()
coins.add(coin1, coin2, coin3)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1, coin1, coin2, coin3)


# ===== GAME LOOP =====
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Draw background
    DISPLAYSURF.blit(background, (0, 0))

    # Draw score text
    score_text = font_small.render("Score: " + str(SCORE), True, BLACK)
    DISPLAYSURF.blit(score_text, (10, 10))

    # Draw coin counter text
    coin_text = font_small.render("Coins: " + str(COINS), True, BLACK)
    DISPLAYSURF.blit(coin_text, (250, 10))

    # Draw speed text
    speed_text = font_small.render("Speed: " + str(round(SPEED, 1)), True, BLACK)
    DISPLAYSURF.blit(speed_text, (10, 35))

    # Move and draw all sprites
    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)

    # Check collision between player and coins
    collected_coins = pygame.sprite.spritecollide(P1, coins, False)

    for coin in collected_coins:
        COINS += coin.weight       # Add coin weight to total coins
        coin.create_random_coin()  # Respawn collected coin with new random weight

    # Increase enemy speed when player earns N coin points
    current_speed_level = COINS // COINS_FOR_SPEED

    if current_speed_level > LAST_SPEED_LEVEL:
        SPEED += 1
        LAST_SPEED_LEVEL = current_speed_level

    # Check collision between player and enemy
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound("crash.wav").play()
        time.sleep(1)

        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
        pygame.display.update()

        time.sleep(2)
        pygame.quit()
        sys.exit()

    # Update display
    pygame.display.update()
    FramePerSec.tick(FPS)
