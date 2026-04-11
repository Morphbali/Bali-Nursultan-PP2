import pygame
from ball import Ball

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Ball Game")

WHITE = (255, 255, 255)

ball = Ball(WIDTH // 2, HEIGHT // 2)

clock = pygame.time.Clock()

running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    ball.move(keys)

    ball.draw(screen)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()