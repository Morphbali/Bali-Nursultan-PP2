import pygame
import random
import sys
import time

# ===== INITIALIZATION =====
pygame.init()

# ===== SCREEN SETTINGS =====
WIDTH = 600
HEIGHT = 400
CELL_SIZE = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Practice 11")

clock = pygame.time.Clock()

# ===== COLORS =====
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
GRAY = (80, 80, 80)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (160, 32, 240)

# ===== FONTS =====
font = pygame.font.SysFont("Verdana", 20)
big_font = pygame.font.SysFont("Verdana", 50)

# ===== GAME VARIABLES =====
snake = [(100, 100), (80, 100), (60, 100)]
direction = "RIGHT"
next_direction = "RIGHT"

score = 0
level = 1
speed = 8

foods_to_next_level = 3
food_eaten_on_level = 0

# Food will disappear after this amount of seconds
FOOD_LIFETIME = 5


def draw_text(text, x, y, color=WHITE):
    """Draws text on the screen."""
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


def generate_food():
    """
    Generates food in a random position.
    Food has different weight/value:
    value 1 = simple food
    value 2 = medium food
    value 3 = bonus food
    """
    while True:
        x = random.randrange(0, WIDTH, CELL_SIZE)
        y = random.randrange(0, HEIGHT, CELL_SIZE)

        # Food must not appear on the snake body
        if (x, y) not in snake:
            value = random.choice([1, 2, 3])

            # Different values have different colors
            if value == 1:
                color = RED
            elif value == 2:
                color = YELLOW
            else:
                color = PURPLE

            # Store creation time to remove food after timer
            created_time = time.time()

            return {
                "position": (x, y),
                "value": value,
                "color": color,
                "created_time": created_time
            }


def game_over():
    """Shows game over screen and closes the game."""
    screen.fill(BLACK)
    text = big_font.render("Game Over", True, RED)
    screen.blit(text, (150, 160))
    pygame.display.update()
    pygame.time.delay(2000)
    pygame.quit()
    sys.exit()


# First food generation
food = generate_food()


# ===== MAIN GAME LOOP =====
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Snake control
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

    # ===== MOVE SNAKE HEAD =====
    head_x, head_y = snake[0]

    if direction == "UP":
        head_y -= CELL_SIZE
    elif direction == "DOWN":
        head_y += CELL_SIZE
    elif direction == "LEFT":
        head_x -= CELL_SIZE
    elif direction == "RIGHT":
        head_x += CELL_SIZE

    new_head = (head_x, head_y)

    # ===== COLLISION WITH WALLS =====
    if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
        game_over()

    # ===== COLLISION WITH ITSELF =====
    if new_head in snake:
        game_over()

    # Add new head to the beginning of the snake
    snake.insert(0, new_head)

    # ===== FOOD TIMER =====
    # If food exists for too long, it disappears and new food appears
    current_time = time.time()
    elapsed_time = current_time - food["created_time"]

    if elapsed_time >= FOOD_LIFETIME:
        food = generate_food()

    # ===== CHECK FOOD EATING =====
    if new_head == food["position"]:
        # Add score according to food weight
        score += food["value"]

        # Food counter for level system
        food_eaten_on_level += 1

        # Snake grows depending on food value
        # We do not remove tail immediately for value amount
        for i in range(food["value"] - 1):
            snake.append(snake[-1])

        # Level up after eating required amount of food
        if food_eaten_on_level >= foods_to_next_level:
            level += 1
            speed += 2
            food_eaten_on_level = 0
            foods_to_next_level += 1

        # Generate new food after eating
        food = generate_food()
    else:
        # If food was not eaten, remove tail to keep snake same length
        snake.pop()

    # ===== DRAWING =====
    screen.fill(BLACK)

    # Draw food
    food_x, food_y = food["position"]
    pygame.draw.rect(screen, food["color"], (food_x, food_y, CELL_SIZE, CELL_SIZE))

    # Show food value on top of food
    value_text = font.render(str(food["value"]), True, BLACK)
    screen.blit(value_text, (food_x + 4, food_y - 2))

    # Draw snake
    for part in snake:
        pygame.draw.rect(screen, GREEN, (part[0], part[1], CELL_SIZE, CELL_SIZE))

    # Timer display for current food
    time_left = max(0, int(FOOD_LIFETIME - elapsed_time))

    # Draw score, level and food information
    draw_text("Score: " + str(score), 10, 10)
    draw_text("Level: " + str(level), 10, 35)
    draw_text("Food to next level: " + str(foods_to_next_level - food_eaten_on_level), 10, 60)
    draw_text("Food value: " + str(food["value"]), 10, 85)
    draw_text("Food timer: " + str(time_left), 10, 110)

    pygame.display.update()
    clock.tick(speed)
