from enum import Enum


class GamePhase(Enum):

    PLAYER_PHASE = 0  # player turn phase, player executes actions
    HOUSE_PHASE = 1  # house turn phase, house executes actions
