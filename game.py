import pygame
from systems.inputs.input import InputSystem, RawInput
from settings import FPS, WINDOW_WIDTH, WINDOW_HEIGHT
from scenes.scene import SceneManager
from systems.logger import LoggerManager

from scenes.scenes.game_scene import GameScene


class Game:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Slime Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.scene_manager = SceneManager()
        self.scene_manager.switch_scene("game")
        self.font = pygame.font.SysFont(None, 22)
        self.scene_manager.start_active_scene()
        self.logger_manager = LoggerManager()

    def run(self):
        while self.running:
            raw_input = InputSystem.poll()
            self.handle_events(raw_input)
            self.dt = self.clock.tick(FPS) / 1000
            self.scene_manager.handle_events(raw_input)
            self.scene_manager.update(self.dt)
            self.scene_manager.draw(self.display)
            self.logger_manager.update()

            fps = self.clock.get_fps()
            fps_surf = self.font.render(f"FPS: {fps:.0f}", True, (255, 0, 0))
            fps_rect = fps_surf.get_rect(bottomright=(WINDOW_WIDTH - 10, WINDOW_HEIGHT - 10))
            self.display.blit(fps_surf, fps_rect)
            pygame.display.flip()
            
    def handle_events(self, raw_input: RawInput):
        for event in raw_input.events:
            if event.type == pygame.QUIT:
                self.running = False
