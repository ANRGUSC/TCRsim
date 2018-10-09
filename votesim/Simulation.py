import numpy as np
import random
from Voter import Voter
from Item import Item
from Token import Token

NUM_ITEMS = 100
NUM_VOTERS = 20
# TCR_VALUE =
DEFAULT_TOKENS = 10

THRESHOLD = 0.8

ALPHA = .25
BETA = .25
GAMMA = .25
THETA = .25

DELTA = 1.03

STAKE = 0.5

P_VE = .9
P_VD = .4
P_VI = .8
P_VU = .5


def set_voter(voter):
    voter.set_tokens(voter.get_tokens() - STAKE)

    if voter.is_engaged() and voter.is_informed():
        p_vote = P_VE * P_VI
    elif not voter.is_engaged() and voter.is_informed():
        p_vote = P_VD * P_VI
    elif voter.is_engaged() and not voter.is_informed():
        p_vote = P_VE * P_VU
    else:
        p_vote = P_VD * P_VU

    if p_vote > random.random(): # if probability of this voter voting correct > random # then vote yes
        voter.set_vote(True)
        voter.set_tokens(voter.get_tokens() + STAKE)
    else:
        voter.set_vote(False)

    voter.set_tokens(voter.get_tokens() * DELTA)

    return voter


def main():
    vote_results = np.empty((NUM_ITEMS, NUM_VOTERS), dtype=Voter)
    items = np.array([Item() for _ in range(NUM_ITEMS)])
    tokens = np.array([Token() for _ in range(NUM_ITEMS)])

    for i in range(NUM_ITEMS):
        total_tokens = 0
        approved_votes = 0

        for j in range(NUM_VOTERS):
            if i == 0:
                vote_results[i, j] = set_voter(Voter(DEFAULT_TOKENS))
            else:
                v = vote_results[i - 1, j]
                vote_results[i, j] = set_voter(v)

            total_tokens += + vote_results[i, j].get_tokens()
            if vote_results[i, j].get_vote():
                approved_votes += 1

        if approved_votes >= THRESHOLD:
            items[i] = Item(True)
        else:
            items[i] = Item(False)

        '''
            tokenValue = TCRValue / numTotalTokens
            voterFunds = numTokensHeld * tokenValue
        '''
        value =
        if items[i].is_valid() and items[i].is_approved():
            tokens[i] = Token(total_tokens)

            print(vote_results[i, j].get_tokens())



main()