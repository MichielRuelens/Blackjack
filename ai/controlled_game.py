from typing import List

from ai.controlled_player import ControlledPlayer
from base.actions.action import Action
from base.actions.action_service import ActionService
from base.game import Game


class ControlledGame(Game):

    def __init__(self):
        super().__init__()

    def play(self, verbose: bool = False):
        raise NotImplemented("The training game can only be played through the play_action() function.")

    def play_action(self, action: Action):
        if not self.initialized:
            raise Exception("Game not initialized")
        self.player.play_action(game_state=self.get_state(), action=action)

    def get_current_actions_mask(self) -> List[bool]:
        """Return a boolean mask representing the current valid actions."""
        return ActionService().get_valid_actions_mask(self.player, self.get_state())

    def _initialize_players(self) -> None:
        self.player = ControlledPlayer()
