import math
import random
import sys
from dataclasses import dataclass

import pygame


pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TITLE = "Treinador de Mira - CS2 Style"

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 150, 255)
GRAY = (100, 100, 100)
DARK_GRAY = (40, 40, 40)
ORANGE = (255, 165, 0)
PURPLE = (150, 50, 200)

FONT = pygame.font.Font(None, 36)
FONT_SMALL = pygame.font.Font(None, 28)
FONT_BIG = pygame.font.Font(None, 48)


@dataclass(frozen=True)
class DifficultyConfig:
    body_width: int
    body_height: int
    head_radius: int
    speed_min: float
    speed_max: float
    color: tuple[int, int, int]


DIFFICULTIES: dict[str, DifficultyConfig] = {
    "easy": DifficultyConfig(80, 160, 35, 1.0, 1.5, (100, 200, 100)),
    "normal": DifficultyConfig(60, 120, 25, 2.0, 3.0, BLUE),
    "hard": DifficultyConfig(45, 90, 18, 3.0, 5.0, ORANGE),
    "insane": DifficultyConfig(35, 70, 12, 5.0, 8.0, PURPLE),
}
MIXED_POOL = ["easy", "normal", "hard", "insane"]


class Bot:
    def __init__(self, difficulty: str = "normal") -> None:
        self.difficulty = difficulty
        self.reset()

    def reset(self) -> None:
        margin = 100
        self.x = random.randint(margin, SCREEN_WIDTH - margin)
        self.y = random.randint(margin, SCREEN_HEIGHT - margin)

        config = DIFFICULTIES.get(self.difficulty, DIFFICULTIES["normal"])
        self.width = config.body_width
        self.height = config.body_height
        self.head_radius = config.head_radius
        self.color = config.color

        self.head_x = self.x
        self.head_y = self.y - self.height // 2 - 10

        self.speed_x = random.choice([-1, 1]) * random.uniform(config.speed_min, config.speed_max)
        self.speed_y = random.choice([-1, 1]) * random.uniform(config.speed_min * 0.5, config.speed_max * 0.5)

        self.move_type = random.choice(["linear", "strafe", "jump", "zigzag"])
        self.jump_timer = 0.0
        self.zigzag_timer = 0.0
        self.base_y = self.y

    def update(self) -> None:
        if self.move_type == "linear":
            self.x += self.speed_x
            self.y += self.speed_y
        elif self.move_type == "strafe":
            multiplier = 1.5 if self.difficulty in {"easy", "normal"} else 1.8
            self.x += self.speed_x * multiplier
        elif self.move_type == "jump":
            self.x += self.speed_x
            self.jump_timer += 0.15
            jump_height = 60 if self.difficulty in {"easy", "normal"} else 100
            self.y = self.base_y - abs(math.sin(self.jump_timer)) * jump_height
        elif self.move_type == "zigzag":
            self.zigzag_timer += 0.1
            self.x += self.speed_x
            self.y = self.base_y + math.sin(self.zigzag_timer * 2) * 50

        self.head_x = self.x
        self.head_y = self.y - self.height // 2 - 10

        if self.x < 50 or self.x > SCREEN_WIDTH - 50:
            self.speed_x *= -1
        if self.y < 100 or self.y > SCREEN_HEIGHT - 50:
            self.speed_y *= -1
            self.base_y = self.y

    def draw(self, surface: pygame.Surface) -> None:
        body_rect = pygame.Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)
        pygame.draw.rect(surface, self.color, body_rect)
        pygame.draw.rect(surface, WHITE, body_rect, 2)

        pygame.draw.circle(surface, GRAY, (int(self.head_x), int(self.head_y)), self.head_radius)
        pygame.draw.circle(surface, WHITE, (int(self.head_x), int(self.head_y)), self.head_radius, 2)

        diff_text = FONT_SMALL.render(self.difficulty[0].upper(), True, WHITE)
        surface.blit(diff_text, (int(self.x) - 5, int(self.y) + self.height // 2 + 5))

    def check_headshot(self, mouse_x: int, mouse_y: int) -> bool:
        distance = math.sqrt((mouse_x - self.head_x) ** 2 + (mouse_y - self.head_y) ** 2)
        return distance <= self.head_radius


class Crosshair:
    def __init__(self) -> None:
        self.size = 20
        self.thickness = 2
        self.gap = 8
        self.dot_size = 3

    def draw(self, surface: pygame.Surface, x: int, y: int, on_target: bool) -> None:
        color = GREEN if on_target else RED

        pygame.draw.line(surface, color, (x - self.gap - self.size, y), (x - self.gap, y), self.thickness)
        pygame.draw.line(surface, color, (x + self.gap, y), (x + self.gap + self.size, y), self.thickness)
        pygame.draw.line(surface, color, (x, y - self.gap - self.size), (x, y - self.gap), self.thickness)
        pygame.draw.line(surface, color, (x, y + self.gap), (x, y + self.gap + self.size), self.thickness)
        pygame.draw.circle(surface, color, (x, y), self.dot_size)

        if on_target:
            pygame.draw.circle(surface, GREEN, (x, y), self.size + 10, 1)


class Game:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        self.num_bots = 3
        self.difficulty = "normal"
        self.game_mode = "classic"

        self.hits = 0
        self.shots = 0
        self.headshot_streak = 0
        self.best_streak = 0

        self.time_attack_duration = 60
        self.time_attack_timer = float(self.time_attack_duration)
        self.time_attack_active = False
        self.time_attack_highscore = 0

        self.crosshair = Crosshair()
        self.bots: list[Bot] = []
        self.spawn_bots()

        self.show_menu = True
        self.menu_selection = 0
        self.menu_options = [
            "Iniciar Classic",
            "Iniciar Time Attack (60s)",
            "Dificuldade",
            "Numero de Bots",
            "Sair",
        ]

    def spawn_bots(self) -> None:
        self.bots = []
        for _ in range(self.num_bots):
            selected_difficulty = random.choice(MIXED_POOL) if self.difficulty == "mixed" else self.difficulty
            self.bots.append(Bot(selected_difficulty))

    def reset_game(self) -> None:
        self.hits = 0
        self.shots = 0
        self.headshot_streak = 0
        self.best_streak = 0
        self.spawn_bots()

    def start_classic(self) -> None:
        self.game_mode = "classic"
        self.show_menu = False
        self.time_attack_active = False
        self.reset_game()

    def start_time_attack(self) -> None:
        self.game_mode = "time_attack"
        self.show_menu = False
        self.reset_game()
        self.time_attack_active = True
        self.time_attack_timer = float(self.time_attack_duration)

    def select_menu_option(self) -> None:
        option = self.menu_options[self.menu_selection]
        if option == "Iniciar Classic":
            self.start_classic()
        elif option == "Iniciar Time Attack (60s)":
            self.start_time_attack()
        elif option == "Dificuldade":
            difficulties = ["easy", "normal", "hard", "insane", "mixed"]
            current_idx = difficulties.index(self.difficulty)
            self.difficulty = difficulties[(current_idx + 1) % len(difficulties)]
        elif option == "Numero de Bots":
            self.num_bots = (self.num_bots % 10) + 1
        elif option == "Sair":
            self.running = False

    def draw_menu(self) -> None:
        self.screen.fill(DARK_GRAY)

        title = FONT_BIG.render("TREINADOR DE MIRA", True, GREEN)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - 190, 100))

        for index, option in enumerate(self.menu_options):
            color = GREEN if index == self.menu_selection else WHITE
            text = FONT.render(option, True, color)
            self.screen.blit(text, (SCREEN_WIDTH // 2 - 150, 250 + index * 60))

        info_texts = [
            f"Dificuldade atual: {self.difficulty.upper()}",
            f"Bots: {self.num_bots}",
            f"Recorde Time Attack: {self.time_attack_highscore}",
            "",
            "Use ↑↓ para navegar, ENTER para selecionar",
        ]

        y = 550
        for text in info_texts:
            if text:
                surface = FONT_SMALL.render(text, True, GRAY)
                self.screen.blit(surface, (SCREEN_WIDTH // 2 - 120, y))
            y += 25

    def handle_menu(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_UP:
                    self.menu_selection = (self.menu_selection - 1) % len(self.menu_options)
                elif event.key == pygame.K_DOWN:
                    self.menu_selection = (self.menu_selection + 1) % len(self.menu_options)
                elif event.key == pygame.K_RETURN:
                    self.select_menu_option()

        self.draw_menu()

    def update_time_attack(self) -> None:
        if self.game_mode == "time_attack" and self.time_attack_active:
            self.time_attack_timer -= 1 / FPS
            if self.time_attack_timer <= 0:
                self.time_attack_timer = 0
                self.time_attack_active = False
                self.time_attack_highscore = max(self.time_attack_highscore, self.hits)

    def handle_shot(self, mouse_x: int, mouse_y: int) -> None:
        self.shots += 1
        hit = False

        for bot in self.bots:
            if bot.check_headshot(mouse_x, mouse_y):
                self.hits += 1
                hit = True
                bot.reset()

        if hit:
            self.headshot_streak += 1
            self.best_streak = max(self.best_streak, self.headshot_streak)
        else:
            self.headshot_streak = 0

    def handle_game(self) -> None:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.update_time_attack()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.show_menu = True
                elif event.key == pygame.K_r:
                    if self.game_mode == "time_attack":
                        self.start_time_attack()
                    else:
                        self.reset_game()
                elif event.key == pygame.K_UP and self.game_mode == "classic":
                    self.num_bots = min(self.num_bots + 1, 10)
                    selected_difficulty = random.choice(MIXED_POOL) if self.difficulty == "mixed" else self.difficulty
                    self.bots.append(Bot(selected_difficulty))
                elif event.key == pygame.K_DOWN and self.game_mode == "classic":
                    self.num_bots = max(self.num_bots - 1, 1)
                    self.bots = self.bots[: self.num_bots]
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.game_mode == "classic" or self.time_attack_active:
                    self.handle_shot(mouse_x, mouse_y)

        for bot in self.bots:
            bot.update()

        on_target = any(bot.check_headshot(mouse_x, mouse_y) for bot in self.bots)
        self.draw_game(mouse_x, mouse_y, on_target)

    def draw_hud(self, on_target: bool) -> None:
        accuracy = (self.hits / self.shots * 100) if self.shots > 0 else 0

        left_texts = [
            f"Headshots: {self.hits}",
            f"Tiros: {self.shots}",
            f"Precisao: {accuracy:.1f}%",
            f"Sequencia: {self.headshot_streak}",
            f"Melhor sequencia: {self.best_streak}",
        ]
        y = 10
        for text in left_texts:
            surface = FONT_SMALL.render(text, True, WHITE)
            self.screen.blit(surface, (10, y))
            y += 25

        right_texts = [
            (f"Modo: {self.game_mode.upper()}", WHITE),
            (f"Dificuldade: {self.difficulty.upper()}", WHITE),
            (f"Bots: {self.num_bots}", WHITE),
        ]
        if self.game_mode == "time_attack":
            timer_color = RED if self.time_attack_timer < 10 else YELLOW if self.time_attack_timer < 30 else GREEN
            right_texts.append((f"Tempo: {int(self.time_attack_timer)}s", timer_color))

        y = 10
        for text, color in right_texts:
            surface = FONT_SMALL.render(text, True, color)
            self.screen.blit(surface, (SCREEN_WIDTH - surface.get_width() - 10, y))
            y += 25

        if on_target:
            indicator = FONT.render("HEADSHOT!", True, GREEN)
            self.screen.blit(indicator, (SCREEN_WIDTH // 2 - 60, 80))

        help_text = "[R] Reset | [↑↓] Bots | [ESC] Menu"
        if self.game_mode == "time_attack" and not self.time_attack_active:
            help_text = "[R] Jogar novamente | [ESC] Menu"
        surface = FONT_SMALL.render(help_text, True, GRAY)
        self.screen.blit(surface, (SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT - 30))

    def draw_time_attack_end(self) -> None:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        is_new_record = self.hits >= self.time_attack_highscore and self.hits > 0
        results = [
            ("TIME ATTACK FINALIZADO!", FONT_BIG, YELLOW),
            ("", None, None),
            (f"Headshots: {self.hits}", FONT, WHITE),
            (f"Tiros: {self.shots}", FONT, WHITE),
            (f"Precisao: {(self.hits / self.shots * 100) if self.shots > 0 else 0:.1f}%", FONT, WHITE),
            (f"Melhor sequencia: {self.best_streak}", FONT, WHITE),
            ("", None, None),
            (("NOVO RECORDE!" if is_new_record else f"Recorde: {self.time_attack_highscore}"), FONT_BIG if is_new_record else FONT, GREEN if is_new_record else WHITE),
            ("", None, None),
            ("Pressione R para jogar novamente", FONT, WHITE),
        ]

        y = 200
        for text, font_obj, color in results:
            if text and font_obj is not None:
                surface = font_obj.render(text, True, color)
                self.screen.blit(surface, (SCREEN_WIDTH // 2 - surface.get_width() // 2, y))
            y += 40

    def draw_game(self, mouse_x: int, mouse_y: int, on_target: bool) -> None:
        self.screen.fill(DARK_GRAY)
        for bot in self.bots:
            bot.draw(self.screen)
        self.crosshair.draw(self.screen, mouse_x, mouse_y, on_target)
        self.draw_hud(on_target)
        if self.game_mode == "time_attack" and not self.time_attack_active:
            self.draw_time_attack_end()

    def run(self) -> None:
        pygame.mouse.set_visible(False)
        while self.running:
            if self.show_menu:
                self.handle_menu()
            else:
                self.handle_game()
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


def main() -> None:
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
