from __future__ import annotations

from typing import TYPE_CHECKING, Type


from systems.actions.action import EntityAction
from entities.entity_type import EntityType

if TYPE_CHECKING:
    from systems.actions.action_system import ActionSystem
    from systems.physics import PhysicEntity
    from systems.graphic import GraphicEntity
    from systems.audio.entity import AudioEntity
    # from systems.items import InventoryComponent
    from systems.actions.action_controller import ActionController


class Entity:
    def __init__(
        self,
        physics_entity: PhysicEntity = None,
        graphic_entity: GraphicEntity = None,
        audio_entity: AudioEntity = None,
        # inventory_component: InventoryComponent = None,
        action_controller: ActionController = None,
        action_system: Type[ActionSystem] = None,
        entity_type: EntityType = EntityType.NONE,
    ):
        self.physics_entity = physics_entity
        self.graphic_entity = graphic_entity
        self.audio_entity = audio_entity
        # self.inventory_component = inventory_component
        self.entity_type = entity_type
        self.action_controller = action_controller
        self.entity_action = EntityAction()
        self.action_system = action_system
