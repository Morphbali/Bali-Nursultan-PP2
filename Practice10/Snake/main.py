import pygame
import random
import sys
import json
import os
import db

pygame.init()

WIDTH = 600
HEIGHT = 400
CELL = 20
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS 4 Snake")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (220, 0, 0)
DARK_RED = (100, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (160, 32, 240)
BLUE = (0, 120, 255)
CYAN = (0, 220, 220)
GRAY = (80, 80, 80)
ORANGE = (255, 165, 0)

font = pygame.font.SysFont("Verdana", 18)
big_font = pygame.font.SysFont("Verdana", 42)
small_font = pygame.font.SysFont("Verdana", 14)

SETTINGS_FILE = "settings.json"
DEFAULT_SETTINGS = {
    "snake_color": [0, 200, 0],
    "grid": True,
    "sound": True
}

FOOD_LIFETIME = 5000
POWERUP_LIFETIME = 8000
POWERUP_DURATION = 5000


def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
        settings = DEFAULT_SETTINGS.copy()
        settings.update(data)
        return settings
    except Exception:
        return DEFAULT_SETTINGS.copy()


def save_settings(settings):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4)


def draw_text(text, x, y, color=WHITE, fnt=None):
    if fnt is None:
        fnt = font
    img = fnt.render(text, True, color)
    screen.blit(img, (x, y))


class Button:
    def __init__(self, text, x, y, w, h):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self):
        mouse = pygame.mouse.get_pos()
        color = (210, 210, 210) if self.rect.collidepoint(mouse) else (235, 235, 235)
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=8)
        img = font.render(self.text, True, BLACK)
        screen.blit(img, img.get_rect(center=self.rect.center))

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)


def all_cells():
    return [(x, y) for x in range(0, WIDTH, CELL) for y in range(0, HEIGHT, CELL)]


def random_cell(forbidden):
    choices = [cell for cell in all_cells() if cell not in forbidden]
    if not choices:
        return (0, 0)
    return random.choice(choices)


def generate_food(snake, obstacles):
    forbidden = set(snake) | set(obstacles)
    pos = random_cell(forbidden)
    value = random.choice([1, 2, 3])
    color = RED if value == 1 else YELLOW if value == 2 else PURPLE
    return {
        "pos": pos,
        "value": value,
        "color": color,
        "spawn_time": pygame.time.get_ticks()
    }


def generate_poison(snake, obstacles, food_pos):
    forbidden = set(snake) | set(obstacles) | {food_pos}
    return {
        "pos": random_cell(forbidden),
        "spawn_time": pygame.time.get_ticks()
    }


def generate_powerup(snake, obstacles, food_pos, poison_pos):
    forbidden = set(snake) | set(obstacles) | {food_pos, poison_pos}
    kind = random.choice(["speed", "slow", "shield"])
    colors = {"speed": ORANGE, "slow": CYAN, "shield": BLUE}
    letters = {"speed": "F", "slow": "S", "shield": "H"}
    return {
        "pos": random_cell(forbidden),
        "kind": kind,
        "color": colors[kind],
        "letter": letters[kind],
        "spawn_time": pygame.time.get_ticks()
    }


def generate_obstacles(level, snake, food_pos=None, poison_pos=None):
    if level < 3:
        return []

    forbidden = set(snake)
    if food_pos:
        forbidden.add(food_pos)
    if poison_pos:
        forbidden.add(poison_pos)

    head = snake[0]
    safe_area = [
        head,
        (head[0] + CELL, head[1]),
        (head[0] - CELL, head[1]),
        (head[0], head[1] + CELL),
        (head[0], head[1] - CELL),
    ]
    forbidden |= set(safe_area)

    count = min(4 + level, 14)
    blocks = []

    for _ in range(count):
        pos = random_cell(forbidden | set(blocks))
        blocks.append(pos)

    return blocks


def draw_grid():
    for x in range(0, WIDTH, CELL):
        pygame.draw.line(screen, (30, 30, 30), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL):
        pygame.draw.line(screen, (30, 30, 30), (0, y), (WIDTH, y))


def username_screen():
    name = ""
    while True:
        screen.fill(BLACK)
        draw_text("Enter Username", 135, 90, WHITE, big_font)
        pygame.draw.rect(screen, WHITE, (120, 190, 360, 45), 2)
        draw_text(name, 130, 200, WHITE, font)
        draw_text("Press ENTER to continue", 170, 260, WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name.strip():
                    return name.strip()
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 15 and event.unicode.isascii() and event.unicode.isprintable():
                    name += event.unicode

        pygame.display.update()
        clock.tick(FPS)


def main_menu():
    username = "Player"
    play = Button("Play", 210, 130, 180, 45)
    leaderboard = Button("Leaderboard", 210, 190, 180, 45)
    settings = Button("Settings", 210, 250, 180, 45)
    quit_btn = Button("Quit", 210, 310, 180, 45)

    while True:
        screen.fill(BLACK)
        draw_text("Snake TSIS 4", 150, 45, GREEN, big_font)
        draw_text("PostgreSQL + Power-ups", 175, 95, WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if play.clicked(event):
                username = username_screen()
                game_loop(username)
            elif leaderboard.clicked(event):
                leaderboard_screen()
            elif settings.clicked(event):
                settings_screen()
            elif quit_btn.clicked(event):
                pygame.quit()
                sys.exit()

        play.draw()
        leaderboard.draw()
        settings.draw()
        quit_btn.draw()
        pygame.display.update()
        clock.tick(FPS)


def leaderboard_screen():
    back = Button("Back", 220, 340, 160, 40)

    while True:
        screen.fill(BLACK)
        draw_text("Leaderboard", 165, 35, GREEN, big_font)
        draw_text("Rank  Name          Score  Lvl  Date", 35, 105, WHITE, small_font)
        rows = db.get_top_scores()

        if not rows:
            draw_text("No scores yet or database not connected", 120, 190, RED, small_font)
        else:
            y = 135
            for i, row in enumerate(rows, start=1):
                username, score, level, date = row
                line = f"{i:<5} {username:<13} {score:<6} {level:<4} {date}"
                draw_text(line, 35, y, WHITE, small_font)
                y += 25

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if back.clicked(event):
                return

        back.draw()
        pygame.display.update()
        clock.tick(FPS)


def settings_screen():
    settings = load_settings()
    colors = [[0, 200, 0], [0, 120, 255], [255, 255, 0], [160, 32, 240]]

    grid_btn = Button("Toggle Grid", 200, 130, 200, 40)
    sound_btn = Button("Toggle Sound", 200, 190, 200, 40)
    color_btn = Button("Change Color", 200, 250, 200, 40)
    save_btn = Button("Save & Back", 200, 320, 200, 40)

    while True:
        screen.fill(BLACK)
        draw_text("Settings", 200, 45, GREEN, big_font)
        draw_text(f"Grid: {'ON' if settings['grid'] else 'OFF'}", 70, 138)
        draw_text(f"Sound: {'ON' if settings['sound'] else 'OFF'}", 70, 198)
        draw_text(f"Color: {settings['snake_color']}", 70, 258)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if grid_btn.clicked(event):
                settings["grid"] = not settings["grid"]
            elif sound_btn.clicked(event):
                settings["sound"] = not settings["sound"]
            elif color_btn.clicked(event):
                i = colors.index(settings["snake_color"]) if settings["snake_color"] in colors else 0
                settings["snake_color"] = colors[(i + 1) % len(colors)]
            elif save_btn.clicked(event):
                save_settings(settings)
                return

        grid_btn.draw()
        sound_btn.draw()
        color_btn.draw()
        save_btn.draw()
        pygame.display.update()
        clock.tick(FPS)


def game_over_screen(username, score, level, best):
    retry = Button("Retry", 200, 250, 180, 45)
    menu = Button("Main Menu", 200, 310, 180, 45)

    while True:
        screen.fill(BLACK)
        draw_text("Game Over", 170, 60, RED, big_font)
        draw_text(f"Player: {username}", 185, 135)
        draw_text(f"Score: {score}", 185, 165)
        draw_text(f"Level: {level}", 185, 195)
        draw_text(f"Personal best: {max(best, score)}", 185, 225)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if retry.clicked(event):
                game_loop(username)
                return
            elif menu.clicked(event):
                return

        retry.draw()
        menu.draw()
        pygame.display.update()
        clock.tick(FPS)


def game_loop(username):
    settings = load_settings()
    snake_color = tuple(settings["snake_color"])
    personal_best = db.get_personal_best(username)

    snake = [(100, 100), (80, 100), (60, 100)]
    direction = "RIGHT"
    next_direction = "RIGHT"
    score = 0
    level = 1
    base_speed = 8
    speed = base_speed
    food_eaten = 0
    food_needed = 3

    obstacles = []
    food = generate_food(snake, obstacles)
    poison = generate_poison(snake, obstacles, food["pos"])
    powerup = None

    active_power = None
    active_power_until = 0
    shield = False

    while True:
        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != "DOWN":
                    next_direction = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    next_direction = "DOWN"
                elif event.key == pygame.K_LEFT and direction != "RIGHT":
                    next_direction = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    next_direction = "RIGHT"
                elif event.key == pygame.K_ESCAPE:
                    return

        direction = next_direction
        head_x, head_y = snake[0]

        if direction == "UP":
            head_y -= CELL
        elif direction == "DOWN":
            head_y += CELL
        elif direction == "LEFT":
            head_x -= CELL
        elif direction == "RIGHT":
            head_x += CELL

        new_head = (head_x, head_y)

        collision = False
        if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
            collision = True
        if new_head in snake:
            collision = True
        if new_head in obstacles:
            collision = True

        if collision:
            if shield:
                shield = False
                active_power = None
                # move head back instead of dying
                new_head = snake[0]
            else:
                db.save_result(username, score, level)
                game_over_screen(username, score, level, personal_best)
                return

        snake.insert(0, new_head)

        if now - food["spawn_time"] >= FOOD_LIFETIME:
            food = generate_food(snake, obstacles)

        if now - poison["spawn_time"] >= FOOD_LIFETIME + 2000:
            poison = generate_poison(snake, obstacles, food["pos"])

        if powerup is None and random.randint(1, 220) == 1:
            powerup = generate_powerup(snake, obstacles, food["pos"], poison["pos"])

        if powerup is not None and now - powerup["spawn_time"] > POWERUP_LIFETIME:
            powerup = None

        if active_power in ["speed", "slow"] and now >= active_power_until:
            active_power = None
            speed = base_speed + (level - 1) * 2

        grew = False

        if new_head == food["pos"]:
            score += food["value"]
            food_eaten += 1
            grew = True

            for _ in range(food["value"] - 1):
                snake.append(snake[-1])

            if food_eaten >= food_needed:
                level += 1
                base_speed += 2
                speed = base_speed
                food_eaten = 0
                food_needed += 1
                obstacles = generate_obstacles(level, snake, food["pos"], poison["pos"])

            food = generate_food(snake, obstacles)

        elif new_head == poison["pos"]:
            # poison shortens snake by 2 segments
            for _ in range(2):
                if len(snake) > 1:
                    snake.pop()
            if len(snake) <= 1:
                db.save_result(username, score, level)
                game_over_screen(username, score, level, personal_best)
                return
            poison = generate_poison(snake, obstacles, food["pos"])
            snake.pop()

        elif powerup is not None and new_head == powerup["pos"]:
            kind = powerup["kind"]
            active_power = kind
            powerup = None

            if kind == "speed":
                speed = base_speed + (level - 1) * 2 + 5
                active_power_until = now + POWERUP_DURATION
            elif kind == "slow":
                speed = max(4, base_speed + (level - 1) * 2 - 4)
                active_power_until = now + POWERUP_DURATION
            elif kind == "shield":
                shield = True

            snake.pop()

        else:
            if not grew:
                snake.pop()

        screen.fill(BLACK)

        if settings["grid"]:
            draw_grid()

        for block in obstacles:
            pygame.draw.rect(screen, GRAY, (block[0], block[1], CELL, CELL))

        pygame.draw.rect(screen, food["color"], (food["pos"][0], food["pos"][1], CELL, CELL))
        value_img = small_font.render(str(food["value"]), True, BLACK)
        screen.blit(value_img, (food["pos"][0] + 5, food["pos"][1] + 1))

        pygame.draw.rect(screen, DARK_RED, (poison["pos"][0], poison["pos"][1], CELL, CELL))
        draw_text("P", poison["pos"][0] + 4, poison["pos"][1] - 2, WHITE, small_font)

        if powerup is not None:
            pygame.draw.rect(screen, powerup["color"], (powerup["pos"][0], powerup["pos"][1], CELL, CELL))
            draw_text(powerup["letter"], powerup["pos"][0] + 4, powerup["pos"][1] - 2, WHITE, small_font)

        for part in snake:
            pygame.draw.rect(screen, snake_color, (part[0], part[1], CELL, CELL))

        if shield:
            pygame.draw.rect(screen, CYAN, (snake[0][0], snake[0][1], CELL, CELL), 3)

        food_time = max(0, (FOOD_LIFETIME - (now - food["spawn_time"])) // 1000)
        power_text = "None"
        if active_power == "speed":
            power_text = f"Speed {max(0, (active_power_until - now) // 1000)}s"
        elif active_power == "slow":
            power_text = f"Slow {max(0, (active_power_until - now) // 1000)}s"
        elif active_power == "shield":
            power_text = "Shield"

        draw_text(f"Player: {username}", 10, 10)
        draw_text(f"Score: {score}", 10, 35)
        draw_text(f"Level: {level}", 10, 60)
        draw_text(f"Best: {personal_best}", 10, 85)
        draw_text(f"Food timer: {food_time}s", 10, 110)
        draw_text(f"Power: {power_text}", 10, 135)

        pygame.display.update()
        clock.tick(speed)


if __name__ == "__main__":
    db.setup_database()
    main_menu()
