from base.actions.action import Action
from base.game_state import GameState
from base.players.player import Player


class ControlledPlayer(Player):

    @property
    def is_human(self):
        return False

    def _choose_action(self, game_state: 'GameState', verbose: bool = False) -> 'Action':
        raise NotImplemented("Controlled players need action determination from the outside.")

    def play_action(self, game_state: 'GameState', action: Action):
        action.execute(self, game_state.deck, game_state.phase)
