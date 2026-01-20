from entities.entity import Entity
from utils.math.vector import Vector
from utils.math.primitive_surface import (
    CirclePrimitiveSurface,
    RectPrimitiveSurface,
    RotatedRectPrimitiveSurface,
)
from systems.physics.entity import PhysicEntity
from systems.graphics.entity import GraphicEntity
from systems.graphics.system import RenderSystemID
from systems.actions.controller.player import PlayerActionController
from systems.actions.system.alive import AliveActionSystem
from systems.actions.controller.ia import AIActionController
from entities.entity_type import EntityType
from systems.ia_components.slime_ia import SlimeIA
from systems.audio.entity import AudioEntity
from systems.audio.synth.sound import SynthSound
from systems.audio.play_policy import PlayPolicy
from systems.audio.synth.wave_type import WaveType
from systems.actions.action_entity import ActionEntity, ActionControllerID, ActionSystemID
from systems.data.entity import DataEntity
from systems.data.storage.alive import AliveDataStorage
import settings


class EntityFactory:
    # ======= PLAYER ENTITIES =======
    @staticmethod
    def create_player(x: float, y: float) -> Entity:
        return Entity(
            physics_entity=PhysicEntity(position=Vector(x, y), surface=CirclePrimitiveSurface(radius=settings.ENTITY_RADIUS), fixed=False, mass=40),
            graphic_entity=GraphicEntity(
                position=Vector(x, y),
                surface=CirclePrimitiveSurface(radius=settings.ENTITY_RADIUS),
                color=(0, 255, 0),
                z_index=100,
                system_id=RenderSystemID.WORLD,
            ),
            audio_entity=AudioEntity({
                "walk": SynthSound(freq=440, amp=1, duration=0.2, wave_type=WaveType.SIN, play_policy=PlayPolicy.RESTART)
            }),
            action_entity=ActionEntity(
                controller_id=ActionControllerID.PLAYER,
                system_id=ActionSystemID.ALIVE,
            ),
            data_entity=DataEntity(
                data_storage=AliveDataStorage(max_life=100)
            ),
            entity_type=EntityType.PLAYER
        )

    # ======= IA ENTITIES =======
    @staticmethod
    def create_slime(x: float, y: float) -> Entity:
        return Entity(
            physics_entity=PhysicEntity(position=Vector(x, y), surface=CirclePrimitiveSurface(radius=settings.ENTITY_RADIUS), fixed=False, mass=1),
            graphic_entity=GraphicEntity(position=Vector(x, y), surface=CirclePrimitiveSurface(radius=settings.ENTITY_RADIUS), color=(255, 0, 0), z_index=90),
            action_entity=ActionEntity(
                controller_id=ActionControllerID.AI_SLIME,
                system_id=ActionSystemID.ALIVE,
            ),
            data_entity=DataEntity(
                data_storage=AliveDataStorage(max_life=50)
            ),
            entity_type=EntityType.SLIME
        )


    # ======= VISUAL ENTITIES =======
    @staticmethod
    def create_visual_rect(x: float, y: float, width: float = 10, height: float = 10) -> Entity:
        return Entity(
            graphic_entity=GraphicEntity(position=Vector(x, y), surface=RectPrimitiveSurface(width=width, height=height), color=(255, 0, 255), z_index=95, visible=False),
            entity_type=EntityType.VISUAL
        )
    
    @staticmethod
    def create_visual_circle(x: float, y: float, radius: float = 10) -> Entity:
        return Entity(
            graphic_entity=GraphicEntity(position=Vector(x, y), surface=CirclePrimitiveSurface(radius=radius), color=(0, 0, 255), z_index=85),
            entity_type=EntityType.VISUAL
        )

    # ======= SOLID ENTITIES =======
    @staticmethod
    def create_solid_rect(x: float, y: float, width: float = 10, height: float = 10) -> Entity:
        return Entity(
            physics_entity=PhysicEntity(position=Vector(x, y), surface=RectPrimitiveSurface(width=width, height=height), fixed=True),
            graphic_entity=GraphicEntity(position=Vector(x, y), surface=RectPrimitiveSurface(width=width, height=height), color=(255, 0, 255)),
            entity_type=EntityType.SOLID
        )


    @staticmethod
    def create_solid_rotated_rect_list(x: float, y: float, width: float = 10, height: float = 10, rotation: float = 45) -> Entity:
        return Entity(
            physics_entity=PhysicEntity(position=Vector(x, y), surface=RotatedRectPrimitiveSurface(width=width, height=height, rotation=rotation), fixed=True),
            entity_type=EntityType.SOLID
        )

    @staticmethod
    def create_solid_circle(x: float, y: float, radius: float = 10) -> Entity:
        return Entity(
            physics_entity=PhysicEntity(position=Vector(x, y), surface=CirclePrimitiveSurface(radius=radius), fixed=False),
            graphic_entity=GraphicEntity(position=Vector(x, y), surface=CirclePrimitiveSurface(radius=radius), color=(0, 0, 255)),
            entity_type=EntityType.SOLID
        )
