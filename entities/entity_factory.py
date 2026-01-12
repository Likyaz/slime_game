from entities.entity import Entity
from systems.vector import Vector
from systems.physics.entity import PhysicEntity
from systems.physics.surface import CirclePhysicSurface, RectPhysicSurface, RotatedRectPhysicSurface
from systems.graphics.entity import GraphicEntity
from systems.graphics.surface import CircleGraphicSurface, RectGraphicSurface, RotatedRectGraphicSurface
from systems.actions.action_controller import PlayerActionController, AIActionController
from systems.actions.action_system import AliveActionSystem
from entities.entity_type import EntityType
from systems.ia_components.slime_ia import SlimeIA
from systems.audio.entity import AudioEntity
from systems.audio.synth.sound import SynthSound
from systems.audio.play_policy import PlayPolicy
from systems.audio.synth.wave_type import WaveType

import settings


class EntityFactory:
    # ======= PLAYER ENTITIES =======
    @staticmethod
    def create_player(x: float, y: float) -> Entity:
        return Entity(
            physics_entity=PhysicEntity(position=Vector(x, y), surface=CirclePhysicSurface(radius=settings.ENTITY_RADIUS), fixed=False, mass=40),
            graphic_entity=GraphicEntity(position=Vector(x, y), surface=CircleGraphicSurface(radius=settings.ENTITY_RADIUS), color=(0, 255, 0), z_index=100),
            audio_entity=AudioEntity({
                "walk": SynthSound(freq=440, amp=1, duration=0.2, wave_type=WaveType.SIN, play_policy=PlayPolicy.RESTART)
            }),
            action_controller=PlayerActionController(),
            action_system=AliveActionSystem,
            entity_type=EntityType.PLAYER
        )

    # ======= IA ENTITIES =======
    @staticmethod
    def create_slime(x: float, y: float) -> Entity:
        return Entity(
            physics_entity=PhysicEntity(position=Vector(x, y), surface=CirclePhysicSurface(radius=settings.ENTITY_RADIUS), fixed=False, mass=1),
            graphic_entity=GraphicEntity(position=Vector(x, y), surface=CircleGraphicSurface(radius=settings.ENTITY_RADIUS), color=(255, 0, 0), z_index=90),
            action_controller=AIActionController(SlimeIA()),
            action_system=AliveActionSystem,
            entity_type=EntityType.SLIME
        )


    # ======= VISUAL ENTITIES =======
    @staticmethod
    def create_visual_rect(x: float, y: float, width: float = 10, height: float = 10) -> Entity:
        return Entity(
            graphic_entity=GraphicEntity(position=Vector(x, y), surface=RectGraphicSurface(width=width, height=height), color=(255, 0, 255), z_index=95),
            entity_type=EntityType.VISUAL
        )
    
    @staticmethod
    def create_visual_circle(x: float, y: float, radius: float = 10) -> Entity:
        return Entity(
            graphic_entity=GraphicEntity(position=Vector(x, y), surface=CircleGraphicSurface(radius=radius), color=(0, 0, 255), z_index=85),
            entity_type=EntityType.VISUAL
        )

    # ======= SOLID ENTITIES =======
    @staticmethod
    def create_solid_rect(x: float, y: float, width: float = 10, height: float = 10) -> Entity:
        return Entity(
            physics_entity=PhysicEntity(position=Vector(x, y), surface=RectPhysicSurface(width=width, height=height), fixed=True),
            graphic_entity=GraphicEntity(position=Vector(x, y), surface=RectGraphicSurface(width=width, height=height), color=(255, 0, 255)),
            entity_type=EntityType.SOLID
        )


    @staticmethod
    def create_solid_rotated_rect_list(x: float, y: float, width: float = 10, height: float = 10, rotation: float = 45) -> Entity:
        return Entity(
            physics_entity=PhysicEntity(position=Vector(x, y), surface=RotatedRectPhysicSurface(width=width, height=height, rotation=rotation), fixed=True),
            entity_type=EntityType.SOLID
        )

    @staticmethod
    def create_solid_circle(x: float, y: float, radius: float = 10) -> Entity:
        return Entity(
            physics_entity=PhysicEntity(position=Vector(x, y), surface=CirclePhysicSurface(radius=radius), fixed=False),
            graphic_entity=GraphicEntity(position=Vector(x, y), surface=CircleGraphicSurface(radius=radius), color=(0, 0, 255)),
            entity_type=EntityType.SOLID
        )
