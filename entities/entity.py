from __future__ import annotations

from typing import TYPE_CHECKING, Type

from systems.physics import PhysicEntity
from systems.graphic import GraphicEntity
from systems.items import InventoryComponent
from systems.actions.action_controller import ActionController
from systems.actions.action import EntityAction
from entities.entity_type import EntityType

if TYPE_CHECKING:
    from systems.actions.action_system import ActionSystem


class Entity:
    def __init__(
        self,
        physics_entity: PhysicEntity = None,
        graphic_entity: GraphicEntity = None,
        # inventory_component: InventoryComponent = None,
        action_controller: ActionController = None,
        action_system: Type[ActionSystem] = None,
        entity_type: EntityType = EntityType.NONE,
    ):
        self.physics_entity = physics_entity
        self.graphic_entity = graphic_entity
        # self.inventory_component = inventory_component
        self.entity_type = entity_type
        self.action_controller = action_controller # Il choisit quoi faire
        self.entity_action = EntityAction() # Il stock quoi faire
        self.action_system = action_system # Applique l'action a la physique
