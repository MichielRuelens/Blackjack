from copy import copy
from typing import List, TYPE_CHECKING

from base.actions.action import Action
from base.actions.request_card_action import RequestCardAction
from base.actions.stop_action import StopAction
from base.players.player import Player
from base.utils.singleton import Singleton

if TYPE_CHECKING:
    from base.game_state import GameState


class ActionService(metaclass=Singleton):

    def __init__(self):
        self._all_actions = [RequestCardAction(), StopAction()]  # type: List['Action']
        self.num_actions = len(self._all_actions)
        self._action_to_idx = {action: i for i, action in enumerate(self._all_actions)}
        self._idx_to_action = {i: action for action, i in self._action_to_idx.items()}

    def action_to_idx(self, action: 'Action') -> int:
        """Return the unique index associated with the given action."""
        return self._action_to_idx[action]

    def idx_to_action(self, index: int) -> 'Action':
        """Return the action associated with the given unique index."""
        # Always return a copy so a unique action object is obtained
        return copy(self._idx_to_action[index])

    def get_valid_actions(self, player: 'Player', game_state: 'GameState') -> List['Action']:
        """Return a list of all valid actions for the given player."""
        # Make sure to return copies of each action so they can be executed later on
        return [copy(a) for a in self._all_actions if a.validate(player, game_state.deck, game_state.phase)]

    def get_valid_actions_mask(self, player: 'Player', game_state: 'GameState') -> List[bool]:
        """Return a boolean mask corresponding to the unique indexes representing the current valid actions."""
        return [a.validate(player, game_state.deck, game_state.phase) for a in self._all_actions]
