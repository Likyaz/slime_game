from abc import ABC, abstractmethod
import pygame

from systems.inputs.input import RawInput


class Scene(ABC):
    def __init__(self):
        self.next_scene: str | None = None

    @abstractmethod
    def handle_events(self, raw_input: RawInput) -> None:
        """Gère les inputs, convertit en actions"""
        pass

    @abstractmethod
    def update(self, dt: float) -> None:
        """Met à jour physique, IA, logique du jeu"""
        pass

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        """Dessine la scène"""
        pass


class SceneManager:
    SCENES: dict[str, type[Scene]] = {}

    def __init__(self):
        self.active_scene: Scene = None

    def switch_scene(self, new_scene: str) -> None:
        self.active_scene = self.SCENES[new_scene]

    def start_active_scene(self) -> None:
        if self.active_scene:
            self.active_scene.start()

    def handle_events(self, raw_input: RawInput) -> None:
        if self.active_scene:
            self.active_scene.handle_events(raw_input)

    def update(self, dt: float) -> None:
        if self.active_scene:
            self.active_scene.update(dt)
    
            if self.active_scene.next_scene:
                self.switch_scene(self.active_scene.next_scene)
                self.active_scene.start()

    def draw(self, screen: pygame.Surface) -> None:
        if self.active_scene:
            self.active_scene.draw(screen)


def register_scene(name: str):
    def decorator(cls):
        SceneManager.SCENES[name] = cls()
        return cls
    return decorator