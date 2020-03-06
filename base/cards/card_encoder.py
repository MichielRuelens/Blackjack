from typing import List, Union, Optional
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer

from base.cards.card import Card
from base.utils.card_constants import POSSIBLE_SUIT, POSSIBLE_RANK, JOKER_SUIT, JOKER_RANK


class CardEncoder:

    def __init__(self):
        classes = [None]                                                                    # empty set of cards
        classes += [Card(rank, suit) for suit in POSSIBLE_SUIT for rank in POSSIBLE_RANK]   # individual cards
        classes += [Card(JOKER_RANK, JOKER_SUIT)]                                           # joker
        self.encoder = MultiLabelBinarizer(classes=classes)

    def encode(self, cards: Union[Optional[Card], List[Card]]) -> np.ndarray:
        if cards is None or isinstance(cards, Card):
            cards = [cards]
        return self.encoder.fit_transform([cards])[0]
