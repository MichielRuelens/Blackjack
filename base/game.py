from functools import partial
from typing import List, Optional

from ai.model_configs.mlp_config import MLPConfig
from base.cards.deck import Deck
from base.constants import Constants
from base.enums.game_phase import GamePhase
from base.game_state import GameState
from base.players.ai_player import AIPlayer
from base.players.human_player import HumanPlayer
from base.players.player import Player
from base.players.random_player import RandomPlayer


class Game:

    def __init__(self):
        self.deck = None  # type: Optional[Deck]
        self.player = None  # type: Optional[Player]
        self.phase = None  # type: Optional[GamePhase]
        self.initialized = False

    def reset_game(self, initialize: bool = True, keep_players: bool = False) -> None:
        """
        Reset the current game.

        :param initialize: if True, re-initialize the game after the reset
        :param keep_players: if True, don't delete the player objects (can be useful for keeping AI models loaded)
                             Note that hands are cleared even when the players are kept.
        """
        self.phase = None
        self.deck = None
        if not keep_players:
            self.player = None  # type: Optional[List[Player]]
        else:
            # We're not killing the players, but they have to be reset (e.g. score set to 0)
            self.player.reset()
        self.initialized = False
        if initialize:
            self.initialize_game(initialize_players=not keep_players)

    def initialize_game(self, initialize_players: bool = True):
        if not self.initialized:
            # Set up game phase
            self.phase = GamePhase.PLAYER_PHASE
            # Initialize players
            if initialize_players:
                self._initialize_players()
            # Create new deck
            self.deck = self._create_deck()
            self.initialized = True

    def play_single_step(self, verbose: bool = False):
        """Play a single action in the game."""
        if not self.initialized:
            raise Exception("Game not initialized")
        if not self.is_finished():
            if verbose:
                self.print()
            game_phase = self.player.play_single_step(self.get_state(), verbose=verbose)
            self.phase = game_phase

    def get_state(self) -> GameState:
        """Return the current GameState of this Board."""
        return GameState(self.phase, self.deck, self.player)

    def is_finished(self) -> bool:
        """
        Return True if the game is finished.

        The game is finished when one of the players has no cards left and there are no more cards in the deck.
        """
        return self.player.stopped or self.player.broken

    def _initialize_players(self) -> None:
        type_to_cls = {
            "random": RandomPlayer,
            "ai": partial(AIPlayer, config=MLPConfig()),
            "human": HumanPlayer
        }
        self.player = type_to_cls.get(Constants.PLAYER_TYPE)()

    @staticmethod
    def _create_deck() -> Deck:
        deck = Deck(with_jokers=False)
        deck.shuffle()
        return deck

    def print(self):
        print(self.player)

    def player_won(self):
        return self.player.stopped and self.player.score <= 21
