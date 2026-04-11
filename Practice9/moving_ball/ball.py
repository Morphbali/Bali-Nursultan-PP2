import pygame

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 25
        self.color = (255, 0, 0)  # Красный цвет
        self.speed = 20

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def move(self, keys):
        if keys[pygame.K_UP] and self.y - self.radius > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y + self.radius < 600:
            self.y += self.speed
        if keys[pygame.K_LEFT] and self.x - self.radius > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x + self.radius < 800:
            self.x += self.speed