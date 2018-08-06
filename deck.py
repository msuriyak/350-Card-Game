Card_values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
Suits = ['Spades', 'Hearts', 'Diamonds', 'Clubs']

DEF_RANKS = {
    'Ace' : 13,
    'King' : 12, 
    'Queen' : 11,
    'Jack' : 10,
    '10' : 9, 
    '9' : 8,
    '8' : 7,
    '7' : 6, 
    '6' : 5,
    '5' : 4,
    '4' : 3,
    '3' : 2,
    '2' : 1
    }

class Card(object):

    def __init__(self, value, suit, ranks=DEF_RANKS):
        self._ranks = ranks
        if value in Card_values:
            self._value = value
        elif value in list(range(2, 11)):
            self._value = repr(value)
        else:
            raise ValueError(str(value) + " is not a valid value for a standard 52 card deck. Allowed values are : " + Card_values)
        
        if suit in Suits:    
            self._suit = suit
        else:
            raise ValueError('Give suit ' + suit + ' not a valid suit. Allowed suits are : ' + suits)        

    @property    
    def value(self):
        return self._value

    @property
    def suit(self):
        return self._suit

    def __eq__(x, y):
        return x.value, x.suit == y.value, y.suit

    def __ne__(x, y):
        return not (x == y)

    def __hash__(self):
        return hash((self.value, self.suit))

    def __repr__(self):
        return str(self.value) + ' of ' + str(self.suit)

    def __gt__(x, y):
        if x.suit == y.suit:
            if x._ranks[x.value] > x._ranks[y.value]:
                return True
            return False
        raise ValueError("Cards with different suits cannot be compared!!")

    def __lt__(x, y):
        if x.suit == y.suit:
            if x._ranks[x.value] < x._ranks[y.value]:
                return True
            return False
        raise ValueError("Cards with different suits cannot be compared!!")

class Hand(object):

    def __init__(self, cards, trump=None):
        self._cards = cards
        self._trump = trump

    @property
    def cards(self):
        return self._cards

    @property
    def trump(self):
        return self._trump

    def find_winner(self):
        curr_suit = self.cards[0].suit
        winner = (0, self.cards[0])
        for i, card in enumerate(self.cards[1:]):
            try:
                if self.trump != "Double Joker":
                    if card > winner[1]:
                        winner = (i+1, card)
                else:
                    if card.suit == self.cards[0].suit:
                        if card < winner[1]:
                            winner = (i+1, card)

            except ValueError:
                if self.trump != None:
                    if card.suit == self.trump:
                        winner = (i+1, card) 
        return winner

class Stack(object):

    def __init__(self, cards):
        self._cards = cards
        self._num_cards = len(cards)

    @property
    def cards(self):
        return self._cards

    @property
    def num_cards(self):
        return self._num_cards

    def sort_stack(self):
        return sorted(self._cards, key=lambda card: (card.suit, DEF_RANKS[card.value])) # Hard coded look into it

    def check_suit(self, suit):
        for card in self._cards:
            if card.suit == suit:
                return True
        return False

    def pop_card(self, card):
        if card not in self.cards:
            raise ValueError("Given card " + str(card) + " does not exist in the stack!!")

        self._cards = list(set(self._cards) - set([card]))
        self._num_cards = self._num_cards - 1

    def suit_cards(self, suit):
        result = []
        for card in self._cards:
            if card.suit == suit:
                result.append(card)

        return result

class Deck(object):
    
    def __init__(self, num_cards, nec_inc=None, nec_exl=None, ranks=DEF_RANKS):
        self._ranks = ranks
        self._num_cards = num_cards
        self.deck = []

        cards_set = set([Card(value, suit, ranks) for suit in Suits for value in Card_values])

        if ranks == DEF_RANKS:
            if nec_exl != None:
                num_exl = len(nec_exl)
                if type(nec_exl) == list:
                    for card in nec_exl:
                        cards_set = cards_set - set([card])
                else:
                    num_exl = 1
                    cards_set = cards_set - nec_exl            
            
            if nec_inc != None:
                num_inc = len(nec_inc)
                if type(nec_inc) == list:
                    for card in nec_inc:
                        self.deck.append(card)
                        cards_set = cards_set - set([card])
                else:
                    num_inc = 1
                    self.deck.append(nec_inc)
                    cards_set = cards_set - nec_inc
            else:
                num_inc = 0

            self.deck = self.deck + sorted(list(cards_set), key=lambda card: ranks[card.value], reverse=True)[:num_cards - num_inc]

        else:
            raise ValueError("Given ranks not defined!!")
        self.sort_deck()

    def sort_deck(self):
        self.deck = sorted(self.deck, key=lambda card: (card.suit, self._ranks[card.value]), reverse=True)

    def shuffle_deck(self):
        from random import shuffle
        return shuffle(self.deck)

    def distribute_deck(self, num_stacks):
        if self._num_cards % num_stacks == 0:
            cards_per_stack = self._num_cards / num_stacks
            self.shuffle_deck()
            return [self.deck[i*cards_per_stack : (i+1)*cards_per_stack] for i in range(num_stacks)]

    def __repr__(self):
        out = ''
        for card in self.deck:
            out = out + str(card) + '\n'
        return out

if __name__ == '__main__':
    print("Running main!!")