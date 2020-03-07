from typing import List, TYPE_CHECKING, Union

import numpy as np

from base.cards.card_encoder import CardEncoder
from base.cards.deck import Deck
from base.enums.game_phase import GamePhase

if TYPE_CHECKING:
    from base.players.player import Player


class GameState:
    """
    The full current state of the game.
    The game state contains all necessary information for a player to determine the next action.
    """

    SIZE = 56  # Total number of integers required to represent the game state

    def __init__(self, phase: GamePhase, deck: Deck, player: 'Player'):
        self.phase = phase
        self.deck = deck
        self.player = player

    def create_numeral_representation(self, player: 'Player', as_array: bool = True) -> Union[List[int], np.array]:
        """
        Create a numerical representation of (a subset of) the game state for the specified player.

        This representation only contains information that is accessible to the specified player.
        """
        representation = []
        representation.extend(self._hand_representation(player=player))
        representation.extend(self._score_representation(player=player))
        if as_array:
            representation = np.array(representation, dtype=np.float32)
        return representation

    @staticmethod
    def _hand_representation(player: 'Player'):
        return list(CardEncoder().encode(player.hand.get_raw_cards()))

    @staticmethod
    def _score_representation(player: 'Player'):
        return [player.score]

    @staticmethod
    def _diff_representation(player: 'Player'):
        return [abs(21 - player.score)]
