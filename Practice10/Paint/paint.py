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

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)


def draw_text(surface):
    font = pygame.font.SysFont("Verdana", 14)

    surface.blit(font.render(f"Tool: {tool} | Size: {radius}", True, BLACK), (10, 10))
    surface.blit(font.render("1 Brush 2 Rect 3 Circle 4 Square", True, BLACK), (10, 30))
    surface.blit(font.render("5 RTri 6 ETri 7 Rhombus E Eraser", True, BLACK), (10, 50))
    surface.blit(font.render("Colors: R G B Y W", True, BLACK), (10, 70))


def draw_rectangle(surface, start, end):
    x1, y1 = start
    x2, y2 = end

    rect = (
        min(x1, x2),
        min(y1, y2),
        abs(x2 - x1),
        abs(y2 - y1)
    )

    pygame.draw.rect(surface, current_color, rect, radius)


def draw_square(surface, start, end):
    x1, y1 = start
    x2, y2 = end

    size = min(abs(x2 - x1), abs(y2 - y1))

    if x2 < x1:
        x1 -= size
    if y2 < y1:
        y1 -= size

    pygame.draw.rect(surface, current_color, (x1, y1, size, size), radius)


def draw_circle(surface, start, end):
    x1, y1 = start
    x2, y2 = end

    circle_radius = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
    pygame.draw.circle(surface, current_color, start, circle_radius, radius)


def draw_right_triangle(surface, start, end):
    x1, y1 = start
    x2, y2 = end

    points = [
        (x1, y1),
        (x1, y2),
        (x2, y2)
    ]

    pygame.draw.polygon(surface, current_color, points, radius)


def draw_equilateral_triangle(surface, start, end):
    x1, y1 = start
    x2, y2 = end

    width = abs(x2 - x1)

    if x2 >= x1:
        left = x1
        right = x1 + width
    else:
        left = x1 - width
        right = x1

    points = [
        ((left + right) // 2, y1),
        (left, y2),
        (right, y2)
    ]

    pygame.draw.polygon(surface, current_color, points, radius)


def draw_rhombus(surface, start, end):
    x1, y1 = start
    x2, y2 = end

    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2

    points = [
        (center_x, y1),
        (x2, center_y),
        (center_x, y2),
        (x1, center_y)
    ]

    pygame.draw.polygon(surface, current_color, points, radius)


while True:
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
            elif event.key == pygame.K_4:
                tool = "square"
            elif event.key == pygame.K_5:
                tool = "right_triangle"
            elif event.key == pygame.K_6:
                tool = "equilateral_triangle"
            elif event.key == pygame.K_7:
                tool = "rhombus"
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

        if event.type == pygame.MOUSEMOTION and drawing:
            if tool == "brush":
                pygame.draw.line(canvas, current_color, last_pos, event.pos, radius * 2)
                pygame.draw.circle(canvas, current_color, event.pos, radius)
                last_pos = event.pos

            elif tool == "eraser":
                pygame.draw.line(canvas, WHITE, last_pos, event.pos, radius * 2)
                pygame.draw.circle(canvas, WHITE, event.pos, radius)
                last_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                drawing = False
                end_pos = event.pos

                if tool == "rectangle":
                    draw_rectangle(canvas, start_pos, end_pos)
                elif tool == "circle":
                    draw_circle(canvas, start_pos, end_pos)
                elif tool == "square":
                    draw_square(canvas, start_pos, end_pos)
                elif tool == "right_triangle":
                    draw_right_triangle(canvas, start_pos, end_pos)
                elif tool == "equilateral_triangle":
                    draw_equilateral_triangle(canvas, start_pos, end_pos)
                elif tool == "rhombus":
                    draw_rhombus(canvas, start_pos, end_pos)

    display = canvas.copy()

    if drawing and tool in [
        "rectangle",
        "circle",
        "square",
        "right_triangle",
        "equilateral_triangle",
        "rhombus"
    ]:
        mouse_pos = pygame.mouse.get_pos()

        if tool == "rectangle":
            draw_rectangle(display, start_pos, mouse_pos)
        elif tool == "circle":
            draw_circle(display, start_pos, mouse_pos)
        elif tool == "square":
            draw_square(display, start_pos, mouse_pos)
        elif tool == "right_triangle":
            draw_right_triangle(display, start_pos, mouse_pos)
        elif tool == "equilateral_triangle":
            draw_equilateral_triangle(display, start_pos, mouse_pos)
        elif tool == "rhombus":
            draw_rhombus(display, start_pos, mouse_pos)

    draw_text(display)

    screen.blit(display, (0, 0))
    pygame.display.flip()
    clock.tick(60)