#!/usr/bin/python
"""This module provides the :class:`Deck` object
"""

import logging
import random
#: a logger object
from typing import List

from base.cards.card import Card
from base.utils.card_constants import JOKER_RANK, JOKER_SUIT, POSSIBLE_RANK, POSSIBLE_SUIT

LOGGER = logging.getLogger(__name__)


class Deck(object):
    """A Deck object
    A new deck starts out ordered.
    If jokers are included, contains (2 + 4 * 13) :class:`deck_of_cards.card.Card` objects
    If no jokers are included, contains (4 * 13) :class:`deck_of_cards.card.Card` objects
    """

    #: a boolean to represent if jokers exist in deck
    _with_jokers = True

    #: an array of unused :class:`deck_of_cards.card.Card` objects that are
    #: waiting to be dealt
    _cards = []

    #: an array of :class:`deck_of_cards.card.Card` objects that have been dealt
    _in_play_cards = []

    def __init__(self, with_jokers=True):
        """
        :param bool with_jokers: include jokers if True
        """
        LOGGER.debug("Creating a new deck (with_jokers:%s)", with_jokers)

        self._num_added_cards = 0  # Keep track of how many cards are added to the deck after creation
        self._with_jokers = with_jokers
        self._cards = []
        self._in_play_cards = []

        # add jokers if necessary
        if with_jokers:
            for _ in range(2):
                self._cards.append(Card(JOKER_RANK, JOKER_SUIT))

        for suit in POSSIBLE_SUIT:
            for rank in POSSIBLE_RANK:
                self._cards.append(Card(rank, suit))

    def add_cards(self, cards: List[Card]) -> None:
        self._cards.extend(cards)
        self._num_added_cards += len(cards)

    def __repr__(self):
        """
        :returns: unambigious string represenation of deck object
        :rtype: str
        """
        card_arrays_dict = {
            '_cards': self._cards,
            '_in_play_cards': self._in_play_cards,
        }

        repr_str = 'Deck('

        for card_array_str, card_array in card_arrays_dict.items():
            repr_str += "%s=[" % card_array_str
            if card_array:
                for c_card in card_array:
                    repr_str += repr(c_card) + ', '
                repr_str = repr_str[:-2]
            repr_str += '], '

        repr_str = repr_str[:-2] + ')'

        return repr_str

    def __str__(self):
        """
        :returns: human readable string represenation of deck object
        :rtype: str
        """
        card_arrays_dict = {
            '_cards': self._cards,
            '_in_play_cards': self._in_play_cards,
        }

        str_str = "Deck(\n\t"

        for card_array_str, card_array in card_arrays_dict.items():
            str_str += "%s : [" % card_array_str
            if card_array:
                for c_card in card_array:
                    str_str += str(c_card) + ', '
                str_str = str_str[:-2]
            str_str += '],\n\t'

        str_str = str_str[:-3] + "\n)"

        return str_str

    def num_cards(self) -> int:
        return len(self._cards)

    def shuffle(self):
        """Shuffle the unused set of cards in :attr:`_cards`
        """
        LOGGER.debug("Shuffling deck")
        random.shuffle(self._cards)

    def deal(self):
        """Deals a single :class:`deck_of_cards.card.Card` from :attr:`_cards`
        Raises an IndexError when :attr:`_cards` is empty
        :returns: a single :class:`deck_of_cards.card.Card`
        :rtype: :class:`deck_of_cards.card.Card`
        :raises: IndexError
        """
        LOGGER.debug("Number of cards left : %d", len(self._cards))

        try:
            # deal the last card from the unused _cards array
            deal_card = self._cards.pop()
        except IndexError:
            raise IndexError('Trying to deal from an empty deck.')

        # add the newly dealt card to the _in_play_cards array
        self._in_play_cards.append(deal_card)

        LOGGER.info("Dealing : %s", deal_card)
        return deal_card

    def deal_n(self, n: int) -> List[Card]:
        """Deal N times."""
        cards = []
        for _ in range(n):
            cards.append(self.deal())
        return cards

    def is_empty(self):
        """This method returns true if the deck(:attr:`_cards`) is empty
        :returns: True if deck is empty
        :rtype: bool
        """
        return not self._cards

    def check_deck(self):
        """Check to make sure all the cards are accounted
        :returns: True if all cards are accounted
        :rtype: bool
        """

        # start with a simple card count check
        total_possible_cards = (13*4) + (2 if self._with_jokers else 0) + self._num_added_cards
        if total_possible_cards != (len(self._cards)
                                    + len(self._in_play_cards)):
            return False

        return_value = True

        # go through all piles of cards and create a dictionary with
        # [suit][rank] = number of occurrences of card
        card_dict = {}
        for pile in [self._cards, self._in_play_cards]:
            for c_card in pile:
                suit = c_card.get_suit()
                rank = c_card.get_rank()

                if suit not in card_dict:
                    card_dict[suit] = {}

                if rank not in card_dict[suit]:
                    card_dict[suit][rank] = 1
                else:
                    card_dict[suit][rank] += 1

        # Don't do this check if we've manually added extra cards to the deck, as this will no longer work in that case
        if self._num_added_cards == 0:
            # go through generated card_dictionary to make sure that there are the
            # appropriate rank of occurrences for each card
            for suit in card_dict.keys():
                for rank in card_dict[suit].keys():
                    if 2 == card_dict[suit][rank]:
                        # check for 2 jokers
                        if not (JOKER_SUIT == suit and JOKER_RANK == rank):
                            return_value = False
                    elif 1 != card_dict[suit][rank]:
                        LOGGER.info("Something is wrong with the %s", Card(rank, suit))
                        return_value = False
        return return_value
