from systems.physics import PhysicsEntity
from systems.graphic import GraphicEntity
from systems.items import InventoryComponent
from systems.ia_components.ia_component import IAComponent
from systems.action_controllers.action_controller import ActionController, EntityAction
from entities.entity_type import EntityType
import settings




class Entity:
    def __init__(
        self,
        physics_entity: PhysicsEntity = None,
        graphic_entity: GraphicEntity = None,
        # inventory_component: InventoryComponent = None,
        action_controller: ActionController = None,
        entity_type: EntityType = EntityType.NONE,
    ):
        self.physics_entity = physics_entity
        self.graphic_entity = graphic_entity
        # self.inventory_component = inventory_component
        self.entity_type = entity_type
        self.action_controller = action_controller # Il choisit quoi faire
        self.entity_action = EntityAction() # Il stock quoi faire
        # self.action_system: ActionSystem# Applique l'action a la physique

    def update(self, dt: float, action: EntityAction):
        move_normalized = action.move.normalize()
        acc = move_normalized * settings.ENTITY_ACCELERATION
        if action.move.length > acc.length:
            self.physics_entity.acc = action.move
        else:
            self.physics_entity.acc = acc
