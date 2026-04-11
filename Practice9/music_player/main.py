import pygame
from player import Player

pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player")

player = Player()

clock = pygame.time.Clock()

running = True
while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player.handle_keys(keys)

    player.display_info(screen)

    font = pygame.font.Font(None, 28)
    text_play = font.render("P = Play", True, (0, 0, 0))
    text_stop = font.render("S = Stop", True, (0, 0, 0))
    text_next = font.render("N = Next", True, (0, 0, 0))
    text_back = font.render("B = Back", True, (0, 0, 0))
    text_quit = font.render("Q = Quit", True, (0, 0, 0))

    screen.blit(text_play, (20, 100))
    screen.blit(text_stop, (20, 140))
    screen.blit(text_next, (20, 180))
    screen.blit(text_back, (20, 220))
    screen.blit(text_quit, (20, 260))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()