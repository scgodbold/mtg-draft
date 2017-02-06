class MTGException(Exception):
    def __init__(self, message, level=None):
        self.message = message
        self.level = level

class JoinDraftException(MTGException):
    pass
