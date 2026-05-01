import pygame
import sys
import random
import time
import json
import os
from pygame.locals import *

pygame.init()
pygame.mixer.init()

FPS = 60
clock = pygame.time.Clock()

WIDTH = 400
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS 3 Racer")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
GREEN = (0, 200, 0)
BLUE = (0, 120, 255)
GRAY = (120, 120, 120)
DARK = (40, 40, 40)
PURPLE = (160, 60, 220)
CYAN = (0, 220, 220)

ROAD_LEFT = 40
ROAD_RIGHT = 360
LANES = [80, 160, 240, 320]
FINISH_DISTANCE = 3000

ASSETS = "assets"
SETTINGS_FILE = "settings.json"
LEADERBOARD_FILE = "leaderboard.json"

font_big = pygame.font.SysFont("Verdana", 42)
font_mid = pygame.font.SysFont("Verdana", 24)
font_small = pygame.font.SysFont("Verdana", 18)

default_settings = {
    "sound": True,
    "car_color": "blue",
    "difficulty": "normal"
}


def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        save_settings(default_settings)
        return default_settings.copy()

    with open(SETTINGS_FILE, "r") as file:
        data = json.load(file)

    settings = default_settings.copy()
    settings.update(data)
    return settings


def save_settings(settings):
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file, indent=4)


def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        save_leaderboard([])
        return []

    with open(LEADERBOARD_FILE, "r") as file:
        return json.load(file)


def save_leaderboard(data):
    with open(LEADERBOARD_FILE, "w") as file:
        json.dump(data, file, indent=4)


def add_score(name, score, distance, coins):
    data = load_leaderboard()

    data.append({
        "name": name,
        "score": int(score),
        "distance": int(distance),
        "coins": int(coins)
    })

    data.sort(key=lambda x: x["score"], reverse=True)
    save_leaderboard(data[:10])


def draw_text(text, x, y, color=BLACK):
    img = font_small.render(text, True, color)
    screen.blit(img, (x, y))


def play_crash(settings):
    if settings["sound"]:
        try:
            pygame.mixer.Sound(os.path.join(ASSETS, "crash.wav")).play()
        except:
            pass


class Button:
    def __init__(self, text, x, y, w, h):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self):
        mouse = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse):
            color = (200, 200, 200)
        else:
            color = (230, 230, 230)

        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=10)

        img = font_small.render(self.text, True, BLACK)
        rect = img.get_rect(center=self.rect.center)
        screen.blit(img, rect)

    def clicked(self, event):
        return event.type == MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)


class Player(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()

        if color == "red":
            car_color = RED
        elif color == "green":
            car_color = GREEN
        elif color == "yellow":
            car_color = YELLOW
        else:
            car_color = BLUE

        try:
            if color == "blue":
                self.image = pygame.image.load(os.path.join(ASSETS, "Player.png")).convert_alpha()
            else:
                self.image = self.create_car(car_color)
        except:
            self.image = self.create_car(car_color)

        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, 520)
        self.speed = 6
        self.shield = False

    def create_car(self, color):
        img = pygame.Surface((45, 85), pygame.SRCALPHA)
        pygame.draw.rect(img, color, (6, 5, 33, 75), border_radius=8)
        pygame.draw.rect(img, BLACK, (12, 14, 21, 18), border_radius=4)
        pygame.draw.rect(img, BLACK, (12, 50, 21, 18), border_radius=4)
        return img

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[K_LEFT] and self.rect.left > ROAD_LEFT:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.right < ROAD_RIGHT:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.top > 100:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed


class Traffic(pygame.sprite.Sprite):
    def __init__(self, speed, player_x):
        super().__init__()

        try:
            self.image = pygame.image.load(os.path.join(ASSETS, "Enemy.png")).convert_alpha()
        except:
            self.image = pygame.Surface((45, 85), pygame.SRCALPHA)
            pygame.draw.rect(self.image, RED, (6, 5, 33, 75), border_radius=8)

        self.rect = self.image.get_rect()

        safe_lanes = [lane for lane in LANES if abs(lane - player_x) > 50]
        if not safe_lanes:
            safe_lanes = LANES

        self.rect.center = (random.choice(safe_lanes), random.randint(-500, -80))
        self.speed = speed

    def move(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()


class Coin(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.speed = speed
        self.weight = random.choice([1, 2, 3])

        if self.weight == 1:
            radius = 10
            color = YELLOW
        elif self.weight == 2:
            radius = 13
            color = ORANGE
        else:
            radius = 16
            color = WHITE

        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        pygame.draw.circle(self.image, BLACK, (radius, radius), radius, 2)

        self.rect = self.image.get_rect()
        self.rect.center = (random.choice(LANES), random.randint(-500, -50))

    def move(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, speed, player_x):
        super().__init__()
        self.speed = speed
        self.kind = random.choice(["barrier", "oil", "pothole", "slow"])

        self.image = pygame.Surface((55, 35), pygame.SRCALPHA)

        if self.kind == "barrier":
            pygame.draw.rect(self.image, ORANGE, (0, 5, 55, 25), border_radius=5)
            pygame.draw.line(self.image, BLACK, (5, 10), (50, 28), 4)

        elif self.kind == "oil":
            pygame.draw.ellipse(self.image, BLACK, (3, 4, 50, 28))
            pygame.draw.ellipse(self.image, DARK, (12, 9, 25, 12))

        elif self.kind == "pothole":
            pygame.draw.ellipse(self.image, DARK, (2, 2, 52, 30))
            pygame.draw.ellipse(self.image, BLACK, (10, 8, 34, 17))

        elif self.kind == "slow":
            pygame.draw.rect(self.image, CYAN, (0, 0, 55, 35), border_radius=5)
            pygame.draw.line(self.image, WHITE, (5, 10), (50, 10), 3)
            pygame.draw.line(self.image, WHITE, (5, 25), (50, 25), 3)

        self.rect = self.image.get_rect()

        safe_lanes = [lane for lane in LANES if abs(lane - player_x) > 50]
        if not safe_lanes:
            safe_lanes = LANES

        self.rect.center = (random.choice(safe_lanes), random.randint(-600, -100))

    def move(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.speed = speed
        self.kind = random.choice(["nitro", "shield", "repair"])
        self.spawn_time = time.time()
        self.life_time = 6

        self.image = pygame.Surface((34, 34), pygame.SRCALPHA)

        if self.kind == "nitro":
            color = PURPLE
            letter = "N"
        elif self.kind == "shield":
            color = BLUE
            letter = "S"
        else:
            color = GREEN
            letter = "R"

        pygame.draw.circle(self.image, color, (17, 17), 17)
        pygame.draw.circle(self.image, WHITE, (17, 17), 17, 2)

        text = font_small.render(letter, True, WHITE)
        self.image.blit(text, (10, 5))

        self.rect = self.image.get_rect()
        self.rect.center = (random.choice(LANES), random.randint(-700, -120))

    def move(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.kill()

        if time.time() - self.spawn_time > self.life_time:
            self.kill()


class MovingBarrier(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()

        self.image = pygame.Surface((90, 25), pygame.SRCALPHA)
        pygame.draw.rect(self.image, ORANGE, (0, 0, 90, 25), border_radius=5)
        pygame.draw.line(self.image, BLACK, (5, 5), (85, 20), 4)

        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, random.randint(-700, -150))
        self.speed = speed
        self.side_speed = random.choice([-2, 2])

    def move(self):
        self.rect.y += self.speed
        self.rect.x += self.side_speed

        if self.rect.left < ROAD_LEFT or self.rect.right > ROAD_RIGHT:
            self.side_speed *= -1

        if self.rect.top > HEIGHT:
            self.kill()


def draw_road(distance):
    try:
        bg = pygame.image.load(os.path.join(ASSETS, "AnimatedStreet.png"))
        screen.blit(bg, (0, 0))
    except:
        screen.fill(DARK)
        pygame.draw.rect(screen, GRAY, (ROAD_LEFT, 0, ROAD_RIGHT - ROAD_LEFT, HEIGHT))
        pygame.draw.line(screen, YELLOW, (ROAD_LEFT, 0), (ROAD_LEFT, HEIGHT), 3)
        pygame.draw.line(screen, YELLOW, (ROAD_RIGHT, 0), (ROAD_RIGHT, HEIGHT), 3)

        offset = int(distance % 80)

        for y in range(-80, HEIGHT, 80):
            pygame.draw.rect(screen, WHITE, (135, y + offset, 15, 45))
            pygame.draw.rect(screen, WHITE, (215, y + offset, 15, 45))
            pygame.draw.rect(screen, WHITE, (295, y + offset, 15, 45))


def username_screen():
    name = ""

    while True:
        screen.fill(WHITE)

        title = font_big.render("Enter Name", True, BLACK)
        screen.blit(title, (70, 100))

        box = pygame.Rect(60, 250, 280, 45)
        pygame.draw.rect(screen, (230, 230, 230), box)
        pygame.draw.rect(screen, BLACK, box, 2)

        text = font_mid.render(name, True, BLACK)
        screen.blit(text, (box.x + 10, box.y + 8))

        draw_text("Press ENTER to start", 90, 320)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_RETURN and name.strip():
                    return name.strip()
                elif event.key == K_BACKSPACE:
                    name = name[:-1]
                else:
                    if len(name) < 12:
                        name += event.unicode

        pygame.display.update()
        clock.tick(FPS)


def settings_screen():
    settings = load_settings()

    sound_btn = Button("Toggle Sound", 95, 150, 210, 45)
    color_btn = Button("Change Car Color", 95, 220, 210, 45)
    diff_btn = Button("Change Difficulty", 95, 290, 210, 45)
    back_btn = Button("Back", 120, 500, 160, 45)

    colors = ["blue", "red", "green", "yellow"]
    difficulties = ["easy", "normal", "hard"]

    while True:
        screen.fill(WHITE)

        title = font_big.render("Settings", True, BLACK)
        screen.blit(title, (85, 70))

        draw_text("Sound: " + ("ON" if settings["sound"] else "OFF"), 100, 120)
        draw_text("Car color: " + settings["car_color"], 100, 190)
        draw_text("Difficulty: " + settings["difficulty"], 100, 260)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if sound_btn.clicked(event):
                settings["sound"] = not settings["sound"]
                save_settings(settings)

            elif color_btn.clicked(event):
                i = colors.index(settings["car_color"])
                settings["car_color"] = colors[(i + 1) % len(colors)]
                save_settings(settings)

            elif diff_btn.clicked(event):
                i = difficulties.index(settings["difficulty"])
                settings["difficulty"] = difficulties[(i + 1) % len(difficulties)]
                save_settings(settings)

            elif back_btn.clicked(event):
                return

        sound_btn.draw()
        color_btn.draw()
        diff_btn.draw()
        back_btn.draw()

        pygame.display.update()
        clock.tick(FPS)


def leaderboard_screen():
    back_btn = Button("Back", 120, 520, 160, 45)

    while True:
        screen.fill(WHITE)

        title = font_big.render("Top 10", True, BLACK)
        screen.blit(title, (120, 60))

        data = load_leaderboard()

        if not data:
            empty = font_mid.render("No scores yet", True, BLACK)
            screen.blit(empty, (100, 230))
        else:
            draw_text("Rank  Name       Score   Dist", 25, 110)

            y = 140
            for i, item in enumerate(data[:10], start=1):
                line = f"{i:<5} {item['name']:<10} {item['score']:<7} {item['distance']}m"
                draw_text(line, 25, y)
                y += 35

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if back_btn.clicked(event):
                return

        back_btn.draw()

        pygame.display.update()
        clock.tick(FPS)


def game_over_screen(username, score, distance, coins):
    retry_btn = Button("Retry", 95, 360, 210, 45)
    menu_btn = Button("Main Menu", 95, 425, 210, 45)

    while True:
        screen.fill(WHITE)

        title = font_big.render("Game Over", True, RED)
        screen.blit(title, (65, 90))

        draw_text("Player: " + username, 110, 180)
        draw_text("Score: " + str(int(score)), 110, 215)
        draw_text("Distance: " + str(int(distance)) + "m", 110, 250)
        draw_text("Coins: " + str(coins), 110, 285)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if retry_btn.clicked(event):
                game_loop(username, load_settings())
                return

            elif menu_btn.clicked(event):
                return

        retry_btn.draw()
        menu_btn.draw()

        pygame.display.update()
        clock.tick(FPS)


def game_loop(username, settings):
    speed = 5
    score = 0
    coins_count = 0
    distance = 0

    active_power = None
    power_end_time = 0

    if settings["difficulty"] == "easy":
        speed = 4
        spawn_modifier = 1.4
    elif settings["difficulty"] == "hard":
        speed = 6
        spawn_modifier = 0.7
    else:
        speed = 5
        spawn_modifier = 1.0

    try:
        pygame.mixer.music.load(os.path.join(ASSETS, "background.wav"))
        if settings["sound"]:
            pygame.mixer.music.play(-1)
    except:
        pass

    player = Player(settings["car_color"])

    all_sprites = pygame.sprite.Group(player)
    traffic = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    events = pygame.sprite.Group()

    traffic_timer = 0
    coin_timer = 0
    obstacle_timer = 0
    power_timer = 0
    event_timer = 0

    while True:
        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        difficulty_level = 1 + distance // 700
        current_speed = speed + difficulty_level * 0.4

        distance += current_speed * 0.12
        score += current_speed * 0.03

        traffic_interval = max(450, int((1400 / spawn_modifier) - difficulty_level * 70))
        obstacle_interval = max(650, int((1900 / spawn_modifier) - difficulty_level * 70))

        if now - traffic_timer > traffic_interval:
            obj = Traffic(current_speed + 2, player.rect.centerx)
            traffic.add(obj)
            all_sprites.add(obj)
            traffic_timer = now

        if now - coin_timer > 900:
            obj = Coin(current_speed)
            coins.add(obj)
            all_sprites.add(obj)
            coin_timer = now

        if now - obstacle_timer > obstacle_interval:
            obj = Obstacle(current_speed, player.rect.centerx)
            obstacles.add(obj)
            all_sprites.add(obj)
            obstacle_timer = now

        if now - power_timer > 7000:
            obj = PowerUp(current_speed)
            powerups.add(obj)
            all_sprites.add(obj)
            power_timer = now

        if now - event_timer > 6000:
            obj = MovingBarrier(current_speed)
            events.add(obj)
            all_sprites.add(obj)
            event_timer = now

        player.move()

        for sprite in all_sprites:
            if sprite != player:
                sprite.move()

        collected = pygame.sprite.spritecollide(player, coins, True)
        for coin in collected:
            coins_count += coin.weight
            score += coin.weight * 10

        collected_powerups = pygame.sprite.spritecollide(player, powerups, True)
        for power in collected_powerups:
            if active_power is None:
                if power.kind == "nitro":
                    active_power = "Nitro"
                    power_end_time = time.time() + 4
                    speed += 3
                    score += 50

                elif power.kind == "shield":
                    active_power = "Shield"
                    player.shield = True

                elif power.kind == "repair":
                    active_power = "Repair"
                    power_end_time = time.time() + 1

                    for obstacle in obstacles:
                        obstacle.kill()
                        score += 25
                        break

        if active_power == "Nitro" and time.time() >= power_end_time:
            speed -= 3
            active_power = None

        if active_power == "Repair" and time.time() >= power_end_time:
            active_power = None

        if active_power == "Shield" and not player.shield:
            active_power = None

        if pygame.sprite.spritecollideany(player, traffic):
            if player.shield:
                player.shield = False
                pygame.sprite.spritecollide(player, traffic, True)
            else:
                play_crash(settings)
                break

        if pygame.sprite.spritecollideany(player, events):
            if player.shield:
                player.shield = False
                pygame.sprite.spritecollide(player, events, True)
            else:
                play_crash(settings)
                break

        hit_obstacles = pygame.sprite.spritecollide(player, obstacles, True)

        for obstacle in hit_obstacles:
            if player.shield:
                player.shield = False

            elif obstacle.kind == "oil":
                player.rect.x += random.choice([-60, 60])
                player.rect.clamp_ip(pygame.Rect(ROAD_LEFT, 0, ROAD_RIGHT - ROAD_LEFT, HEIGHT))

            elif obstacle.kind == "slow":
                player.speed = max(3, player.speed - 1)
                score -= 5

            else:
                play_crash(settings)
                add_score(username, score, distance, coins_count)
                game_over_screen(username, score, distance, coins_count)
                return

        if distance >= FINISH_DISTANCE:
            score += 500
            break

        draw_road(distance)

        for sprite in all_sprites:
            screen.blit(sprite.image, sprite.rect)

        if player.shield:
            pygame.draw.circle(screen, CYAN, player.rect.center, 55, 3)

        remaining = max(0, FINISH_DISTANCE - int(distance))

        draw_text("Player: " + username, 10, 10)
        draw_text("Score: " + str(int(score)), 10, 35)
        draw_text("Coins: " + str(coins_count), 10, 60)
        draw_text("Distance: " + str(int(distance)) + "m", 10, 85)
        draw_text("Remaining: " + str(remaining) + "m", 10, 110)

        if active_power is None:
            power_text = "Power: none"
        elif active_power in ["Nitro", "Repair"]:
            left = max(0, int(power_end_time - time.time()))
            power_text = "Power: " + active_power + " " + str(left) + "s"
        else:
            power_text = "Power: Shield"

        draw_text(power_text, 205, 10)

        pygame.display.update()
        clock.tick(FPS)

    add_score(username, score, distance, coins_count)
    game_over_screen(username, score, distance, coins_count)


def main_menu():
    play_btn = Button("Play", 110, 160, 180, 45)
    leaderboard_btn = Button("Leaderboard", 110, 220, 180, 45)
    settings_btn = Button("Settings", 110, 280, 180, 45)
    quit_btn = Button("Quit", 110, 340, 180, 45)

    while True:
        screen.fill(WHITE)

        title = font_big.render("Racer", True, BLACK)
        screen.blit(title, (125, 80))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if play_btn.clicked(event):
                username = username_screen()
                game_loop(username, load_settings())

            elif leaderboard_btn.clicked(event):
                leaderboard_screen()

            elif settings_btn.clicked(event):
                settings_screen()

            elif quit_btn.clicked(event):
                pygame.quit()
                sys.exit()

        play_btn.draw()
        leaderboard_btn.draw()
        settings_btn.draw()
        quit_btn.draw()

        pygame.display.update()
        clock.tick(FPS)


main_menu()