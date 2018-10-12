import numpy as np
import random

P_ENGAGED = 0.5
P_INFORMED = 0.5


class Voter():
    def __init__(self, tokens):
        self.__mTokens = tokens
        self.__mEngaged = self.get_engagement()
        self.__mInformed = self.get_inform()
        self.__mVote = None

    def is_engaged(self):
        return self.__mEngaged

    def is_informed(self):
        return self.__mInformed

    def get_engagement(self):
        return random.random() > P_ENGAGED

    def get_inform(self):
        return random.random() > P_INFORMED

    def get_tokens(self):
        return self.__mTokens

    def set_tokens(self, tokens):
        if tokens <= 0:
            self.__mTokens = 0
        else:
            self.__mTokens = tokens

    def set_vote(self, vote):
        self.__mVote = vote

    def get_vote(self):
        return self.__mVote