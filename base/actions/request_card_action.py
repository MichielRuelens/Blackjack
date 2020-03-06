import logging
from numbers import Number
from typing import TYPE_CHECKING

from base.actions.action import Action
from base.enums.game_phase import GamePhase

if TYPE_CHECKING:
    from base.players.player import Player
    from base.cards.deck import Deck


class RequestCardAction(Action):
    """ Request a card from the dealer. """

    def _key(self):
        """Return a tuple of all fields that should be checked in equality and hashing operations."""
        return None

    def get_reward(self) -> Number:
        return 0

    def validate(self, player: 'Player', deck: 'Deck', phase: 'GamePhase', verbose: bool = False):
        if phase != GamePhase.PLAYER_PHASE:
            if verbose:
                logging.info("Invalid action {}. Reason: wrong phase - {}".format(self, phase))
            return False
        if player.broken:
            logging.info("Invalid action {}. Player is broken.")
            return False
        if player.stopped:
            logging.info("Invalid action {}. Player has stopped.")
        return True

    def _execute(self, player: 'Player', deck: 'Deck', phase: 'GamePhase'):
        deck_card = deck.deal()
        player.hand.add(deck_card)
        if player.score == 21:
            player.stopped = True
        elif player.score > 21:
            player.broken = True

    def _target_phase(self, player: 'Player', deck: 'Deck', phase: 'GamePhase') -> GamePhase:
        if player.score == 21:
            return GamePhase.HOUSE_PHASE
        if player.broken:
            return GamePhase.HOUSE_PHASE
        return GamePhase.PLAYER_PHASE

    def __str__(self):
        execution_tag = "" if not self.is_executed else "(E) "
        return "{}RequestCardAction".format(execution_tag)
