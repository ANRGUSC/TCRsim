import numpy as np
import random
from Voter import Voter
from Item import Item
from TCR import TCR
from copy import copy
import matplotlib.pyplot as plt
from Tkinter import *



class Simulation():
    def __init__(self):
        self.__numItems = 100
        self.__numVoters = 20
        self.__defaultTokens = 10

        self.__stakePool = 0.0
        self.__totalTokens = self.__numVoters * self.__defaultTokens

        self.__alpha = .25
        self.__beta = .25
        self.__gamma = .25
        self.__theta = .25

        self.__delta = 0.04

        self.__initialStake = 0.5  # should self.__stake increase in proportion to how many total tokens are available?
        self.__stake = 0.5

        self.__pVE = .9
        self.__pVD = .1
        self.__pVCI = .8
        self.__pVCU = .1

    def parse_input(self):
        print('parsing')

    def get_input(self):
        numVoters = 0
        while numVoters < 10:
            numVoters = input("Enter number of voters ( > 10 ): ")
        self.__numVoters = numVoters

        numItems = 0
        while numItems < 10:
            numItems = input("Enter number of items ( > 10 ): ")
        self.__numItems = numItems


    def set_vote(self, voter, item):
        p_vote = random.random()
        if (voter.is_engaged() and self.__pVE > p_vote) or (not voter.is_engaged() and self.__pVD > p_vote):
            voter.set_tokens(voter.get_tokens() - self.__stake)
            self.__stakePool += self.__stake
            p_correct = random.random()
            if (voter.is_informed() and self.__pVCI > p_correct) or (not voter.is_informed() and self.__pVCU > p_correct):
                voter.set_vote(item.is_valid())  # set vote to correct vote
            else:
                voter.set_vote(not item.is_valid())  # else sets vote to incorrect vote
        return voter


    def write_file(self, tcr_array, item_array, vote_results):
        f = open("output.txt", "w")
        f.write("TCR Val\tValid\tAccept\t\t")
        for i in range(self.__numVoters):
            f.write("V" + str(i + 1) + "\t")
        f.write("\n")
        for i in range(self.__numItems):
            f.write("%.2f" % tcr_array[i].get_tcr_value() + "\t" + str(item_array[i].is_valid())
                    + "\t" + str(item_array[i].is_accepted()) + "\t\t")
            for j in range(self.__numVoters):
                f.write("%.2f" % vote_results[i, j].get_tokens() + "\t")
            f.write("\n")

        f.write("\t\t\t\t")
        for i in range(self.__numVoters):
            if vote_results[0, i].is_engaged():
                f.write("Eng\t")
            else:
                f.write("Uneng\t")
        f.write("\n\t\t\t\t")
        for i in range(self.__numVoters):
            if vote_results[0, i].is_informed():
                f.write("Inf\t")
            else:
                f.write("Uninf\t")
        f.write("\n")


    def generate_plot(self, vote_results):
        # create 4 different arrays for informed-engaged, uninformed-engaged, informed-unengaged, uninformed-unengaged
        # average?
        arr_informed_engaged = np.zeros(self.__numItems, dtype=float)
        arr_uninformed_engaged = np.zeros(self.__numItems, dtype=float)
        arr_informed_unengaged = np.zeros(self.__numItems, dtype=float)
        arr_uninformed_unengaged = np.zeros(self.__numItems, dtype=float)

        num_informed_engaged = 0
        num_uninformed_engaged = 0
        num_informed_unengaged = 0
        num_uninformed_unengaged = 0
        for i in range(self.__numVoters):
            voter = vote_results[0, i]
            if voter.is_informed() and voter.is_engaged():
                num_informed_engaged += 1
            elif voter.is_informed() and not voter.is_engaged():
                num_informed_unengaged += 1
            elif not voter.is_informed() and voter.is_engaged():
                num_uninformed_engaged += 1
            elif not voter.is_informed() and not voter.is_engaged():
                num_uninformed_unengaged += 1

        for i in range(self.__numItems):
            for j in range(self.__numVoters):
                voter = vote_results[i, j]
                if voter.is_informed() and voter.is_engaged():
                    arr_informed_engaged[i] += voter.get_tokens()
                elif voter.is_informed() and not voter.is_engaged():
                    arr_informed_unengaged[i] += voter.get_tokens()
                elif not voter.is_informed() and voter.is_engaged():
                    arr_uninformed_engaged[i] += voter.get_tokens()
                elif not voter.is_informed() and not voter.is_engaged():
                    arr_uninformed_unengaged[i] += voter.get_tokens()
            arr_informed_engaged[i] /= num_informed_engaged
            arr_informed_unengaged[i] /= num_informed_unengaged
            arr_uninformed_engaged[i] /= num_uninformed_engaged
            arr_uninformed_unengaged[i] /= num_uninformed_unengaged

        plt.plot(arr_informed_engaged, label='informed-engaged')
        plt.plot(arr_informed_unengaged, label='informed-unengaged')
        plt.plot(arr_uninformed_engaged, label='uninformed-engaged')
        plt.plot(arr_uninformed_unengaged, label='uninformed-unengaged')
        plt.xlabel('voting round')
        plt.ylabel('Tokens')
        plt.legend()
        plt.show()

    def set_tcr_values(self, tcr_array, item_array):
        for i in range(self.__numItems):
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

    def main(self):
        self.get_input()

        vote_results = np.empty((self.__numItems, self.__numVoters), dtype=type(Voter))
        item_array = np.array([Item() for _ in range(self.__numItems)])
        tcr_array = np.empty(self.__numItems, dtype=type(TCR))

        for i in range(self.__numItems):
            accepted_votes = 0
            rejected_votes = 0
            item = Item()

            for j in range(self.__numVoters):
                if i == 0:
                    vote_results[i, j] = self.set_vote(Voter(self.__defaultTokens), item)
                else:
                    v = copy(vote_results[i - 1, j])
                    v.set_vote(None)
                    vote_results[i, j] = self.set_vote(v, item)

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

            self.__totalTokens = (1 + self.__delta) * self.__totalTokens
            tcr_array[i] = TCR(self.__totalTokens)

            for j in range(self.__numVoters):
                voter = vote_results[i, j]
                num_stake_majority_tokens = self.__stakePool / num_majority
                # print(num_stake_majority_tokens)
                num_inflation_tokens = (self.__totalTokens - (self.__totalTokens / (1 + self.__delta))) / (accepted_votes + rejected_votes)

                if voter.get_vote() is not None:
                    if item_array[i].is_accepted() == voter.get_vote():
                        # if voter voted correctly, give self.__stake value back
                        voter.set_tokens(voter.get_tokens() + num_stake_majority_tokens)

                    # every voter gets total tokens * self.__delta tokens
                    voter.set_tokens(voter.get_tokens() + num_inflation_tokens)
            self.__stake = self.__initialStake / (self.__numVoters * self.__defaultTokens) * self.__totalTokens

        self.set_tcr_values(tcr_array, item_array)

        self.write_file(tcr_array, item_array, vote_results)

        self.generate_plot(vote_results)


simulation = Simulation()
simulation.main()