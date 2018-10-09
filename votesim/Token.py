class Token:
    # tokenValue = TCRValue / numTotalTokens

    def __init__(self, tokens):
        self.__mTotalTokens = tokens
        self.__mTCRValue = None
        self.__mTokenValue = None

    def set_total_tokens(self, total_tokens):
        self.__mTotalTokens = total_tokens

    def get_total_tokens(self):
        return self.__mTotalTokens

    # def set_tcr_value(self):
    #
    # def get_tcr_value(self):
    #
    # def set_token_value(self):
    #
    # def get_token_value(self):

