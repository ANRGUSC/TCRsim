import numpy as np
import random


class Voter():
    def __init__(self, tokens, p_engaged, p_informed):
        self.__mTokens = tokens
        self.__mEngaged = self.get_engagement(p_engaged)
        self.__mInformed = self.get_inform(p_informed)
        self.__mVote = None

    def is_engaged(self):
        return self.__mEngaged

    def is_informed(self):
        return self.__mInformed

    def get_engagement(self, p_engaged):
        return random.random() < p_engaged

    def get_inform(self, p_informed):
        return random.random() < p_informed

    def get_tokens(self):
        return self.__mTokens

    def set_tokens(self, tokens):
        if tokens <= 0.0:
            self.__mTokens = 0.0
        else:
            self.__mTokens = tokens

    def set_vote(self, vote):
        self.__mVote = vote

    def get_vote(self):
        return self.__mVote