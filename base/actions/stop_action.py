import logging
from numbers import Number
from typing import TYPE_CHECKING

from base.actions.action import Action
from base.enums.game_phase import GamePhase

if TYPE_CHECKING:
    from base.cards.deck import Deck
    from base.players.player import Player


class StopAction(Action):
    """ Stop the turn action. """

    def _key(self):
        """Return a tuple of all fields that should be checked in equality and hashing operations."""
        return None

    def get_reward(self) -> Number:
        return 1

    def validate(self, player: 'Player', deck: 'Deck', phase: 'GamePhase', verbose: bool = False):
        if phase != GamePhase.PLAYER_PHASE:
            if verbose:
                logging.info("Invalid action {}. Reason: wrong phase - {}".format(self, phase))
            return False
        if player.broken:
            logging.info("Invalid action {}. Player is broken.")
            return False
        return True

    def _execute(self, player: 'Player', deck: 'Deck', phase: 'GamePhase'):
        player.stopped = True

    def _target_phase(self, player: 'Player', deck: 'Deck', phase: 'GamePhase') -> GamePhase:
        return GamePhase.HOUSE_PHASE

    def __str__(self):
        execution_tag = "" if not self.is_executed else "(E) "
        return "{}StopAction".format(execution_tag)
