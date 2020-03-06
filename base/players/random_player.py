import random
from typing import TYPE_CHECKING

from base.actions.action_service import ActionService
from base.players.player import Player

if TYPE_CHECKING:
    from base.game_state import GameState
    from base.actions.action import Action


class RandomPlayer(Player):

    @property
    def is_human(self):
        return False

    def _choose_action(self, game_state: 'GameState', verbose: bool = False) -> 'Action':
        eligible_actions = ActionService().get_valid_actions(self, game_state)
        return random.choice(eligible_actions)
