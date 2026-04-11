import pygame
from datetime import datetime

class Clock:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.sec_angle = 0
        self.min_angle = 0

        self.left_hand = pygame.image.load("images/left-hand.PNG")
        self.right_hand = pygame.image.load("images/right-hand.PNG")
        
        self.left_hand = pygame.transform.scale(self.left_hand, (60, 250))  # Увеличена секундная стрелка
        self.right_hand = pygame.transform.scale(self.right_hand, (80, 300))  # Увеличена минутная стрелка

    def update(self):
        now = datetime.now()

        self.sec_angle = -(now.second / 60) * 360  # Секундная стрелка
        self.min_angle = -(now.minute / 60) * 360  # Минутная стрелка

    def draw(self, screen):
        right_hand_rotated = pygame.transform.rotate(self.right_hand, self.min_angle)
        right_rect = right_hand_rotated.get_rect(center=(self.x, self.y))
        screen.blit(right_hand_rotated, right_rect.topleft)

        left_hand_rotated = pygame.transform.rotate(self.left_hand, self.sec_angle)
        left_rect = left_hand_rotated.get_rect(center=(self.x, self.y))
        screen.blit(left_hand_rotated, left_rect.topleft)