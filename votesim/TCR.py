class TCR:
    # tokenValue = TCRValue / numTotalTokens

    def __init__(self, total_tokens):
        self.__mTotalTokens = total_tokens
        self.__mTokenValue = None

        self.__mTCRValue = 0
        self.__mNumValidItems = 0
        self.__mNumInvalidItems = 0
        self.__mNumTotalItems = 0

    def set_total_tokens(self, total_tokens):
        self.__mTotalTokens = total_tokens

    def get_total_tokens(self):
        return self.__mTotalTokens

    def set_tcr_value(self, valid_included, invalid_not_included, invalid_included, valid_not_included):
        self.__mNumValidItems += valid_included
        self.__mNumInvalidItems += invalid_included
        self.__mNumTotalItems = self.__mNumValidItems + self.__mNumInvalidItems
        self.__mTCRValue += valid_included + invalid_not_included - invalid_included - valid_not_included

    def get_tcr_value(self):
        return self.__mTCRValue

    # def set_token_value(self):
    #
    # def get_token_value(self):

