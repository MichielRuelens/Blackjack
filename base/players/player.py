from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING

from base.cards.hand import Hand
from base.enums.game_phase import GamePhase

if TYPE_CHECKING:
    from base.game_state import GameState
    from base.actions.action import Action


class Player(metaclass=ABCMeta):

    def __init__(self):
        self.hand = Hand()  # type: Hand
        self.broken = False
        self.stopped = False

    @property
    @abstractmethod
    def is_human(self):
        raise NotImplementedError

    @property
    def score(self) -> float:
        return sum([card.get_rank() for card in self.hand])

    @abstractmethod
    def _choose_action(self, game_state: 'GameState', verbose: bool = False) -> 'Action':
        """
        Return an action to take given the current GameState.

        The chosen action must be an eligible one given the current state, invalid actions will result in an Exception.
        A valid series of actions will always result in a END_TURN_PHASE game phase which ends the players turn.
        """
        raise NotImplementedError

    def reset(self):
        self.hand = Hand()
        self.stopped = False
        self.broken = False

    def play_single_step(self, game_state: 'GameState', verbose: bool = False) -> GamePhase:
        """
        Play a single move based on the given GameState.

        :param game_state: the current state of the game
        :param verbose: if True, print extra information to the console
        :return: the action taken by the player
        """
        action = self._choose_action(game_state, verbose=verbose)
        if verbose:
            print("Executing {}".format(action))
        new_phase = action.execute(self, game_state.deck, game_state.phase)
        return new_phase

    def num_cards(self) -> int:
        return self.hand.num_cards()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        broken = "- broken" if self.broken else ""
        stopped = "- stopped" if self.stopped else ""
        print_str = "Player - {} {}{}\n".format(self.score, broken, stopped)
        print_str += str(self.hand)
        return print_str
