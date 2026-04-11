import pygame
import math
from datetime import datetime
from clock import Clock

pygame.init()

WIDTH, HEIGHT = 400, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey's Clock")

clock_image = pygame.image.load("images/dial.jpg")
clock_image = pygame.transform.scale(clock_image, (300, 300))  # Устанавливаем размер циферблата
clock = Clock(WIDTH // 2, HEIGHT // 2)

fps = 60
clock_tick = pygame.time.Clock()

running = True
while running:
    screen.fill((255, 255, 255))  # Белый фон

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(clock_image, (WIDTH // 2 - 150, HEIGHT // 2 - 150))

    clock.update()

    clock.draw(screen)

    pygame.display.flip()
    clock_tick.tick(fps)  # Обновление каждую секунду

pygame.quit()