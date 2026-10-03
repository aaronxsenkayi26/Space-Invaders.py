import random
import subprocess
import sys

try:
    import pygame
except ImportError:
    print("Pygame not found. Automatically running 'pip install pygame'...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
        import pygame
        print("Pygame installed successfully!")
    except Exception as error:
        print(f"Failed to automatically install Pygame: {error}")
        sys.exit(1)


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
ALIEN_WIDTH = 40
ALIEN_HEIGHT = 32
ALIEN_ROWS = 5
ALIEN_COLUMNS = 11
ALIEN_START_X = 90
ALIEN_START_Y = 88
ALIEN_GAP_X = 18
ALIEN_GAP_Y = 46
INVASION_LINE = SCREEN_HEIGHT - 100

BLACK = (5, 8, 18)
WHITE = (238, 244, 255)
GREEN = (88, 245, 125)
RED = (255, 88, 100)
YELLOW = (255, 224, 91)
CYAN = (100, 222, 255)
ORANGE = (255, 163, 77)
BUTTON_BG = (30, 45, 55)
BUTTON_ACTIVE = (45, 115, 80)
SHIELD_COLOR = (80, 215, 130)

ALIEN_COLORS = (
    (255, 95, 107),
    (255, 176, 83),
    (117, 224, 255),
)
ALIEN_FRAMES = (
    (
        ("..####..", ".######.", "##.##.##", "########", "..####..", ".##..##.", "##....##", ".##..##."),
        ("..####..", ".######.", "##.##.##", "########", "..####..", "##....##", ".##..##.", "##....##"),
    ),
    (
        (".##..##.", "..######", ".#######", "##.##.##", "########", ".##.##..", "##....##", ".##..##."),
        (".##..##.", "..######", ".#######", "##.##.##", "########", "..##.##.", ".##..##.", "##....##"),
    ),
    (
        ("...##...", "..####..", ".######.", "##.##.##", "########", "##.##.##", "##....##", ".##..##."),
        ("...##...", "..####..", ".######.", "##.##.##", "########", ".######.", "..#..#..", ".##..##."),
    ),
)


class Player:
    width = 48
    height = 32
    y = SCREEN_HEIGHT - 72
    speed = 330

    def __init__(self):
        self.x = (SCREEN_WIDTH - self.width) / 2
        self.invulnerability = 0.0

    @property
    def rect(self):
        return pygame.Rect(round(self.x), self.y, self.width, self.height)

    def move(self, direction, delta_time):
        self.x += direction * self.speed * delta_time
        self.x = max(0, min(SCREEN_WIDTH - self.width, self.x))

    def draw(self, surface, ticks):
        if self.invulnerability > 0 and ticks // 100 % 2:
            return
        x = round(self.x)
        y = self.y
        pygame.draw.polygon(surface, GREEN, (
            (x + 24, y), (x + 30, y + 13), (x + 47, y + 25),
            (x + 47, y + 31), (x + 1, y + 31), (x + 1, y + 25),
            (x + 18, y + 13),
        ))
        pygame.draw.rect(surface, WHITE, (x + 22, y + 12, 4, 8))
        pygame.draw.rect(surface, GREEN, (x + 22, y + 25, 4, 6))


class Alien:
    def __init__(self, x, y, row):
        self.x = float(x)
        self.y = float(y)
        self.row = row
        self.points = 30 if row == 0 else 20 if row == 1 else 10

    @property
    def rect(self):
        return pygame.Rect(round(self.x), round(self.y), ALIEN_WIDTH, ALIEN_HEIGHT)

    def draw(self, surface, ticks):
        sprite_type = min(self.row, 2)
        frame = (ticks // 360) % 2
        pattern = ALIEN_FRAMES[sprite_type][frame]
        color = ALIEN_COLORS[sprite_type]
        cell_width = ALIEN_WIDTH // 8
        cell_height = ALIEN_HEIGHT // 8
        for row_index, line in enumerate(pattern):
            for column_index, pixel in enumerate(line):
                if pixel == "#":
                    pygame.draw.rect(
                        surface,
                        color,
                        (
                            round(self.x) + column_index * cell_width,
                            round(self.y) + row_index * cell_height,
                            cell_width,
                            cell_height,
                        ),
                    )


class Shot:
    def __init__(self, x, y, speed, color, zigzag=False):
        self.x = float(x)
        self.y = float(y)
        self.speed = speed
        self.color = color
        self.zigzag = zigzag
        self.direction = 1
        self.turn_timer = 0.0

    @property
    def rect(self):
        return pygame.Rect(round(self.x) - 3, round(self.y), 6, 16)

    def update(self, delta_time):
        self.y += self.speed * delta_time
        if self.zigzag:
            self.turn_timer += delta_time
            if self.turn_timer >= 0.16:
                self.turn_timer = 0.0
                self.direction *= -1
            self.x += self.direction * 70 * delta_time

    def draw(self, surface):
        if self.speed < 0:
            pygame.draw.rect(surface, self.color, self.rect)
            pygame.draw.rect(surface, WHITE, self.rect.inflate(-2, -2))
        else:
            rect = self.rect
            pygame.draw.line(surface, self.color, rect.midtop, rect.midbottom, 4)
            pygame.draw.line(surface, WHITE, rect.midtop, rect.midbottom, 1)


class Shield:
    pattern = (
        "..######..",
        ".########.",
        "##########",
        "##########",
        "##########",
        "####..####",
        "###....###",
    )
    block_size = 7

    def __init__(self, x):
        self.blocks = []
        for row, line in enumerate(self.pattern):
            for column, pixel in enumerate(line):
                if pixel == "#":
                    self.blocks.append(pygame.Rect(
                        x + column * self.block_size,
                        440 + row * self.block_size,
                        self.block_size,
                        self.block_size,
                    ))

    def draw(self, surface):
        for block in self.blocks:
            pygame.draw.rect(surface, SHIELD_COLOR, block)


class GameState:
    def __init__(self):
        self.high_score = 0
        self.restart()

    def restart(self):
        self.score = 0
        self.lives = 3
        self.wave = 1
        self.game_over = False
        self.player = Player()
        self.high_score = getattr(self, "high_score", 0)
        self.starting_alien_count = ALIEN_ROWS * ALIEN_COLUMNS
        self._start_wave()

    def _start_wave(self):
        self.aliens = [
            Alien(
                ALIEN_START_X + column * (ALIEN_WIDTH + ALIEN_GAP_X),
                ALIEN_START_Y + row * ALIEN_GAP_Y,
                row,
            )
            for row in range(ALIEN_ROWS)
            for column in range(ALIEN_COLUMNS)
        ]
        self.player_shots = []
        self.alien_shots = []
        self.shields = [Shield(x) for x in (90, 285, 480, 675)]
        self.fleet_direction = 1
        self.fleet_step_timer = 0.0
        self.enemy_fire_timer = 0.9
        self.fire_cooldown = 0.0

    def update(self, delta_time, move_direction, firing):
        if self.game_over:
            return

        self.player.move(move_direction, delta_time)
        self.player.invulnerability = max(0.0, self.player.invulnerability - delta_time)
        self.fire_cooldown = max(0.0, self.fire_cooldown - delta_time)
        if firing and self.fire_cooldown == 0 and not self.player_shots:
            self.player_shots.append(Shot(
                self.player.rect.centerx,
                self.player.rect.top - 14,
                -580,
                CYAN,
            ))
            self.fire_cooldown = 0.18

        self._move_shots(delta_time)
        self._move_fleet(delta_time)
        self._fire_alien_shots(delta_time)
        self._check_collisions()

        if not self.aliens and not self.game_over:
            self.wave += 1
            self._start_wave()

    def _move_shots(self, delta_time):
        for shot in self.player_shots[:]:
            shot.update(delta_time)
            if shot.rect.bottom < 0:
                self.player_shots.remove(shot)
                continue
            if self._hit_shield(shot):
                self.player_shots.remove(shot)
                continue
            for alien in self.aliens[:]:
                if shot.rect.colliderect(alien.rect):
                    self.aliens.remove(alien)
                    self.player_shots.remove(shot)
                    self.score += alien.points
                    self.high_score = max(self.high_score, self.score)
                    break

        for shot in self.alien_shots[:]:
            shot.update(delta_time)
            if shot.rect.top > SCREEN_HEIGHT:
                self.alien_shots.remove(shot)
            elif self._hit_shield(shot):
                self.alien_shots.remove(shot)

    def _hit_shield(self, shot):
        for shield in self.shields:
            for block in shield.blocks:
                if shot.rect.colliderect(block):
                    shield.blocks.remove(block)
                    return True
        return False

    def _move_fleet(self, delta_time):
        if not self.aliens:
            return
        remaining = len(self.aliens) / self.starting_alien_count
        interval = max(0.085, 0.76 - 0.62 * (1 - remaining))
        interval /= 1 + (self.wave - 1) * 0.12
        self.fleet_step_timer += delta_time
        while self.fleet_step_timer >= interval:
            self.fleet_step_timer -= interval
            step = 9 * self.fleet_direction
            left_edge = min(alien.rect.left for alien in self.aliens)
            right_edge = max(alien.rect.right for alien in self.aliens)
            if left_edge + step < 16 or right_edge + step > SCREEN_WIDTH - 16:
                self.fleet_direction *= -1
                for alien in self.aliens:
                    alien.y += 18
            else:
                for alien in self.aliens:
                    alien.x += step

            if max(alien.rect.bottom for alien in self.aliens) >= INVASION_LINE:
                self.game_over = True
                self.lives = 0
                return

    def _fire_alien_shots(self, delta_time):
        if not self.aliens:
            return
        self.enemy_fire_timer -= delta_time
        if self.enemy_fire_timer > 0:
            return

        lowest_by_column = {}
        for alien in self.aliens:
            current = lowest_by_column.get(alien.x)
            if current is None or alien.y > current.y:
                lowest_by_column[alien.x] = alien
        shooter = random.choice(list(lowest_by_column.values()))
        self.alien_shots.append(Shot(
            shooter.rect.centerx,
            shooter.rect.bottom,
            220 + self.wave * 18,
            ORANGE,
            zigzag=random.random() < 0.35,
        ))
        self.enemy_fire_timer = max(0.34, 1.3 - self.wave * 0.06)

    def _check_collisions(self):
        if self.player.invulnerability <= 0:
            for shot in self.alien_shots[:]:
                if shot.rect.colliderect(self.player.rect):
                    self.alien_shots.remove(shot)
                    self.lives -= 1
                    self.player.x = (SCREEN_WIDTH - self.player.width) / 2
                    self.player.invulnerability = 1.5
                    self.alien_shots.clear()
                    if self.lives <= 0:
                        self.game_over = True
                    break


def draw_button(surface, rect, label, font, active=False):
    color = BUTTON_ACTIVE if active else BUTTON_BG
    pygame.draw.rect(surface, color, rect, border_radius=6)
    pygame.draw.rect(surface, WHITE, rect, width=1, border_radius=6)
    label_surface = font.render(label, True, WHITE)
    surface.blit(label_surface, label_surface.get_rect(center=rect.center))


def draw_game(surface, state, fonts, buttons, stars, mouse_pos, mouse_down, ticks):
    surface.fill(BLACK)
    for x, y, radius, phase in stars:
        brightness = 100 + (ticks // 180 + phase) % 100
        pygame.draw.circle(surface, (brightness, brightness, min(255, brightness + 30)), (x, y), radius)

    pygame.draw.line(surface, (48, 62, 82), (0, 58), (SCREEN_WIDTH, 58), 1)
    font, button_font = fonts
    score_label = font.render(f"SCORE {state.score:05}", True, WHITE)
    best_label = font.render(f"BEST {state.high_score:05}", True, CYAN)
    status_label = button_font.render(f"LIVES {state.lives}   WAVE {state.wave}", True, GREEN)
    surface.blit(score_label, (14, 16))
    surface.blit(best_label, (185, 16))
    surface.blit(status_label, (340, 16))

    left_button, fire_button, right_button, restart_button = buttons
    draw_button(surface, left_button, "LEFT", button_font, mouse_down and left_button.collidepoint(mouse_pos))
    draw_button(surface, fire_button, "FIRE", button_font, mouse_down and fire_button.collidepoint(mouse_pos))
    draw_button(surface, right_button, "RIGHT", button_font, mouse_down and right_button.collidepoint(mouse_pos))

    for shield in state.shields:
        shield.draw(surface)
    for alien in state.aliens:
        alien.draw(surface, ticks)
    for shot in state.player_shots + state.alien_shots:
        shot.draw(surface)
    state.player.draw(surface, ticks)

    pygame.draw.line(surface, (65, 77, 102), (0, SCREEN_HEIGHT - 22), (SCREEN_WIDTH, SCREEN_HEIGHT - 22), 1)

    if state.game_over:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 165))
        surface.blit(overlay, (0, 0))
        title = font.render("GAME OVER", True, RED)
        result = font.render(f"FINAL SCORE  {state.score:05}", True, WHITE)
        prompt = font.render("Press R or click below to restart", True, WHITE)
        surface.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 260)))
        surface.blit(result, result.get_rect(center=(SCREEN_WIDTH // 2, 303)))
        surface.blit(prompt, prompt.get_rect(center=(SCREEN_WIDTH // 2, 346)))
        draw_button(surface, restart_button, "PLAY AGAIN", button_font)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Space Invaders")
    clock = pygame.time.Clock()
    state = GameState()
    font = pygame.font.SysFont("Arial", 22, bold=True)
    button_font = pygame.font.SysFont("Arial", 18, bold=True)
    left_button = pygame.Rect(478, 10, 92, 38)
    fire_button = pygame.Rect(582, 10, 82, 38)
    right_button = pygame.Rect(676, 10, 108, 38)
    restart_button = pygame.Rect(315, 375, 170, 46)
    buttons = (left_button, fire_button, right_button, restart_button)
    rng = random.Random(12)
    stars = [
        (rng.randrange(SCREEN_WIDTH), rng.randrange(SCREEN_HEIGHT), rng.choice((1, 1, 2)), rng.randrange(100))
        for _ in range(75)
    ]

    running = True
    while running:
        delta_time = min(clock.tick(FPS) / 1000, 0.05)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and state.game_over and event.key == pygame.K_r:
                state.restart()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if state.game_over and restart_button.collidepoint(event.pos):
                    state.restart()

        keys = pygame.key.get_pressed()
        mouse_down = pygame.mouse.get_pressed()[0]
        mouse_pos = pygame.mouse.get_pos()
        move_left = keys[pygame.K_LEFT] or keys[pygame.K_a] or (mouse_down and left_button.collidepoint(mouse_pos))
        move_right = keys[pygame.K_RIGHT] or keys[pygame.K_d] or (mouse_down and right_button.collidepoint(mouse_pos))
        direction = int(bool(move_right)) - int(bool(move_left))
        firing = keys[pygame.K_SPACE] or (mouse_down and fire_button.collidepoint(mouse_pos))
        state.update(delta_time, direction, bool(firing))

        draw_game(
            screen,
            state,
            (font, button_font),
            buttons,
            stars,
            mouse_pos,
            mouse_down,
            pygame.time.get_ticks(),
        )
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
