import pygame
from .bird import Bird
from .pipe import Pipe

# Game Engine

WHITE = (255, 255, 255)
GREEN = (0, 150, 0)


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.pipe_speed = 4
        self.pipe_gap = 150
        self.pipe_interval = 90

        self.bird = Bird(width // 4, height // 2)
        self._spawn_timer = 0
        self.pipes = [
            Pipe(
                width + 100,
                height,
                gap=self.pipe_gap,
                speed=self.pipe_speed
            )
        ]

        self.score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        self.game_over = False
        self.difficulty_menu = False
        self.exit_game = False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:

            # Task 3: Difficulty selection after Game Over
            if self.game_over:
                if event.key == pygame.K_1:
                    self.set_difficulty("Easy")
                elif event.key == pygame.K_2:
                    self.set_difficulty("Medium")
                elif event.key == pygame.K_3:
                    self.set_difficulty("Hard")
                elif event.key == pygame.K_4:
                    self.exit_game = True

            # Normal gameplay
            else:
                if event.key == pygame.K_SPACE:
                    self.bird.flap()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if not self.game_over:
                self.bird.flap()

    def handle_input(self):
        # Reserved for continuously-held-key input
        pass

    def set_difficulty(self, difficulty):
        if difficulty == "Easy":
            self.pipe_speed = 3
            self.pipe_gap = 190

        elif difficulty == "Medium":
            self.pipe_speed = 4
            self.pipe_gap = 150

        elif difficulty == "Hard":
            self.pipe_speed = 6
            self.pipe_gap = 110

        self.reset()

    def reset(self):
        """Reset the game after choosing a difficulty."""
        self.bird = Bird(self.width // 4, self.height // 2)

        self.pipes = [
            Pipe(
                self.width + 100,
                self.height,
                gap=self.pipe_gap,
                speed=self.pipe_speed
            )
        ]

        self._spawn_timer = 0
        self.score = 0
        self.game_over = False

    def update(self):
        if self.game_over:
            return

        self.bird.update()

        # Ground and ceiling collision
        if (
            self.bird.y - self.bird.radius <= 0
            or self.bird.y + self.bird.radius >= self.height
        ):
            self.game_over = True
            return

        self._spawn_timer += 1

        if self._spawn_timer >= self.pipe_interval:
            self._spawn_timer = 0

            self.pipes.append(
                Pipe(
                    self.width,
                    self.height,
                    gap=self.pipe_gap,
                    speed=self.pipe_speed
                )
            )

        for pipe in self.pipes:
            pipe.move()

            # Task 1: Accurate collision detection
            if (
                self.bird.rect().colliderect(pipe.top_rect())
                or self.bird.rect().colliderect(pipe.bottom_rect())
            ):
                self.game_over = True

            # Score when bird passes a pipe
            if not pipe.scored and pipe.x + pipe.width < self.bird.x:
                pipe.scored = True
                self.score += 1

        self.pipes = [
            p for p in self.pipes
            if not p.off_screen()
        ]

    def render(self, screen):
        # Draw pipes
        for pipe in self.pipes:
            pygame.draw.rect(screen, GREEN, pipe.top_rect())
            pygame.draw.rect(screen, GREEN, pipe.bottom_rect())

        # Draw bird
        pygame.draw.circle(
            screen,
            WHITE,
            (int(self.bird.x), int(self.bird.y)),
            self.bird.radius
        )

        # Draw score
        score_text = self.font.render(
            f"Score: {self.score}",
            True,
            WHITE
        )
        screen.blit(score_text, (10, 10))

        # Task 2 + Task 3
        if self.game_over:
            game_over_text = self.font.render(
                "GAME OVER",
                True,
                WHITE
            )

            final_score_text = self.font.render(
                f"Final Score: {self.score}",
                True,
                WHITE
            )

            difficulty_text = self.font.render(
                "Choose Difficulty",
                True,
                WHITE
            )

            easy_text = self.font.render(
                "1 - Easy",
                True,
                WHITE
            )

            medium_text = self.font.render(
                "2 - Medium",
                True,
                WHITE
            )

            hard_text = self.font.render(
                "3 - Hard",
                True,
                WHITE
            )

            exit_text = self.font.render(
                "4 - Exit",
                True,
                WHITE
            )

            screen.blit(
                game_over_text,
                (
                    self.width // 2 - game_over_text.get_width() // 2,
                    180
                )
            )

            screen.blit(
                final_score_text,
                (
                    self.width // 2 - final_score_text.get_width() // 2,
                    230
                )
            )

            screen.blit(
                difficulty_text,
                (
                    self.width // 2 - difficulty_text.get_width() // 2,
                    290
                )
            )

            screen.blit(
                easy_text,
                (
                    self.width // 2 - easy_text.get_width() // 2,
                    340
                )
            )

            screen.blit(
                medium_text,
                (
                    self.width // 2 - medium_text.get_width() // 2,
                    380
                )
            )

            screen.blit(
                hard_text,
                (
                    self.width // 2 - hard_text.get_width() // 2,
                    420
                )
            )

            screen.blit(
                exit_text,
                (
                    self.width // 2 - exit_text.get_width() // 2,
                    460
                )
            )