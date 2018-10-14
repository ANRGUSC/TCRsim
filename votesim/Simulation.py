import numpy as np
import random
from Voter import Voter
from Item import Item
from TCR import TCR
from copy import copy
# import matplotlib.pyplot as plt


NUM_ITEMS = 100
NUM_VOTERS = 20
DEFAULT_TOKENS = 10

STAKE_POOL: float = 0.0
TOTAL_TOKENS = NUM_VOTERS * DEFAULT_TOKENS

ALPHA = .25
BETA = .25
GAMMA = .25
THETA = .25

DELTA = 0.05

STAKE_I = 0.5  # should stake increase in proportion to how many total tokens are available?
STAKE = 0.5

P_VE = .9
P_VD = .4
P_VCI = .8
P_VCU = .5


def set_vote(voter, item):
    global STAKE_POOL
    p_vote = random.random()
    if (voter.is_engaged() and P_VE > p_vote) or (not voter.is_engaged() and P_VD > p_vote):
        voter.set_tokens(voter.get_tokens() - STAKE)
        STAKE_POOL += STAKE
        p_correct = random.random()
        if (voter.is_informed() and P_VCI > p_correct) or (not voter.is_informed() and P_VCU > p_correct):
            voter.set_vote(item.is_valid())  # set vote to correct vote
        else:
            voter.set_vote(not item.is_valid())  # else sets vote to incorrect vote

    return voter


def write_file(tcr_array, item_array, vote_results):
    f = open("demofile.txt", "w")
    f.write("TCR Val\tValid\tAccept\t\t")
    for i in range(NUM_VOTERS):
        f.write("V" + str(i + 1) + "\t")
    f.write("\n")
    for i in range(NUM_ITEMS):
        f.write("%.2f" % tcr_array[i].get_tcr_value() + "\t" + str(item_array[i].is_valid())
                + "\t" + str(item_array[i].is_accepted()) + "\t\t")
        for j in range(NUM_VOTERS):
            f.write("%.2f" % vote_results[i, j].get_tokens() + "\t")
        f.write("\n")


def generate_plot(vote_results):
    # create 4 different arrays for informed-engaged, uninformed-engaged, informed-unengaged, uninformed-unengaged
    # average?
    arr_informed_engaged = np.zeros(NUM_ITEMS, dtype=float)
    arr_uninformed_engaged = np.zeros(NUM_ITEMS, dtype=float)
    arr_informed_unengaged = np.zeros(NUM_ITEMS, dtype=float)
    arr_uninformed_unengaged = np.zeros(NUM_ITEMS, dtype=float)

    num_informed_engaged = 0
    num_uninformed_engaged = 0
    num_informed_unengaged = 0
    num_uninformed_unengaged = 0
    for i in range(NUM_VOTERS):
        voter = vote_results[0, i]
        if voter.is_informed() and voter.is_engaged():
            num_informed_engaged += 1
        elif voter.is_informed() and not voter.is_engaged():
            num_informed_unengaged += 1
        elif not voter.is_informed() and voter.is_engaged():
            num_uninformed_engaged += 1
        elif not voter.is_informed() and not voter.is_engaged():
            num_uninformed_unengaged += 1

    for i in range(NUM_ITEMS):
        for j in range(NUM_VOTERS):
            voter = vote_results[i, j]
            if voter.is_informed() and voter.is_engaged():
                arr_informed_engaged[i] += voter.get_tokens()
            elif voter.is_informed() and not voter.is_engaged():
                arr_informed_unengaged += voter.get_tokens()
            elif not voter.is_informed() and voter.is_engaged():
                arr_uninformed_engaged += voter.get_tokens()
            elif not voter.is_informed() and not voter.is_engaged():
                arr_uninformed_unengaged += voter.get_tokens()
        arr_informed_engaged[i] /= num_informed_engaged
        arr_informed_unengaged[i] /= num_informed_unengaged
        arr_uninformed_engaged[i] /= num_uninformed_engaged
        arr_uninformed_unengaged[i] /= num_uninformed_unengaged

    # labels = ["informed-engaged ", "informed-unengaged", "uninformed-engaged", "uninformed-unengaged"]
    # plot = np.stack(arr_informed_engaged, arr_informed_unengaged, arr_uninformed_engaged, arr_uninformed_unengaged)
    # fig, ax = plt.subplots()
    # ax.stackplot(y1, y2, y3, labels=labels)
    # ax.legend(loc='upper left')
    # plt.show()


def main():
    global TOTAL_TOKENS
    global STAKE
    vote_results = np.empty((NUM_ITEMS, NUM_VOTERS), dtype=Voter)
    item_array = np.array([Item() for _ in range(NUM_ITEMS)])
    tcr_array = np.empty(NUM_ITEMS, dtype=TCR)

    for i in range(NUM_ITEMS):
        accepted_votes = 0
        rejected_votes = 0
        item = Item()

        for j in range(NUM_VOTERS):
            if i == 0:
                vote_results[i, j] = set_vote(Voter(DEFAULT_TOKENS), item)
            else:
                v = copy(vote_results[i - 1, j])
                vote_results[i, j] = set_vote(v, item)

            if vote_results[i, j].get_vote() is True:
                accepted_votes += 1
            elif vote_results[i, j].get_vote() is False:
                rejected_votes += 1

        if accepted_votes > rejected_votes:
            # if num of accepted votes is greater than the majority (0.5) then set the item to be accepted
            item.set_acceptance(True)
            num_majority = accepted_votes
        else:
            item.set_acceptance(False)
            num_majority = rejected_votes
        item_array[i] = item

        TOTAL_TOKENS = (1 + DELTA) * TOTAL_TOKENS
        tcr_array[i] = TCR(TOTAL_TOKENS)

        for j in range(NUM_VOTERS):
            voter = vote_results[i, j]
            num_stake_majority_tokens = STAKE / num_majority
            num_inflation_tokens = (TOTAL_TOKENS - (TOTAL_TOKENS / (1 + DELTA))) / (accepted_votes + rejected_votes)

            if voter.get_vote() is not None:
                if item_array[i].is_accepted() == voter.get_vote():
                    # if voter voted correctly, give stake value back
                    voter.set_tokens(voter.get_tokens() + num_stake_majority_tokens)

                # every voter gets total tokens * delta tokens
                voter.set_tokens(voter.get_tokens() + num_inflation_tokens)

        STAKE = STAKE_I / (NUM_VOTERS * DEFAULT_TOKENS) * TOTAL_TOKENS

    for i in range(NUM_ITEMS):
        if i is not 0:
            tcr = tcr_array[i - 1]
        else:
            tcr = tcr_array[i]

        tcr_array[i] = copy(tcr)
        item = item_array[i]
        if item.is_valid() and item.is_accepted():
            tcr_array[i].set_tcr_value(1, 0, 0, 0)
        elif item.is_valid() and not item.is_accepted():
            tcr_array[i].set_tcr_value(0, 0, 0, 1)
        elif not item.is_valid() and item.is_accepted():
            tcr_array[i].set_tcr_value(0, 0, 1, 0)
        elif not item.is_valid() and not item.is_accepted():
            tcr_array[i].set_tcr_value(0, 1, 0, 0)

    write_file(tcr_array, item_array, vote_results)
    generate_plot(vote_results)

main()
