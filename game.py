from array import array
import math
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
MUSIC_SAMPLE_RATE = 22050
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

CATALOG_TABS = ("Jets", "Blasters", "Fire Rate", "Bullet Amount", "Achievements")
CATALOG_TAB_LABELS = {
    "Jets": "JETS",
    "Blasters": "BLASTERS",
    "Fire Rate": "FIRE RATE",
    "Bullet Amount": "BULLET AMOUNT",
    "Achievements": "ACHIEVEMENTS",
}
UPGRADE_CATALOGS = {
    "Jets": (
        {"id": "scout", "name": "Scout", "score": 0, "style": 0, "color": GREEN},
        {"id": "falcon", "name": "Falcon", "score": 500, "style": 1, "color": CYAN},
        {"id": "viper", "name": "Viper", "score": 1500, "style": 2, "color": ORANGE},
        {"id": "comet", "name": "Comet", "score": 3000, "style": 3, "color": (255, 115, 220)},
        {"id": "starfire", "name": "Starfire", "score": 6000, "style": 4, "color": (100, 225, 200)},
        {"id": "phantom", "name": "Phantom", "score": 12000, "style": 5, "color": (205, 165, 255)},
    ),
    "Blasters": (
        {"id": "pulse", "name": "Pulse", "score": 0, "color": CYAN},
        {"id": "ember", "name": "Ember", "score": 400, "color": ORANGE},
        {"id": "ion", "name": "Ion", "score": 1000, "color": (150, 135, 255)},
        {"id": "prism", "name": "Prism", "score": 2200, "color": (255, 105, 220)},
        {"id": "nova", "name": "Nova", "score": 6000, "color": (105, 255, 205)},
        {"id": "quasar", "name": "Quasar", "score": 12000, "color": (255, 235, 130)},
    ),
    "Fire Rate": (
        {"id": "standard", "name": "Standard", "score": 0, "cooldown": 0.18},
        {"id": "rapid", "name": "Rapid", "score": 750, "cooldown": 0.14},
        {"id": "turbo", "name": "Turbo", "score": 1800, "cooldown": 0.10},
        {"id": "overdrive", "name": "Overdrive", "score": 3500, "cooldown": 0.07},
        {"id": "hyperion", "name": "Hyperion", "score": 6000, "cooldown": 0.055},
        {"id": "singularity", "name": "Singularity", "score": 12000, "cooldown": 0.04},
    ),
    "Bullet Amount": (
        {"id": "single", "name": "Single Shot", "score": 0, "amount": 1},
        {"id": "twin", "name": "Twin Shot", "score": 1200, "amount": 2},
        {"id": "triple", "name": "Triple Shot", "score": 2500, "amount": 3},
        {"id": "fan", "name": "Fan Volley", "score": 4000, "amount": 5},
        {"id": "thunder", "name": "Thunder Volley", "score": 6000, "amount": 7},
        {"id": "starfall", "name": "Starfall Volley", "score": 12000, "amount": 9},
    ),
}
ACHIEVEMENTS = (
    {"name": "First Contact", "score": 250, "reward": "+1 extra life", "extra_lives": 1},
    {"name": "Squadron Pilot", "score": 500, "reward": "Repair all shields", "repair_shields": True},
    {"name": "The Wide Receiver", "score": 1500, "reward": "+1 extra life", "extra_lives": 1},
    {"name": "Ace of the Fleet", "score": 3000, "reward": "+1 life and shield repair", "extra_lives": 1, "repair_shields": True},
    {"name": "Alien Nemesis", "score": 5000, "reward": "+2 extra lives", "extra_lives": 2},
    {"name": "Shield Guardian", "score": 6500, "reward": "Repair all shields", "repair_shields": True},
    {"name": "Vanguard Ace", "score": 9000, "reward": "+2 extra lives", "extra_lives": 2},
    {"name": "Star Marshal", "score": 12500, "reward": "+1 life and shield repair", "extra_lives": 1, "repair_shields": True},
    {"name": "Galactic Guardian", "score": 18000, "reward": "+3 extra lives", "extra_lives": 3},
)
MUSIC_TRACKS = (
    {
        "name": "Vector Assault",
        "melody": (
            523.25, 0, 659.25, 783.99, 698.46, 659.25, 587.33, 0,
            466.16, 587.33, 698.46, 783.99, 932.33, 783.99, 698.46, 0,
            523.25, 659.25, 783.99, 1046.50, 932.33, 783.99, 659.25, 587.33,
            466.16, 523.25, 587.33, 698.46, 659.25, 587.33, 523.25, 0,
        ),
        "bass": (130.81, 155.56, 174.61, 146.83),
    },
    {
        "name": "Star Patrol",
        "melody": (
            392.00, 523.25, 659.25, 0, 523.25, 659.25, 783.99, 0,
            698.46, 659.25, 523.25, 392.00, 440.00, 523.25, 659.25, 0,
            349.23, 440.00, 523.25, 698.46, 659.25, 523.25, 440.00, 0,
            392.00, 523.25, 587.33, 659.25, 523.25, 440.00, 392.00, 0,
        ),
        "bass": (98.00, 130.81, 146.83, 116.54),
    },
    {
        "name": "Nebula Run",
        "melody": (
            659.25, 0, 783.99, 987.77, 880.00, 0, 783.99, 659.25,
            587.33, 698.46, 880.00, 0, 1046.50, 880.00, 783.99, 0,
            659.25, 783.99, 987.77, 1174.66, 1046.50, 987.77, 880.00, 0,
            587.33, 659.25, 783.99, 880.00, 783.99, 659.25, 587.33, 0,
        ),
        "bass": (164.81, 196.00, 146.83, 174.61),
    },
)


def create_music_loop(track_index=0):
    track = MUSIC_TRACKS[track_index]
    melody = track["melody"]
    bass_line = track["bass"]
    note_duration = 0.16
    samples_per_note = int(MUSIC_SAMPLE_RATE * note_duration)
    audio_samples = array("h")

    for note_index, frequency in enumerate(melody):
        bass_frequency = bass_line[(note_index // 4) % len(bass_line)]
        for sample_index in range(samples_per_note):
            time = sample_index / MUSIC_SAMPLE_RATE
            envelope = min(
                1.0,
                sample_index / (MUSIC_SAMPLE_RATE * 0.008),
                (samples_per_note - sample_index) / (MUSIC_SAMPLE_RATE * 0.018),
            )
            lead_phase = (time * frequency) % 1 if frequency else 1
            bass_phase = (time * bass_frequency) % 1
            lead = 1 if frequency and lead_phase < 0.5 else -1 if frequency else 0
            bass = 1 if bass_phase < 0.5 else -1
            sample = int((lead * 0.13 + bass * 0.045) * envelope * 32767)
            audio_samples.append(max(-32768, min(32767, sample)))

    return pygame.mixer.Sound(buffer=audio_samples.tobytes())


def create_effect_sequence(notes, note_duration=0.12, waveform="square"):
    samples_per_note = int(MUSIC_SAMPLE_RATE * note_duration)
    audio_samples = array("h")
    for frequency in notes:
        for sample_index in range(samples_per_note):
            time = sample_index / MUSIC_SAMPLE_RATE
            phase = (time * frequency) % 1
            if waveform == "sine":
                value = math.sin(2 * math.pi * phase)
            elif waveform == "triangle":
                value = 1 - 4 * abs(phase - 0.5)
            else:
                value = 1 if phase < 0.5 else -1
            envelope = min(
                1.0,
                sample_index / (MUSIC_SAMPLE_RATE * 0.006),
                (samples_per_note - sample_index) / (MUSIC_SAMPLE_RATE * 0.025),
            )
            audio_samples.append(int(value * envelope * 22000))
    return pygame.mixer.Sound(buffer=audio_samples.tobytes())


def create_laser_sound():
    duration = 0.13
    sample_count = int(MUSIC_SAMPLE_RATE * duration)
    audio_samples = array("h")
    phase = 0.0
    for sample_index in range(sample_count):
        progress = sample_index / sample_count
        frequency = 1450 - progress * 980
        phase = (phase + frequency / MUSIC_SAMPLE_RATE) % 1
        envelope = min(1.0, sample_index / 70, (sample_count - sample_index) / 450)
        value = 1 if phase < 0.5 else -1
        audio_samples.append(int(value * envelope * 18000))
    return pygame.mixer.Sound(buffer=audio_samples.tobytes())


def create_achievement_sound():
    notes = ((659.25, 0.14), (880.0, 0.14), (1108.73, 0.18), (1318.51, 0.52))
    audio_samples = array("h")
    for frequency, duration in notes:
        sample_count = int(MUSIC_SAMPLE_RATE * duration)
        for sample_index in range(sample_count):
            time = sample_index / MUSIC_SAMPLE_RATE
            envelope = min(1.0, sample_index / 120) * math.exp(-time * 2.8)
            chord = (
                math.sin(2 * math.pi * frequency * time)
                + 0.38 * math.sin(2 * math.pi * frequency * 2 * time)
                + 0.16 * math.sin(2 * math.pi * frequency * 3 * time)
            )
            audio_samples.append(int(chord * envelope * 7800))
    return pygame.mixer.Sound(buffer=audio_samples.tobytes())


class AudioManager:
    def __init__(self):
        self.music_sounds = [create_music_loop(index) for index in range(len(MUSIC_TRACKS))]
        self.effects = {
            "laser": create_laser_sound(),
            "achievement": create_achievement_sound(),
            "game_over": create_effect_sequence((659.25, 523.25, 392.0, 261.63), 0.23, "triangle"),
            "count_3": create_effect_sequence((523.25,), 0.16),
            "count_2": create_effect_sequence((659.25,), 0.16),
            "count_1": create_effect_sequence((783.99,), 0.16),
            "count_go": create_effect_sequence((1046.5, 1318.51), 0.14),
        }
        self.music_channel = None
        self.preview_channel = None
        self.effect_channels = []
        self.track_index = 0
        self.master_volume = 0.72
        self.music_volume = 0.5
        self.music_enabled = True
        self.music_active = True
        self._start_music()

    def _start_music(self):
        if not self.music_enabled:
            return
        self.music_channel = self.music_sounds[self.track_index].play(loops=-1)
        self._sync_music_channel()

    def preview_track(self, track_index):
        self.stop_preview()
        if not self.music_enabled:
            return
        self.preview_channel = self.music_sounds[track_index].play()
        if self.preview_channel is not None:
            self.preview_channel.set_volume(self.master_volume * self.music_volume)

    def stop_preview(self):
        if self.preview_channel is not None:
            self.preview_channel.stop()
            self.preview_channel = None

    def _sync_music_channel(self):
        if self.music_channel is None:
            return
        self.music_channel.set_volume(self.master_volume * self.music_volume)
        if self.music_active and self.music_enabled:
            self.music_channel.unpause()
        else:
            self.music_channel.pause()

    def sync_settings(self, settings, should_play_music):
        new_track = settings["track"]
        track_changed = new_track != self.track_index
        self.track_index = new_track
        self.master_volume = settings["master_volume"]
        self.music_volume = settings["music_volume"]
        self.music_enabled = settings["music_enabled"]
        self.music_active = should_play_music

        if (track_changed or not self.music_enabled) and self.music_channel is not None:
            self.music_channel.stop()
            self.music_channel = None
        if self.music_enabled and self.music_channel is None:
            self._start_music()
        self._sync_music_channel()

        if not self.music_enabled:
            self.stop_preview()
        elif self.preview_channel is not None:
            if self.preview_channel.get_busy():
                self.preview_channel.set_volume(self.master_volume * self.music_volume)
            else:
                self.preview_channel = None

        active_channels = []
        for channel, effect_volume in self.effect_channels:
            if channel.get_busy():
                channel.set_volume(self.master_volume * effect_volume)
                active_channels.append((channel, effect_volume))
        self.effect_channels = active_channels

    def play_effect(self, name, volume=0.45):
        sound = self.effects.get(name)
        if sound is None:
            return
        channel = sound.play()
        if channel is not None:
            channel.set_volume(self.master_volume * volume)
            self.effect_channels.append((channel, volume))


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

    def draw(self, surface, ticks, jet=None):
        if self.invulnerability > 0 and ticks // 100 % 2:
            return
        x = round(self.x)
        y = self.y
        style = jet["style"] if jet else 0
        color = jet["color"] if jet else GREEN
        shapes = (
            ((24, 0), (30, 13), (47, 25), (47, 31), (1, 31), (1, 25), (18, 13)),
            ((24, 0), (31, 12), (47, 22), (43, 31), (5, 31), (1, 22), (17, 12)),
            ((24, 0), (29, 12), (47, 17), (39, 31), (9, 31), (1, 17), (19, 12)),
            ((24, 0), (32, 14), (47, 28), (39, 28), (33, 31), (15, 31), (9, 28), (1, 28), (16, 14)),
            ((24, 0), (28, 12), (45, 18), (47, 29), (31, 27), (24, 31), (17, 27), (1, 29), (3, 18), (20, 12)),
            ((24, 0), (34, 15), (47, 20), (36, 22), (43, 31), (27, 28), (24, 31), (21, 28), (5, 31), (12, 22), (1, 20), (14, 15)),
        )
        pygame.draw.polygon(surface, color, tuple((x + px, y + py) for px, py in shapes[style]))
        pygame.draw.rect(surface, WHITE, (x + 22, y + 12, 4, 8))
        pygame.draw.rect(surface, color, (x + 22, y + 25, 4, 6))


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
        self.achievements = set()
        self.equipped = {name: items[0]["id"] for name, items in UPGRADE_CATALOGS.items()}
        self.catalog_tab = CATALOG_TABS[0]
        self.achievement_popup = None
        self.achievement_popup_timer = 0.0
        self.exit_confirmation = False
        self.exit_was_paused = False
        self.audio_settings = {
            "track": 0,
            "master_volume": 0.72,
            "music_volume": 0.5,
            "music_enabled": True,
        }
        self.restart()

    def restart(self):
        self.score = 0
        self.lives = 3
        self.wave = 1
        self.game_over = False
        self.paused = False
        self.catalog_open = False
        self.settings_open = False
        self.settings_dropdown_open = False
        self.preview_track = None
        self.resume_countdown = 0.0
        self.shots_fired = 0
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
        if self.game_over or self.catalog_open or self.settings_open:
            return
        if self.resume_countdown > 0:
            self.resume_countdown = max(0.0, self.resume_countdown - delta_time)
            if self.resume_countdown == 0:
                self.paused = False
            return
        if self.paused:
            return
        self.achievement_popup_timer = max(0.0, self.achievement_popup_timer - delta_time)
        if self.achievement_popup_timer == 0:
            self.achievement_popup = None

        self.player.move(move_direction, delta_time)
        self.player.invulnerability = max(0.0, self.player.invulnerability - delta_time)
        self.fire_cooldown = max(0.0, self.fire_cooldown - delta_time)
        if firing and self.fire_cooldown == 0:
            self.shots_fired += 1
            bullet_count = self.equipped_item("Bullet Amount")["amount"]
            blaster_color = self.equipped_item("Blasters")["color"]
            for bullet_index in range(bullet_count):
                offset = (bullet_index - (bullet_count - 1) / 2) * 10
                self.player_shots.append(Shot(
                    self.player.rect.centerx + offset,
                    self.player.rect.top - 14,
                    -580,
                    blaster_color,
                ))
            self.fire_cooldown = self.equipped_item("Fire Rate")["cooldown"]

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
                    self._check_achievements()
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

    def equipped_item(self, category):
        item_id = self.equipped[category]
        return next(item for item in UPGRADE_CATALOGS[category] if item["id"] == item_id)

    def item_is_unlocked(self, category, item):
        return self.high_score >= item["score"]

    def equip_item(self, category, item_id):
        item = next((item for item in UPGRADE_CATALOGS[category] if item["id"] == item_id), None)
        if item is not None and self.item_is_unlocked(category, item):
            self.equipped[category] = item_id
            return True
        return False

    def open_catalog(self):
        if self.game_over or self.settings_open or self.resume_countdown > 0:
            return False
        self.catalog_open = True
        self.paused = True
        return True

    def close_catalog(self):
        if self.catalog_open:
            self.catalog_open = False
            self.paused = True
            self.resume_countdown = 3.0

    def open_settings(self):
        if self.game_over or self.catalog_open or self.resume_countdown > 0:
            return False
        self.settings_open = True
        self.settings_dropdown_open = False
        self.preview_track = None
        self.paused = True
        return True

    def close_settings(self):
        if self.settings_open:
            self.settings_open = False
            self.settings_dropdown_open = False
            self.preview_track = None
            self.paused = True
            self.resume_countdown = 3.0

    def _check_achievements(self):
        for achievement in ACHIEVEMENTS:
            name = achievement["name"]
            if self.high_score >= achievement["score"] and name not in self.achievements:
                self.achievements.add(name)
                self.achievement_popup = name
                self.achievement_popup_timer = 4.0
                self.lives += achievement.get("extra_lives", 0)
                if achievement.get("repair_shields"):
                    self.shields = [Shield(x) for x in (90, 285, 480, 675)]


def draw_button(surface, rect, label, font, active=False):
    color = BUTTON_ACTIVE if active else BUTTON_BG
    pygame.draw.rect(surface, color, rect, border_radius=6)
    pygame.draw.rect(surface, WHITE, rect, width=1, border_radius=6)
    label_surface = font.render(label, True, WHITE)
    surface.blit(label_surface, label_surface.get_rect(center=rect.center))


def draw_pause_button(surface, rect, paused, icon_font, active=False):
    color = BUTTON_ACTIVE if active else BUTTON_BG
    pygame.draw.rect(surface, color, rect, border_radius=6)
    pygame.draw.rect(surface, WHITE, rect, width=1, border_radius=6)
    center_x, center_y = rect.center
    if paused:
        pygame.draw.polygon(surface, WHITE, (
            (center_x - 5, center_y - 9),
            (center_x + 9, center_y),
            (center_x - 5, center_y + 9),
        ))
    else:
        icon = icon_font.render("\u23f8", True, WHITE)
        surface.blit(icon, icon.get_rect(center=rect.center))


def create_catalog_layout():
    tabs = {
        name: pygame.Rect(34 + index * 146, 126, 140, 36)
        for index, name in enumerate(CATALOG_TABS)
    }
    cards = {}
    for category, items in UPGRADE_CATALOGS.items():
        cards[category] = [
            pygame.Rect(40 + (index % 2) * 365, 176 + (index // 2) * 80, 350, 68)
            for index in range(len(items))
        ]
    cards["Achievements"] = [
        pygame.Rect(40 + (index % 2) * 365, 176 + (index // 2) * 76, 350, 60)
        for index in range(len(ACHIEVEMENTS))
    ]
    return {
        "panel": pygame.Rect(20, 68, 760, 520),
        "close": pygame.Rect(736, 80, 34, 34),
        "tabs": tabs,
        "cards": cards,
    }


def create_settings_layout():
    return {
        "panel": pygame.Rect(100, 80, 600, 440),
        "close": pygame.Rect(652, 94, 34, 34),
        "track": pygame.Rect(132, 168, 380, 42),
        "save_track": pygame.Rect(522, 168, 146, 42),
        "track_options": [
            pygame.Rect(132, 210 + index * 34, 536, 34)
            for index in range(len(MUSIC_TRACKS))
        ],
        "master_slider": pygame.Rect(144, 347, 480, 8),
        "music_slider": pygame.Rect(144, 414, 480, 8),
        "music_toggle": pygame.Rect(590, 458, 78, 34),
    }


def create_exit_confirmation_layout():
    return {
        "panel": pygame.Rect(125, 185, 550, 230),
        "yes": pygame.Rect(270, 335, 110, 44),
        "no": pygame.Rect(420, 335, 110, 44),
    }


def draw_volume_slider(surface, rect, value):
    center_y = rect.centery
    pygame.draw.line(surface, (76, 93, 115), rect.midleft, rect.midright, 6)
    active_width = int(rect.width * value)
    if active_width:
        pygame.draw.line(surface, CYAN, rect.midleft, (rect.left + active_width, center_y), 6)
    knob_x = rect.left + active_width
    pygame.draw.circle(surface, WHITE, (knob_x, center_y), 10)
    pygame.draw.circle(surface, CYAN, (knob_x, center_y), 5)


def draw_settings(surface, state, fonts, layout):
    font, button_font, catalog_font = fonts
    dim = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    dim.fill((0, 0, 0, 205))
    surface.blit(dim, (0, 0))
    pygame.draw.rect(surface, (12, 21, 36), layout["panel"], border_radius=8)
    pygame.draw.rect(surface, (89, 125, 157), layout["panel"], width=1, border_radius=8)
    title = font.render("GAME SETTINGS", True, WHITE)
    surface.blit(title, (132, 99))
    draw_button(surface, layout["close"], "X", button_font)

    track_label = catalog_font.render("MUSIC TRACK", True, CYAN)
    surface.blit(track_label, (138, 145))
    selected_track = state.preview_track
    if selected_track is None:
        selected_track = state.audio_settings["track"]
    track_name = MUSIC_TRACKS[selected_track]["name"]
    track_label = f"PREVIEW: {track_name}" if state.preview_track is not None else track_name
    draw_button(surface, layout["track"], track_label, button_font)
    save_label = "SAVE" if state.preview_track is not None else "SAVED"
    draw_button(
        surface,
        layout["save_track"],
        save_label,
        button_font,
        state.preview_track is not None,
    )
    arrow_x = layout["track"].right - 22
    pygame.draw.polygon(surface, WHITE, (
        (arrow_x - 6, layout["track"].centery - 3),
        (arrow_x + 6, layout["track"].centery - 3),
        (arrow_x, layout["track"].centery + 4),
    ))

    master_percent = round(state.audio_settings["master_volume"] * 100)
    master_label = catalog_font.render(f"MAIN VOLUME  {master_percent}%", True, WHITE)
    surface.blit(master_label, (138, 312))
    draw_volume_slider(surface, layout["master_slider"], state.audio_settings["master_volume"])

    music_percent = round(state.audio_settings["music_volume"] * 100)
    music_label = catalog_font.render(f"MUSIC VOLUME  {music_percent}%", True, WHITE)
    surface.blit(music_label, (138, 379))
    draw_volume_slider(surface, layout["music_slider"], state.audio_settings["music_volume"])

    music_text = catalog_font.render("MUSIC", True, WHITE)
    surface.blit(music_text, (138, 464))
    toggle_color = BUTTON_ACTIVE if state.audio_settings["music_enabled"] else RED
    pygame.draw.rect(surface, toggle_color, layout["music_toggle"], border_radius=17)
    knob_x = layout["music_toggle"].right - 17 if state.audio_settings["music_enabled"] else layout["music_toggle"].left + 17
    pygame.draw.circle(surface, WHITE, (knob_x, layout["music_toggle"].centery), 12)
    toggle_label = catalog_font.render("ON" if state.audio_settings["music_enabled"] else "OFF", True, WHITE)
    label_x = layout["music_toggle"].left + 7 if state.audio_settings["music_enabled"] else layout["music_toggle"].left + 38
    surface.blit(toggle_label, (label_x, layout["music_toggle"].y + 10))

    if state.settings_dropdown_open:
        for index, rect in enumerate(layout["track_options"]):
            selected_track = state.preview_track
            if selected_track is None:
                selected_track = state.audio_settings["track"]
            selected = index == selected_track
            draw_button(surface, rect, MUSIC_TRACKS[index]["name"], catalog_font, selected)


def draw_catalog(surface, state, fonts, layout):
    font, button_font, catalog_font, tab_font = fonts
    dim = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    dim.fill((0, 0, 0, 205))
    surface.blit(dim, (0, 0))
    pygame.draw.rect(surface, (12, 21, 36), layout["panel"], border_radius=8)
    pygame.draw.rect(surface, (89, 125, 157), layout["panel"], width=1, border_radius=8)

    title = font.render("HANGAR CATALOG", True, WHITE)
    best = catalog_font.render(f"BEST SCORE  {state.high_score:,}", True, CYAN)
    surface.blit(title, (40, 82))
    surface.blit(best, (490, 91))
    draw_button(surface, layout["close"], "X", button_font)

    for tab_name, rect in layout["tabs"].items():
        draw_button(surface, rect, CATALOG_TAB_LABELS[tab_name], tab_font, state.catalog_tab == tab_name)

    if state.catalog_tab == "Achievements":
        items = ACHIEVEMENTS
    else:
        items = UPGRADE_CATALOGS[state.catalog_tab]

    for index, item in enumerate(items):
        rect = layout["cards"][state.catalog_tab][index]
        if state.catalog_tab == "Achievements":
            unlocked = item["name"] in state.achievements
            equipped = False
        else:
            unlocked = state.item_is_unlocked(state.catalog_tab, item)
            equipped = state.equipped[state.catalog_tab] == item["id"]

        if equipped or (state.catalog_tab == "Achievements" and unlocked):
            edge_color = GREEN
        elif unlocked:
            edge_color = CYAN
        else:
            edge_color = (73, 88, 108)
        fill_color = (22, 37, 54) if unlocked else (18, 25, 37)
        pygame.draw.rect(surface, fill_color, rect, border_radius=6)
        pygame.draw.rect(surface, edge_color, rect, width=1, border_radius=6)

        item_name = catalog_font.render(item["name"], True, WHITE if unlocked else (147, 158, 172))
        if state.catalog_tab == "Achievements":
            detail_text = f"Reach {item['score']:,} pts | {item['reward']}"
            status_text = "EARNED" if unlocked else "LOCKED"
        else:
            if item["score"] == 0:
                detail_text = "Available from the start"
            elif state.catalog_tab == "Fire Rate":
                detail_text = f"Fires every {item['cooldown']:.2f} sec"
            elif state.catalog_tab == "Bullet Amount":
                detail_text = f"{item['amount']} shots per volley"
            else:
                detail_text = f"Unlock at {item['score']:,} pts"
            status_text = "EQUIPPED" if equipped else "EQUIP" if unlocked else "LOCKED"

        detail = catalog_font.render(detail_text, True, (164, 182, 199))
        status = catalog_font.render(status_text, True, edge_color)
        if state.catalog_tab == "Achievements":
            surface.blit(item_name, (rect.x + 12, rect.y + 6))
            surface.blit(detail, (rect.x + 12, rect.y + 35))
            surface.blit(status, status.get_rect(midright=(rect.right - 12, rect.y + 18)))
        else:
            surface.blit(item_name, (rect.x + 12, rect.y + 9))
            surface.blit(detail, (rect.x + 12, rect.y + 38))
            surface.blit(status, status.get_rect(midright=(rect.right - 12, rect.centery)))

    footer = catalog_font.render("Unlocked upgrades are permanent for this session. Click an unlocked item to equip it.", True, (164, 182, 199))
    footer_y = 566 if state.catalog_tab == "Achievements" else 528
    surface.blit(footer, footer.get_rect(center=(SCREEN_WIDTH // 2, footer_y)))


def draw_game(surface, state, fonts, buttons, catalog_layout, settings_layout, stars, mouse_pos, mouse_down, ticks):
    surface.fill(BLACK)
    for x, y, radius, phase in stars:
        brightness = 100 + (ticks // 180 + phase) % 100
        pygame.draw.circle(surface, (brightness, brightness, min(255, brightness + 30)), (x, y), radius)

    pygame.draw.line(surface, (48, 62, 82), (0, 58), (SCREEN_WIDTH, 58), 1)
    font, button_font, pause_icon_font, catalog_font, tab_font = fonts
    score_label = font.render(f"SCORE {state.score:05}", True, WHITE)
    best_label = font.render(f"BEST {state.high_score:05}", True, CYAN)
    status_label = button_font.render(f"LIVES {state.lives}   WAVE {state.wave}", True, GREEN)
    surface.blit(score_label, (14, 16))
    surface.blit(best_label, (145, 16))
    surface.blit(status_label, (250, 16))

    left_button, fire_button, right_button, restart_button, pause_button, catalog_button, settings_button = buttons
    draw_button(surface, left_button, "LEFT", button_font, mouse_down and left_button.collidepoint(mouse_pos))
    draw_button(surface, fire_button, "FIRE", button_font, mouse_down and fire_button.collidepoint(mouse_pos))
    draw_button(surface, right_button, "RIGHT", button_font, mouse_down and right_button.collidepoint(mouse_pos))
    draw_button(surface, catalog_button, "CATALOG", catalog_font, state.catalog_open)
    pygame.draw.rect(surface, BUTTON_BG, settings_button, border_radius=6)
    pygame.draw.rect(surface, WHITE, settings_button, width=1, border_radius=6)
    settings_icon = pause_icon_font.render("\u2699", True, WHITE)
    surface.blit(settings_icon, settings_icon.get_rect(center=settings_button.center))
    draw_pause_button(
        surface,
        pause_button,
        state.paused,
        pause_icon_font,
        mouse_down and pause_button.collidepoint(mouse_pos),
    )

    for shield in state.shields:
        shield.draw(surface)
    for alien in state.aliens:
        alien.draw(surface, ticks)
    for shot in state.player_shots + state.alien_shots:
        shot.draw(surface)
    state.player.draw(surface, ticks, state.equipped_item("Jets"))

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
    elif state.catalog_open:
        draw_catalog(surface, state, (font, button_font, catalog_font, tab_font), catalog_layout)
    elif state.settings_open:
        draw_settings(surface, state, (font, button_font, catalog_font), settings_layout)
    elif state.resume_countdown > 0:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 165))
        surface.blit(overlay, (0, 0))
        title = font.render("GET READY", True, YELLOW)
        countdown = font.render(str(max(1, int(state.resume_countdown + 0.999))), True, WHITE)
        surface.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 270)))
        surface.blit(countdown, countdown.get_rect(center=(SCREEN_WIDTH // 2, 320)))
    elif state.paused:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 165))
        surface.blit(overlay, (0, 0))
        title = font.render("PAUSED", True, YELLOW)
        prompt = font.render("Press P or click the play button to resume", True, WHITE)
        surface.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 275)))
        surface.blit(prompt, prompt.get_rect(center=(SCREEN_WIDTH // 2, 320)))

    if state.achievement_popup and not state.catalog_open and not state.game_over:
        popup_rect = pygame.Rect(220, 72, 360, 54)
        pygame.draw.rect(surface, (16, 36, 47), popup_rect, border_radius=6)
        pygame.draw.rect(surface, CYAN, popup_rect, width=1, border_radius=6)
        popup_title = catalog_font.render("ACHIEVEMENT UNLOCKED", True, CYAN)
        popup_name = catalog_font.render(state.achievement_popup, True, WHITE)
        surface.blit(popup_title, popup_title.get_rect(center=(popup_rect.centerx, popup_rect.y + 16)))
        surface.blit(popup_name, popup_name.get_rect(center=(popup_rect.centerx, popup_rect.y + 38)))

    if state.exit_confirmation:
        exit_layout = create_exit_confirmation_layout()
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))
        surface.blit(overlay, (0, 0))
        pygame.draw.rect(surface, (12, 21, 36), exit_layout["panel"], border_radius=8)
        pygame.draw.rect(surface, RED, exit_layout["panel"], width=1, border_radius=8)
        question = font.render("Are you sure you want to exit?", True, WHITE)
        warning_one = catalog_font.render("You'll lose all of your achievements", True, YELLOW)
        warning_two = catalog_font.render("and awards.", True, YELLOW)
        surface.blit(question, question.get_rect(center=(SCREEN_WIDTH // 2, 230)))
        surface.blit(warning_one, warning_one.get_rect(center=(SCREEN_WIDTH // 2, 276)))
        surface.blit(warning_two, warning_two.get_rect(center=(SCREEN_WIDTH // 2, 301)))
        draw_button(surface, exit_layout["yes"], "YES", button_font)
        draw_button(surface, exit_layout["no"], "NO", button_font, True)


def handle_catalog_click(state, position, layout):
    if layout["close"].collidepoint(position):
        state.close_catalog()
        return

    for tab_name, rect in layout["tabs"].items():
        if rect.collidepoint(position):
            state.catalog_tab = tab_name
            return

    if state.catalog_tab == "Achievements":
        return
    for item, rect in zip(UPGRADE_CATALOGS[state.catalog_tab], layout["cards"][state.catalog_tab]):
        if rect.collidepoint(position):
            state.equip_item(state.catalog_tab, item["id"])
            return


def set_audio_slider(settings, slider_name, rect, position_x):
    settings[slider_name] = max(0.0, min(1.0, (position_x - rect.left) / rect.width))


def handle_settings_click(state, position, layout):
    if layout["close"].collidepoint(position):
        state.close_settings()
        return "close", None

    if state.settings_dropdown_open:
        for index, rect in enumerate(layout["track_options"]):
            if rect.collidepoint(position):
                state.preview_track = index
                state.settings_dropdown_open = False
                return "preview", index
        state.settings_dropdown_open = False

    if layout["track"].collidepoint(position):
        state.settings_dropdown_open = True
    elif layout["save_track"].collidepoint(position) and state.preview_track is not None:
        state.audio_settings["track"] = state.preview_track
        state.preview_track = None
        return "save", state.audio_settings["track"]
    elif layout["music_toggle"].collidepoint(position):
        state.audio_settings["music_enabled"] = not state.audio_settings["music_enabled"]
    elif layout["master_slider"].inflate(0, 24).collidepoint(position):
        set_audio_slider(state.audio_settings, "master_volume", layout["master_slider"], position[0])
    elif layout["music_slider"].inflate(0, 24).collidepoint(position):
        set_audio_slider(state.audio_settings, "music_volume", layout["music_slider"], position[0])


def main():
    pygame.mixer.pre_init(frequency=MUSIC_SAMPLE_RATE, size=-16, channels=1, buffer=512)
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Space Invaders")
    clock = pygame.time.Clock()
    state = GameState()
    audio_manager = None
    if pygame.mixer.get_init() is not None:
        try:
            audio_manager = AudioManager()
        except pygame.error:
            audio_manager = None
    font = pygame.font.SysFont("Arial", 22, bold=True)
    button_font = pygame.font.SysFont("Arial", 18, bold=True)
    catalog_font = pygame.font.SysFont("Arial", 14, bold=True)
    tab_font = pygame.font.SysFont("Segoe UI Emoji", 14, bold=True)
    pause_icon_font = pygame.font.SysFont("Segoe UI Symbol", 28)
    left_button = pygame.Rect(540, 10, 66, 38)
    fire_button = pygame.Rect(612, 10, 56, 38)
    right_button = pygame.Rect(674, 10, 110, 38)
    restart_button = pygame.Rect(315, 375, 170, 46)
    pause_button = pygame.Rect(470, 10, 38, 38)
    catalog_button = pygame.Rect(394, 10, 70, 38)
    settings_button = pygame.Rect(502, 10, 34, 38)
    buttons = (left_button, fire_button, right_button, restart_button, pause_button, catalog_button, settings_button)
    catalog_layout = create_catalog_layout()
    settings_layout = create_settings_layout()
    exit_layout = create_exit_confirmation_layout()
    rng = random.Random(12)
    stars = [
        (rng.randrange(SCREEN_WIDTH), rng.randrange(SCREEN_HEIGHT), rng.choice((1, 1, 2)), rng.randrange(100))
        for _ in range(75)
    ]

    running = True
    countdown_mark = 0
    while running:
        delta_time = min(clock.tick(FPS) / 1000, 0.05)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if not state.exit_confirmation:
                    state.exit_was_paused = state.paused
                    state.paused = True
                state.exit_confirmation = True
            elif event.type == pygame.KEYDOWN:
                if state.exit_confirmation:
                    if event.key == pygame.K_y:
                        running = False
                    elif event.key in (pygame.K_n, pygame.K_ESCAPE):
                        state.exit_confirmation = False
                        state.paused = state.exit_was_paused
                elif state.settings_open and event.key in (pygame.K_ESCAPE, pygame.K_x):
                    state.close_settings()
                    if audio_manager is not None:
                        audio_manager.stop_preview()
                elif state.catalog_open and event.key in (pygame.K_ESCAPE, pygame.K_x):
                    state.close_catalog()
                elif state.game_over and event.key == pygame.K_r:
                    state.restart()
                elif not state.game_over and state.resume_countdown == 0:
                    if event.key == pygame.K_p and not state.catalog_open and not state.settings_open:
                        state.paused = not state.paused
                    elif event.key == pygame.K_c and not state.catalog_open and not state.settings_open:
                        state.open_catalog()
                    elif event.key == pygame.K_g and not state.catalog_open and not state.settings_open:
                        state.open_settings()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if state.exit_confirmation:
                    if exit_layout["yes"].collidepoint(event.pos):
                        running = False
                    elif exit_layout["no"].collidepoint(event.pos):
                        state.exit_confirmation = False
                        state.paused = state.exit_was_paused
                elif state.settings_open:
                    settings_action = handle_settings_click(state, event.pos, settings_layout)
                    if audio_manager is not None and settings_action is not None:
                        if settings_action[0] == "preview":
                            audio_manager.preview_track(settings_action[1])
                        elif settings_action[0] in ("close", "save"):
                            audio_manager.stop_preview()
                elif state.catalog_open:
                    handle_catalog_click(state, event.pos, catalog_layout)
                elif state.game_over and restart_button.collidepoint(event.pos):
                    state.restart()
                elif not state.game_over and state.resume_countdown == 0:
                    if catalog_button.collidepoint(event.pos):
                        state.open_catalog()
                    elif pause_button.collidepoint(event.pos):
                        state.paused = not state.paused
                    elif settings_button.collidepoint(event.pos):
                        state.open_settings()

        if not running:
            break

        if state.settings_open and pygame.mouse.get_pressed()[0]:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if settings_layout["master_slider"].inflate(0, 24).collidepoint(mouse_x, mouse_y):
                set_audio_slider(state.audio_settings, "master_volume", settings_layout["master_slider"], mouse_x)
            elif settings_layout["music_slider"].inflate(0, 24).collidepoint(mouse_x, mouse_y):
                set_audio_slider(state.audio_settings, "music_volume", settings_layout["music_slider"], mouse_x)

        keys = pygame.key.get_pressed()
        mouse_down = pygame.mouse.get_pressed()[0]
        mouse_pos = pygame.mouse.get_pos()
        input_blocked = (
            state.exit_confirmation
            or state.settings_open
            or state.catalog_open
            or state.paused
            or state.resume_countdown > 0
        )
        move_left = not input_blocked and (
            keys[pygame.K_LEFT] or keys[pygame.K_a] or (mouse_down and left_button.collidepoint(mouse_pos))
        )
        move_right = not input_blocked and (
            keys[pygame.K_RIGHT] or keys[pygame.K_d] or (mouse_down and right_button.collidepoint(mouse_pos))
        )
        direction = int(bool(move_right)) - int(bool(move_left))
        firing = not input_blocked and (keys[pygame.K_SPACE] or (mouse_down and fire_button.collidepoint(mouse_pos)))
        shots_before = state.shots_fired
        achievements_before = len(state.achievements)
        was_game_over = state.game_over
        state.update(delta_time, direction, bool(firing))

        music_should_play = not (
            state.game_over
            or state.paused
            or state.catalog_open
            or state.settings_open
            or state.exit_confirmation
            or state.resume_countdown > 0
        )
        if audio_manager is not None:
            audio_manager.sync_settings(state.audio_settings, music_should_play)
            if state.shots_fired > shots_before:
                audio_manager.play_effect("laser")
            if len(state.achievements) > achievements_before:
                audio_manager.play_effect("achievement", 0.65)
            if not was_game_over and state.game_over:
                audio_manager.play_effect("game_over", 0.7)
            current_countdown_mark = int(math.ceil(state.resume_countdown))
            if current_countdown_mark > 0 and current_countdown_mark != countdown_mark:
                audio_manager.play_effect(f"count_{current_countdown_mark}", 0.5)
            elif countdown_mark > 0 and current_countdown_mark == 0:
                audio_manager.play_effect("count_go", 0.55)
            countdown_mark = current_countdown_mark

        draw_game(
            screen,
            state,
            (font, button_font, pause_icon_font, catalog_font, tab_font),
            buttons,
            catalog_layout,
            settings_layout,
            stars,
            mouse_pos,
            mouse_down,
            pygame.time.get_ticks(),
        )
        pygame.display.flip()

    if audio_manager is not None and audio_manager.music_channel is not None:
        audio_manager.music_channel.stop()
    pygame.quit()


if __name__ == "__main__":
    main()
