import random

from systems.ia_components.ia_component import IAComponent
from utils.math.vector import Vector
from systems.actions.action.alive import AliveActionEntity
from systems.actions.controller.ia import EntityPerception
from entities.entity_type import EntityType


class SlimeIA(IAComponent):
    def __init__(self):
        self.target_direction = Vector.random_unit_vector()
        self.rotation_speed = 0
        self.rotation_acc = 0


    def action(self, entity_perception: EntityPerception):
        closest_slime = None
        closest_slime_distance = float('inf')
        for entity_info in entity_perception.entities:
            if entity_info.type == EntityType.SLIME and not entity_info.entity.data_entity.data_storage.dead:
                if entity_info.distance.length < 100 and entity_info.distance.length < closest_slime_distance:
                    closest_slime = entity_info
                    closest_slime_distance = entity_info.distance.length

        if closest_slime:
            return AliveActionEntity(
                move=closest_slime.distance,
                pick=False,
                target=closest_slime.entity,
                attack=True
            )

        self.rotation_acc += random.uniform(-0.05, 0.05)
        self.rotation_acc = max(-0.1, min(self.rotation_acc, 0.1))
        self.rotation_speed += self.rotation_acc
        self.rotation_speed = max(-0.3, min(self.rotation_speed, 0.3))
        self.target_direction = self.target_direction.add_angle_random(-self.rotation_speed , self.rotation_speed)
        return AliveActionEntity(
            move=self.target_direction,
            pick=False,
            target=None,
            attack=False
        )
        # return EntityAction(
        #     move=Vector(0, 0),
        #     pick=False
        # )
