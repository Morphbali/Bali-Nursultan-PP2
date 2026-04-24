import pygame
import random
import sys

pygame.init()

WIDTH = 600
HEIGHT = 400
CELL_SIZE = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
GRAY = (80, 80, 80)

font = pygame.font.SysFont("Verdana", 20)
big_font = pygame.font.SysFont("Verdana", 50)

snake = [(100, 100), (80, 100), (60, 100)]
direction = "RIGHT"
next_direction = "RIGHT"

score = 0
level = 1
speed = 8
foods_to_next_level = 3
food_eaten_on_level = 0


def draw_text(text, x, y, color=WHITE):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


def generate_food():
    while True:
        x = random.randrange(0, WIDTH, CELL_SIZE)
        y = random.randrange(0, HEIGHT, CELL_SIZE)

        # Еда не должна появляться на змейке
        if (x, y) not in snake:
            return (x, y)


food = generate_food()


def game_over():
    screen.fill(BLACK)
    text = big_font.render("Game Over", True, RED)
    screen.blit(text, (150, 160))
    pygame.display.update()
    pygame.time.delay(2000)
    pygame.quit()
    sys.exit()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Управление змейкой
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != "DOWN":
                next_direction = "UP"
            elif event.key == pygame.K_DOWN and direction != "UP":
                next_direction = "DOWN"
            elif event.key == pygame.K_LEFT and direction != "RIGHT":
                next_direction = "LEFT"
            elif event.key == pygame.K_RIGHT and direction != "LEFT":
                next_direction = "RIGHT"

    direction = next_direction

    head_x, head_y = snake[0]

    # Движение головы
    if direction == "UP":
        head_y -= CELL_SIZE
    elif direction == "DOWN":
        head_y += CELL_SIZE
    elif direction == "LEFT":
        head_x -= CELL_SIZE
    elif direction == "RIGHT":
        head_x += CELL_SIZE

    new_head = (head_x, head_y)

    # Проверка столкновения со стеной
    if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
        game_over()

    # Проверка столкновения с самой собой
    if new_head in snake:
        game_over()

    snake.insert(0, new_head)

    # Проверка съела ли змейка еду
    if new_head == food:
        score += 1
        food_eaten_on_level += 1

        # Если съели нужное количество еды — следующий уровень
        if food_eaten_on_level >= foods_to_next_level:
            level += 1
            speed += 2
            food_eaten_on_level = 0
            foods_to_next_level += 1

        food = generate_food()
    else:
        snake.pop()

    screen.fill(BLACK)

    # Рисуем еду
    pygame.draw.rect(screen, RED, (food[0], food[1], CELL_SIZE, CELL_SIZE))

    # Рисуем змейку
    for part in snake:
        pygame.draw.rect(screen, GREEN, (part[0], part[1], CELL_SIZE, CELL_SIZE))

    # Счётчики очков и уровня
    draw_text("Score: " + str(score), 10, 10)
    draw_text("Level: " + str(level), 10, 35)
    draw_text("Food to next level: " + str(foods_to_next_level - food_eaten_on_level), 10, 60)

    pygame.display.update()
    clock.tick(speed)