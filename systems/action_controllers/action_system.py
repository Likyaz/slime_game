from entities.entity import Entity

class ActionSystem:
    def __init__(self):
        self.entities = entities

    def update(self, dt: float, entity: Entity):
        for entity in self.entities:
            entity.entity_action = entity.action_controller.get_action()


class AliveActionSystem(ActionSystem):
    def __init__(self):
        super().__init__()

    def update(self, dt: float, entity: Entity):
        entity.entity_action = entity.action_controller.get_action()