import pygame
import sys

pygame.init()

WIDTH = 640
HEIGHT = 480

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

current_color = BLUE
tool = "brush"

radius = 10
drawing = False
start_pos = None
last_pos = None

screen.fill(WHITE)


def draw_text():
    font = pygame.font.SysFont("Verdana", 16)

    text = f"Tool: {tool} | Size: {radius} | 1 Brush  2 Rect  3 Circle  E Eraser"
    img = font.render(text, True, BLACK)
    screen.blit(img, (10, 10))

    text2 = "Colors: R Red | G Green | B Blue | Y Yellow | W White"
    img2 = font.render(text2, True, BLACK)
    screen.blit(img2, (10, 30))


while True:
    temp_screen = screen.copy()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            if event.key == pygame.K_r:
                current_color = RED
                tool = "brush"
            elif event.key == pygame.K_g:
                current_color = GREEN
                tool = "brush"
            elif event.key == pygame.K_b:
                current_color = BLUE
                tool = "brush"
            elif event.key == pygame.K_y:
                current_color = YELLOW
                tool = "brush"
            elif event.key == pygame.K_w:
                current_color = WHITE
                tool = "brush"

            elif event.key == pygame.K_1:
                tool = "brush"
            elif event.key == pygame.K_2:
                tool = "rectangle"
            elif event.key == pygame.K_3:
                tool = "circle"
            elif event.key == pygame.K_e:
                tool = "eraser"

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                drawing = True
                start_pos = event.pos
                last_pos = event.pos

            elif event.button == 3:
                radius = max(1, radius - 2)

            elif event.button == 4:
                radius = min(100, radius + 2)

            elif event.button == 5:
                radius = max(1, radius - 2)

        if event.type == pygame.MOUSEMOTION:
            if drawing:
                if tool == "brush":
                    pygame.draw.line(screen, current_color, last_pos, event.pos, radius * 2)
                    pygame.draw.circle(screen, current_color, event.pos, radius)
                    last_pos = event.pos

                elif tool == "eraser":
                    pygame.draw.line(screen, WHITE, last_pos, event.pos, radius * 2)
                    pygame.draw.circle(screen, WHITE, event.pos, radius)
                    last_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                drawing = False
                end_pos = event.pos

                if tool == "rectangle":
                    x1, y1 = start_pos
                    x2, y2 = end_pos

                    rect_x = min(x1, x2)
                    rect_y = min(y1, y2)
                    rect_w = abs(x2 - x1)
                    rect_h = abs(y2 - y1)

                    pygame.draw.rect(screen, current_color, (rect_x, rect_y, rect_w, rect_h), radius)

                elif tool == "circle":
                    x1, y1 = start_pos
                    x2, y2 = end_pos

                    circle_radius = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)

                    pygame.draw.circle(screen, current_color, start_pos, circle_radius, radius)

    display = screen.copy()

    if drawing and tool in ["rectangle", "circle"]:
        mouse_pos = pygame.mouse.get_pos()

        if tool == "rectangle":
            x1, y1 = start_pos
            x2, y2 = mouse_pos

            rect_x = min(x1, x2)
            rect_y = min(y1, y2)
            rect_w = abs(x2 - x1)
            rect_h = abs(y2 - y1)

            pygame.draw.rect(display, current_color, (rect_x, rect_y, rect_w, rect_h), radius)

        elif tool == "circle":
            x1, y1 = start_pos
            x2, y2 = mouse_pos

            circle_radius = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)

            pygame.draw.circle(display, current_color, start_pos, circle_radius, radius)

    draw_text()

    pygame.display.flip()
    clock.tick(60)