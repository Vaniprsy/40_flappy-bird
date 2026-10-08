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

        self.bird = Bird(width // 4, height // 2)
        self.pipe_speed = 4
        self.pipe_interval = 90  # frames between pipe spawns
        self._spawn_timer = 0
        self.pipes = [Pipe(width + 100, height, speed=self.pipe_speed)]

        self.score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        self.game_over = False

    def handle_event(self, event):
        # Handle flap and restart input
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if self.game_over:
                self.reset()
            else:
                self.bird.flap()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.game_over:
                self.reset()
            else:
                self.bird.flap()

    def handle_input(self):
        # Reserved for continuously-held-key input
        pass

    def reset(self):
        """Reset the game after Game Over."""
        self.bird = Bird(self.width // 4, self.height // 2)
        self.pipes = [
            Pipe(self.width + 100, self.height, speed=self.pipe_speed)
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
                Pipe(self.width, self.height, speed=self.pipe_speed)
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

        self.pipes = [p for p in self.pipes if not p.off_screen()]

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

        # Draw current score
        score_text = self.font.render(
            f"Score: {self.score}",
            True,
            WHITE
        )
        screen.blit(score_text, (10, 10))

        # Task 2: Game Over screen
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

            restart_text = self.font.render(
                "Press SPACE to restart",
                True,
                WHITE
            )

            screen.blit(
                game_over_text,
                (
                    self.width // 2 - game_over_text.get_width() // 2,
                    250
                )
            )

            screen.blit(
                final_score_text,
                (
                    self.width // 2 - final_score_text.get_width() // 2,
                    300
                )
            )

            screen.blit(
                restart_text,
                (
                    self.width // 2 - restart_text.get_width() // 2,
                    350
                )
            )
            