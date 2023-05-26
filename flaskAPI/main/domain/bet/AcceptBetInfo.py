from main.domain.identifiers.DomainId import DomainId

class AcceptBetInfo:
    
    def __init__(self, bet_id: DomainId, user_id: DomainId):
        self.bet_id = bet_id
        self.user_id = user_id