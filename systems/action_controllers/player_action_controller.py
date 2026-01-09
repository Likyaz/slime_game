from systems.action_controllers.action_controller import ActionController, EntityAction
from systems.inputs.game_input import GameAction


class PlayerActionController(ActionController):
    def feed_input(self, game_action: GameAction) -> None:
        self.last_action = EntityAction(
            move=game_action.move,
            pick=game_action.pick
        )

    def get_action(self) -> EntityAction:
        return self.last_action
