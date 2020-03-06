from typing import List, Optional

from base.cards.card import Card
from base.cards.card_set import CardSet


class Stack(CardSet):

    def description(self) -> str:
        return "Stack"

    def look(self) -> Optional[Card]:
        """
        Return the top card on the stack.

        This is the only card visible to the players.
        """
        return self._cards[-1] if self._cards else None

    def put(self, card: Card):
        self._cards.append(card)

    def grab(self) -> List[Card]:
        cards = self._cards
        self._clear()
        return cards

    def _clear(self):
        self._cards = []
