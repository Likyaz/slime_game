from __future__ import annotations

from typing import TYPE_CHECKING

from entities.entity_type import EntityType


if TYPE_CHECKING:
    from systems.physics.entity import PhysicEntity
    from systems.graphics.entity import GraphicEntity
    from systems.audio.entity import AudioEntity
    # from systems.items import InventoryComponent
    from systems.actions.action_entity import ActionEntity


class Entity:
    def __init__(
        self,
        physics_entity: PhysicEntity = None,
        graphic_entity: GraphicEntity = None,
        audio_entity: AudioEntity = None,
        # inventory_component: InventoryComponent = None,
        action_entity: ActionEntity = None,
        entity_type: EntityType = EntityType.NONE,
    ):
        self.physics_entity = physics_entity
        self.graphic_entity = graphic_entity
        self.audio_entity = audio_entity
        # self.inventory_component = inventory_component
        self.entity_type = entity_type
        self.action_entity = action_entity

    def __repr__(self):
        return (
            "Entity(\n"
            f"  physics_entity={self.physics_entity},\n"
            f"  graphic_entity={self.graphic_entity},\n"
            f"  audio_entity={self.audio_entity},\n"
            f"  entity_type={self.entity_type},\n"
            f"  action_entity={self.action_entity}\n"
            ")"
        )
    
    def __str__(self):
        return self.__repr__()
