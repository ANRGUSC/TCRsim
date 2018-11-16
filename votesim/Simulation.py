import numpy as np
import random
from Voter import Voter
from Item import Item
from TCR import TCR
from copy import copy
import matplotlib.pyplot as plt


class Simulation():
    def __init__(self):
        self.__numItems = 50
        self.__numVoters = 100
        self.__defaultTokens = 100.0

        self.__stakePool = 0.0
        self.__totalTokens = 0.0
        self.__totalTokens = self.__numVoters * self.__defaultTokens

        self.__delta = .00

        self.__stake = self.__defaultTokens * .05
        self.__initialStake = self.__stake

        self.__pVE = .8
        self.__pVD = .2
        self.__pVCI = .85
        self.__pVCU = .15

        self.__pEngaged = .5
        self.__pInformed = .1


    def get_input(self):
        x = raw_input("Would you like to input your own variables? (Y/N): ")
        if x == 'Y' or x == 'y':
            numVoters = 0
            while numVoters < 10:
                numVoters = int(input("Enter number of voters ( > 0 ): "))
            self.__numVoters = numVoters

            numItems = 0
            while numItems < 10:
                numItems = int(input("Enter number of items ( > 5 ): "))
            self.__numItems = numItems

            defaultTokens = -1
            while defaultTokens < 0:
                defaultTokens = int(input("Enter number of default tokens each voter starts with ( > 0 ): "))
            self.__defaultTokens = defaultTokens

            pEngaged = -1
            while pEngaged < 0 or pEngaged > 1:
                pEngaged = float(input("Enter probability of a voter being engaged (0 to 1): "))
            self.__pEngaged = pEngaged

            pInformed = -1
            while pInformed < 0 or pInformed > 1:
                pInformed = float(input("Enter probability of voter being informed (0 to 1): "))
            self.__pInformed = pInformed

            pVoteEngaged = -1
            while pVoteEngaged < 0 or pVoteEngaged > 1:
                pVoteEngaged = float(input("Enter probability of voting if engaged (0 to 1): "))
            self.__pVE = pVoteEngaged

            pVoteDisengaged = -1
            while pVoteDisengaged < 0 or pVoteDisengaged > 1:
                pVoteDisengaged = float(input("Enter probability of voting if unengaged (0 to 1): "))
            self.__pVD = pVoteDisengaged

            pVoteCorrectInformed = -1
            while pVoteCorrectInformed < 0 or pVoteCorrectInformed > 1:
                pVoteCorrectInformed = float(input("Enter probability of voter voting correctly if informed (0 to 1): "))
            self.__pVCI = pInformed

            pVoteCorrectUninformed = -1
            while pVoteCorrectUninformed < 0 or pVoteCorrectUninformed > 1:
                pVoteCorrectUninformed = float(input("Enter probability of voter voting correct if uninformed (0 to 1): "))
            self.__pVCU = pVoteCorrectUninformed


    def set_vote(self, voter, item):
        p_vote = random.random()
        if (voter.is_engaged() and self.__pVE > p_vote) or (not voter.is_engaged() and self.__pVD > p_vote):
            stake = self.__stake
            if voter.get_tokens() < self.__stake:
                pass
            self.__stakePool += stake
            voter.set_tokens(voter.get_tokens() - stake)
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
        f.write("Total\n")
        total = 0
        for i in range(self.__numItems):
            f.write("%.2f" % tcr_array[i].get_tcr_value() + "\t" + str(item_array[i].is_valid())
                    + "\t" + str(item_array[i].is_accepted()) + "\t\t")
            for j in range(self.__numVoters):
                total += vote_results[i,j].get_tokens()
                f.write("%.2f" % vote_results[i, j].get_tokens() + "\t")
            f.write(str(total))
            total = 0
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


    def generate_voter_plot(self, vote_results):
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
        plt.plot(arr_informed_unengaged, label='informed-disengaged')
        plt.plot(arr_uninformed_engaged, label='uninformed-engaged')
        plt.plot(arr_uninformed_unengaged, label='uninformed-disengaged')
        plt.xlabel('Voting Round')
        plt.ylabel('Tokens')
        plt.legend(loc = 'upper left')
        plt.savefig('images/token_infm' + str(self.__pInformed)[2] + 'infl' + str(self.__delta)[2:] + '.png')
        plt.show()

    def generate_tcr_plot(self, tcr_array):
        token_values = []
        for tcr in tcr_array:
            token_values.append(tcr.get_tcr_value())
        plt.plot(token_values, label='TCR Value')
        plt.xlabel('Voting Round')
        plt.ylabel('Value')
        plt.legend(loc = 'upper left')
        plt.savefig('images/tcr_infm' + str(self.__pInformed)[2] + 'infl' + str(self.__delta)[2:] + '.png')
        plt.show()


    '''
    wealth of IE class = ( total # of tokens held by IE voters / total # of tokens ) * TCR value

    average wealth of an IE voter = class wealth / # of individuals 
    '''
    def generate_wealth_plot(self, vote_results, tcr_array):
        wealth_ie = np.zeros(self.__numItems, dtype=float)
        wealth_iu = np.zeros(self.__numItems, dtype=float)
        wealth_ue = np.zeros(self.__numItems, dtype=float)
        wealth_uu = np.zeros(self.__numItems, dtype=float)

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
                    wealth_ie[i] += voter.get_tokens()
                elif voter.is_informed() and not voter.is_engaged():
                    wealth_iu[i] += voter.get_tokens()
                elif not voter.is_informed() and voter.is_engaged():
                    wealth_ue[i] += voter.get_tokens()
                elif not voter.is_informed() and not voter.is_engaged():
                    wealth_uu[i] += voter.get_tokens()

            wealth_ie[i] = ( tcr_array[i].get_tcr_value() / tcr_array[i].get_total_tokens() ) * (wealth_ie[i] / num_informed_engaged)
            wealth_iu[i] = ( tcr_array[i].get_tcr_value() / tcr_array[i].get_total_tokens() ) * (wealth_iu[i] / num_informed_unengaged)
            wealth_ue[i] = ( tcr_array[i].get_tcr_value() / tcr_array[i].get_total_tokens() ) * (wealth_ue[i] / num_uninformed_engaged)
            wealth_uu[i] = ( tcr_array[i].get_tcr_value() / tcr_array[i].get_total_tokens() ) * (wealth_uu[i] / num_uninformed_unengaged)
            
        plt.plot(wealth_ie, label='informed-engaged')
        plt.plot(wealth_iu, label='informed-disengaged')
        plt.plot(wealth_ue, label='uninformed-engaged')
        plt.plot(wealth_uu, label='uninformed-disengaged')
        plt.xlabel('Voting Round')
        plt.ylabel('Average Wealth')
        plt.legend(loc = 'upper left')
        plt.savefig('images/wealth_infm' + str(self.__pInformed)[2] + 'infl' + str(self.__delta)[2:] + '.png')
        plt.show()



    def set_tcr_values(self, tcr_array, item_array):
        for i in range(self.__numItems):
            num_tokens = tcr_array[i].get_total_tokens()
            if i is not 0:
                tcr = tcr_array[i - 1]
            else:
                tcr = tcr_array[i]

            tcr_array[i] = copy(tcr)
            tcr_array[i].set_total_tokens(num_tokens)
            
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

        random.seed(999)
        
        for i in range(self.__numItems):
            accepted_votes = 0
            rejected_votes = 0
            item = Item()

            for j in range(self.__numVoters):
                if i == 0:
                    vote_results[i, j] = self.set_vote(Voter(self.__defaultTokens, self.__pEngaged, self.__pInformed), item)
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

            prev_tokens = self.__totalTokens
            self.__totalTokens = (1 + self.__delta) * self.__totalTokens
            tcr_array[i] = TCR(self.__totalTokens)

            for j in range(self.__numVoters):
                voter = vote_results[i, j]
                num_stake_majority_tokens = (self.__stakePool / num_majority)
                num_inflation_tokens = (self.__totalTokens - prev_tokens) / (accepted_votes + rejected_votes)
                if voter.get_vote() is not None:
                    if item_array[i].is_accepted() == voter.get_vote():
                        # if voter voted correctly, give self.__stake value back
                        voter.set_tokens(voter.get_tokens() + num_stake_majority_tokens)

                    # every voter gets total tokens * self.__delta tokens
                    voter.set_tokens(voter.get_tokens() + num_inflation_tokens)
            self.__stakePool = 0.0
            # self.__stake = (self.__stake * (1 + self.__delta))
            self.__stake = ( self.__initialStake / self.__defaultTokens ) * (self.__totalTokens / self.__numVoters)

        self.set_tcr_values(tcr_array, item_array)
        self.write_file(tcr_array, item_array, vote_results)
        self.generate_voter_plot(vote_results)
        self.generate_tcr_plot(tcr_array)
        self.generate_wealth_plot(vote_results, tcr_array)



simulation = Simulation()
simulation.main()
