from scenes.scene import Scene
import pygame

from systems.inputs.input import RawInput
from systems.inputs.game_input import GameInput
from systems.physics import PhysicSystem
from systems.graphic import GraphicSystem
from entities.entity_manager import EntityManager
from entities.entity_factory import EntityFactory
from scenes.scene import register_scene
from systems.actions.action_system import ActionSystemManager
import settings


@register_scene("game")
class GameScene(Scene):
    def __init__(self):
        super().__init__()
        self.physics_system = PhysicSystem()
        self.graphic_system = GraphicSystem()
        self.action_system_manager = ActionSystemManager()
        self.input = GameInput()

        self.entity_manager = EntityManager(
            physics_system=self.physics_system,
            graphic_system=self.graphic_system,
            action_system_manager=self.action_system_manager
        )

        # ========= Create Player =========
        self.player = EntityFactory.create_player(800, 600)
        self.entity_manager.add_entity(self.player)

        # ========= Create Solids =========
        self.solids = [
            # Le cadre de la scène
            EntityFactory.create_solid_rect(settings.WINDOW_WIDTH // 2, -25, settings.WINDOW_WIDTH + 100, 50),
            EntityFactory.create_solid_rect(settings.WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT + 25, settings.WINDOW_WIDTH + 100, 50),
            EntityFactory.create_solid_rect(-25, settings.WINDOW_HEIGHT // 2, 50, settings.WINDOW_HEIGHT + 100),
            EntityFactory.create_solid_rect(settings.WINDOW_WIDTH + 25, settings.WINDOW_HEIGHT // 2, 50, settings.WINDOW_HEIGHT + 100),
            # EntityFactory.create_solid_rect(50, 50, 300, 10),


            EntityFactory.create_solid_rect(400, 300, 300, 50),
            EntityFactory.create_solid_circle(500, 500, 10),
        ]
        self.entity_manager.add_entities(self.solids)

        # ========= Create Slimes =========
        self.slimes = [
            EntityFactory.create_slime(600, 350)
            for _ in range(100)
        ]
        self.entity_manager.add_entities(self.slimes)

        # ========= Create Visual Entities =========
        self.visual_entities = [
            EntityFactory.create_visual_rect(100, 100, 100, 100),
            EntityFactory.create_visual_circle(200, 200, 50),
        ]
        self.entity_manager.add_entities(self.visual_entities)

    def handle_events(self, raw_input: RawInput) -> None:
        game_action = self.input.handle(raw_input)
        self.player.action_controller.feed_input(game_action)
        if game_action.open_inventory:
            self.next_scene = "inventory"

    def update(self, dt: float) -> None:
        self.physics_system.update_all(dt)
        self.entity_manager.update_all(dt)
        self.action_system_manager.update_all(dt)

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill((0, 0, 0))
        self.graphic_system.draw_all(screen)


