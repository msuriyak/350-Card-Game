import numpy as np
import scipy

# Number of allowed players : 4 - 13

def num_cards(num_players):
    return 52 - 52%num_players, 52//num_players, 52%num_players

