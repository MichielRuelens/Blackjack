from abc import ABCMeta, abstractmethod
from numbers import Number
from typing import TYPE_CHECKING

from base.enums.game_phase import GamePhase

if TYPE_CHECKING:
    from base.cards.deck import Deck
    from base.players.player import Player


class Action(metaclass=ABCMeta):

    def __init__(self):
        super().__init__()
        self.is_executed = False

    @abstractmethod
    def _key(self):
        """Return a tuple of all fields that should be checked in equality and hashing operations."""
        raise NotImplementedError

    @abstractmethod
    def validate(self, player: 'Player', deck: 'Deck', phase: 'GamePhase', verbose: bool = False):
        raise NotImplementedError

    @abstractmethod
    def _execute(self, player: 'Player', deck: 'Deck', phase: 'GamePhase'):
        raise NotImplementedError

    @abstractmethod
    def _target_phase(self, player: 'Player', deck: 'Deck', phase: 'GamePhase') -> GamePhase:
        raise NotImplementedError

    def get_reward(self) -> Number:
        """Return the reward for this action, assuming the action has already been executed."""
        return 0

    def execute(self, player: 'Player', deck: 'Deck', phase: 'GamePhase') -> GamePhase:
        """Validate this action for the given player and board, execute the action and update the board phase."""
        if self.is_executed:
            raise Exception("Cannot execute the same action twice!")
        if not self.validate(player=player, phase=phase, deck=deck, verbose=True):
            raise Exception("Invalid action. \n {} \n {} \n {} \n {}".format(self, player, phase, deck))
        self._execute(player, deck, phase)
        self.is_executed = True
        return self._target_phase(player, deck, phase)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other) -> bool:
        """Override equality method
        :returns: True if two objects are cards and have the same :attr:`_rank` and :attr:`_suit`
        :rtype: bool
        """
        if type(other) is type(self):
            if self._key() == other._key():
                return True
        return False

    def __ne__(self, other) -> bool:
        """Override inequality method
        :returns: not :attr:`__eq__`
        :rtype: bool
        """
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self._key())
