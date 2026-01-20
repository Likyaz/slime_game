from systems.actions.system import ActionSystem
from entities.entity import Entity
from systems.event_bus import EventBus
from systems.event_bus.event.audio import PlaySoundEvent
from systems.data.storage.alive import AliveDataStorage
import settings
from utils.math.vector import Vector


class AliveActionSystem(ActionSystem):
    @classmethod
    def apply_action(self, dt: float, entity: Entity) -> None:
        # life gestion
        data = entity.data_entity.data_storage
        if data.life <= 0:
            data.dead = True

        if data.dead:
            entity.graphic_entity.color = (0, 0, 255)
            data.time_before_delete -= dt
    
        # if no action or dead, return
        if entity.action_entity.current_action is None or data.dead:
            entity.physics_entity.acc = Vector(0, 0)
            return

        # attack gestion
        if entity.action_entity.current_action.attack and entity.action_entity.current_action.target:
            dist = entity.physics_entity.position - entity.action_entity.current_action.target.physics_entity.position
            if dist.length < 10:
                target = entity.action_entity.current_action.target
                if target and isinstance(target.data_entity.data_storage, AliveDataStorage):
                    target.data_entity.data_storage.life -= 1
                return

        # move gestion
        move = entity.action_entity.current_action.move
        move_normalized = move.normalize()
        acc_max = move_normalized * settings.ENTITY_ACCELERATION

        if move.length > 0:
            EventBus.emit(PlaySoundEvent(key_sound="walk", entity=entity))

        if move.length > acc_max.length:
            entity.physics_entity.acc = move
        else:
            entity.physics_entity.acc = acc_max
