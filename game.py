from deck import Deck, Stack, Hand, Card, Suits, Card_values
import random

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

class Player(object):
    def __init__(self):
        self.stack = None
        self.hands = []
        self.points = 0

    def set_stack(self, stack):
        self.stack = stack

    # primary simulation plays random card
    # AI will be built later
    def play_card(self, suit, trump=None): 
        if suit != None:
            if self.stack.check_suit(suit):
                suit_cards = self.stack.suit_cards(suit)
                card_played = suit_cards[random.randint(0, len(suit_cards) - 1)]
                self.stack.pop_card(card_played)
                return card_played
            else:
                if trump == None:
                    return 'Open Trump!' 
                if self.stack.check_suit(trump):
                    trump_cards = self.stack.suit_cards(trump)
                    card_played = trump_cards[random.randint(0, len(trump_cards) - 1)]
                    self.stack.pop_card(card_played)
                    return card_played
                else:
                    card_played = self.stack.cards[random.randint(0, self.stack.num_cards - 1)]
                    self.stack.pop_card(card_played)
                    return card_played
        else:
            card_played = self.stack.cards[random.randint(0, self.stack.num_cards - 1)]
            self.stack.pop_card(card_played)
            return card_played
    
    def calc_points(self):
        points = 0
        for hand in self.hands:
            points = points + hand.calc_points()
        self.points = points
        return points

class Game(object):
    def __init__(self, num_players):
        self._num_players = num_players
        num_deck_cards, cards_per_player, num_exclusion = self.calc_num_cards()
        self._num_deck_cards = int(num_deck_cards)
        self._cards_per_player = int(cards_per_player)
        self._num_exclusion = int(num_exclusion)
        self.players = [Player() for _ in range(num_players)]

        self._decks = Deck(num_deck_cards, nec_exl=removal_cards[:num_exclusion])

    @property
    def cards_per_player(self):
        return self._cards_per_player

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

        for i, stack in enumerate(player_stacks):
            self.players[i].set_stack(stack)

    # Will have to be changed
    def play_game(self, num_games=1):
        for rounds in range(num_games):
            self.create_round(rounds)
            
            # for count, player in enumerate(self.players): # remove
            #     print("Player " + str(count) + " stack : " + str(player.stack)) # remove
            
            winner = 0
            trump = Suits[random.randint(0, len(Suits) - 1)]
            trump_open = False

            print("Trump is : " + trump) # remove
            
            for i in range(self.cards_per_player) :
                curr_hand = []
                suit = None
                for j in range(self.num_players):
                    if trump_open:
                        card = self.players[(winner + j)%self.num_players].play_card(suit, trump)
                        curr_hand.append(card)
                    else:
                        card = self.players[(winner + j)%self.num_players].play_card(suit)
                        if type(card) != Card:
                            trump_open = True
                            print("Trump is open") # remove
                            card = self.players[(winner + j)%self.num_players].play_card(suit, trump)
                        curr_hand.append(card)
                    if j==0:
                        suit = card.suit
                
                winner_old = winner
                if trump_open:
                    winner, _ = Hand(curr_hand, trump).find_winner()
                else:
                    winner, _ = Hand(curr_hand).find_winner()
                winner = (winner + winner_old)%self.num_players
                self.players[winner].hands.append(Hand(curr_hand))

                print(str(winner) + " - " + str(Hand(curr_hand).calc_points()) + " :: " + str(Hand(curr_hand))) # remove
                        
            s = 0 # remove
            for k, player in enumerate(self.players): # remove
                s = s + player.calc_points() # remove
                print("Player " + str(k) + " : " + str(player.calc_points())) # remove
            print("Total points : " + str(s)) # remove

if __name__ == '__main__':
    print('Running main!!')
    curr_game = Game(6)
    curr_game.play_game(1)