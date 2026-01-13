from systems.actions.system import ActionSystem
from entities.entity import Entity
from systems.event_bus import EventBus
from systems.event_bus.event.audio import PlaySoundEvent
import settings


class AliveActionSystem(ActionSystem):
    @classmethod
    def apply_action(self, dt: float, entity: Entity) -> None:
        move_normalized = entity.entity_action.move.normalize()
        acc = move_normalized * settings.ENTITY_ACCELERATION

        if entity.entity_action.move.length > 0:
            EventBus.emit(PlaySoundEvent(key_sound="walk", entity=entity))

        if entity.entity_action.move.length > acc.length:
            entity.physics_entity.acc = entity.entity_action.move
        else:
            entity.physics_entity.acc = acc
