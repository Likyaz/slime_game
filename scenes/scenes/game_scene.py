from scenes.scene import Scene
import pygame

from systems.inputs.manager import RawInput
from systems.inputs.manager import InputSystemManager
from systems.inputs.system.game import GameInputSystem
from systems.physics.manager import PhysicSystemManager
from systems.physics.system.top_down import TopDownPhysicsSystem
from systems.graphics.manager import GraphicSystemManager
from systems.graphics.system.top_view_2d import TopView2DGraphicSystem
from entities.entity_manager import EntityManager
from entities.entity_factory import EntityFactory
from scenes.scene import register_scene
from systems.actions.action_system import ActionSystemManager
from systems.audio.audio_system_manager import AudioSystemManager
from systems.audio.synth.source import SynthAudioSource
import settings


@register_scene("game")
class GameScene(Scene):
    def __init__(self):
        super().__init__()
        self.physics_system_manager = PhysicSystemManager(TopDownPhysicsSystem())
        self.graphic_system_manager = GraphicSystemManager(TopView2DGraphicSystem())
        self.action_system_manager = ActionSystemManager()
        self.input_system_manager = InputSystemManager(GameInputSystem())
        self.audio_system = AudioSystemManager()
        self.audio_system.register_audio_source(SynthAudioSource)

        self.entity_manager = EntityManager(
            physics_system_manager=self.physics_system_manager,
            graphic_system_manager=self.graphic_system_manager,
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
            for _ in range(10)
        ]
        self.entity_manager.add_entities(self.slimes)

        # ========= Create Visual Entities =========
        self.visual_entities = [
            EntityFactory.create_visual_rect(100, 100, 100, 100),
            EntityFactory.create_visual_circle(200, 200, 50),
        ]
        self.entity_manager.add_entities(self.visual_entities)

    def start(self) -> None:
        self.audio_system.start_audio()

    def quit(self) -> None:
        self.audio_system.stop_audio()
        super().quit()

    def handle_events(self, raw_input: RawInput) -> None:
        game_action = self.input_system_manager.handle(raw_input)
        self.player.action_controller.feed_input(game_action)
        # if game_action.open_inventory:
        #     self.next_scene = "inventory"

    def update(self, dt: float) -> None:
        self.physics_system_manager.update_all(dt)
        self.entity_manager.update_all(dt)
        self.action_system_manager.update_all(dt)
        self.audio_system.play_sounds()

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill((0, 0, 0))
        self.graphic_system_manager.draw_all(screen)


