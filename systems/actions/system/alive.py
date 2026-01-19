from systems.actions.system import ActionSystem
from entities.entity import Entity
from systems.event_bus import EventBus
from systems.event_bus.event.audio import PlaySoundEvent
import settings


class AliveActionSystem(ActionSystem):
    @classmethod
    def apply_action(self, dt: float, entity: Entity) -> None:
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
