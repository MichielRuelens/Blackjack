# Suits
HEARTS = "hearts"
DIAMONDS = "diamonds"
SPADES = "spades"
CLUBS = "clubs"


#: an array with all the possible suit strings
POSSIBLE_SUIT = [HEARTS, DIAMONDS, SPADES, CLUBS]

#: an array with the possible ranks
POSSIBLE_RANK = range(1, 14, 1)

#: a string representing the Joker's suit
JOKER_SUIT = 'joker'

#: a number representing the Joker's rank
JOKER_RANK = 0

#: a dictionary which translates the special face cards to strings
RANK_TRANSLATION = {
    1: 'ace',
    11: 'jack',
    12: 'queen',
    13: 'king',
}

RANK_TRANSLATION_SHORT = {
    1: 'A',
    11: 'J',
    12: 'Q',
    13: 'K',
}
