from typing import TYPE_CHECKING

from base.actions.action_service import ActionService
from base.players.player import Player

if TYPE_CHECKING:
    from base.game_state import GameState
    from base.actions.action import Action


class HumanPlayer(Player):

    @property
    def is_human(self):
        return True

    def _choose_action(self, game_state: 'GameState', verbose: bool = False) -> 'Action':
        eligible_actions = ActionService().get_valid_actions(self, game_state)
        for i, action in enumerate(eligible_actions):
            print("{}: {}".format(i, action))
        action_index = None
        while action_index is None:
            try:
                action_index = input("Type the number of the action you wish to execute:")
                action_index = int(action_index)
            except ValueError:
                print("Invalid action number '{}', please enter a number!".format(action_index))
                action_index = None
        return eligible_actions[action_index]
