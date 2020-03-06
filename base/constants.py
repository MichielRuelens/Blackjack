from collections import defaultdict


class Constants:

    NUM_CARDS_IN_STARTING_HAND = 11
    NUM_PLAYERS = 2
    PLAYER_TYPE = "human"

    GAME_ID_LENGTH = 20

    rewards = defaultdict(lambda: 1)
    rewards[21] = 150
    rewards[20] = 70
    rewards[19] = 50
    rewards[18] = 20
    rewards[17] = 10
    rewards[16] = 5
    rewards[15] = 3
    rewards[14] = 2
