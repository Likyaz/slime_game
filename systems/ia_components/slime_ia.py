from dataclasses import dataclass
import random

from systems.ia_components.ia_component import IAComponent
from systems.action_controllers.action_controller import EntityAction
from systems.physics import Vector
from systems.action_controllers.ia_action_controller import EntityPerception
from entities.entity import EntityType

class SlimeIA(IAComponent):
    def __init__(self):
        self.target_direction = Vector.random_unit_vector()
        self.rotation_speed = 0
        self.rotation_acc = 0


    def action(self, entity_perception: EntityPerception):
        # for entity_info in entity_perception.entities:
            # if entity_info.type == EntityType.PLAYER:
                # if entity_info.distance.length < 100:
                #     return EntityAction(
                #             move=entity_info.distance,
                #             pick=False
                #         )
                # else:
        self.rotation_acc += random.uniform(-0.05, 0.05)
        self.rotation_acc = max(-0.1, min(self.rotation_acc, 0.1))
        self.rotation_speed += self.rotation_acc
        self.rotation_speed = max(-0.3, min(self.rotation_speed, 0.3))
        self.target_direction = self.target_direction.add_angle_random(-self.rotation_speed , self.rotation_speed)
        return EntityAction(
            move=self.target_direction,
            pick=False
        )
        # return EntityAction(
        #     move=Vector(0, 0),
        #     pick=False
        # )
