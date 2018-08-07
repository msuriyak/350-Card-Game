from deck import Deck, Stack, Hand, Card, Suits, Card_values

# Number of allowed players : 4 - 17
removal_cards = [
    Card(2, 'Clubs'), 
    Card(2, 'Diamonds'), 
    Card(2, 'Hearts'),
    Card(2, 'Spades'),
    Card(3, 'Clubs'), 
    Card(3, 'Diamonds'), 
    Card(3, 'Hearts'),
    Card(4, 'Clubs'),
    Card(4, 'Clubs'), 
    Card(4, 'Diamonds'), 
    Card(4, 'Hearts')
    ]

class Game(object):

    def __init__(self, num_players):
        self._num_players = num_players
        num_deck_cards, num_cards, num_exclusion = self.calc_num_cards()
        self._num_deck_cards = int(num_deck_cards)
        self._num_cards = int(num_cards)
        self._num_exclusion = int(num_exclusion)

        self._decks = Deck(num_deck_cards, nec_exl=removal_cards[:num_exclusion])

    @property
    def num_cards(self):
        return self._num_cards

    @property
    def num_players(self):
        return self._num_players

    @property
    def num_deck_cards(self):
        return self._num_deck_cards

    @property
    def num_rounds(self):
        return self._num_rounds

    @property
    def num_exclusion(self):
        return self._num_exclusion

    def calc_num_cards(self):
        return 52 - 52%self.num_players, 52//self.num_players, 52%self.num_players

    def create_round(self, round_id):
        flag = 1
        while flag==1:
            flag = 0
            player_stacks = [Stack(cards).sort_stack() for cards in self._decks.distribute_deck(self.num_players)]

            for stack in player_stacks:
                if stack.calc_points() == 0:
                    flag = 1
                    break
        return player_stacks

if __name__ == '__main__':
    print('Running main!!')