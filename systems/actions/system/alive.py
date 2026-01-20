from systems.actions.system import ActionSystem
from entities.entity import Entity
from systems.event_bus import EventBus
from systems.event_bus.event.audio import PlaySoundEvent
from systems.data.storage.alive import AliveDataStorage
import settings


class AliveActionSystem(ActionSystem):
    @classmethod
    def apply_action(self, dt: float, entity: Entity) -> None:
        if entity.data_entity and isinstance(entity.data_entity.data_storage, AliveDataStorage):
            data = entity.data_entity.data_storage
            if data.life <= 0:
                data.dead = True
            
            if data.dead:
                data.time_before_delete -= dt
        
        if entity.action_entity.current_action is None:
            return
        move = entity.action_entity.current_action.move
        move_normalized = move.normalize()
        acc_max = move_normalized * settings.ENTITY_ACCELERATION

        if move.length > 0:
            EventBus.emit(PlaySoundEvent(key_sound="walk", entity=entity))

        if move.length > acc_max.length:
            entity.physics_entity.acc = move
        else:
            entity.physics_entity.acc = acc_max
