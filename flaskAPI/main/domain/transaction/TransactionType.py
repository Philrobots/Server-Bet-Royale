from enum import Enum

class TransactionType(Enum):
    ADD_FUNDS = "ADD_FUNDS",
    RETRIEVE_FUNDS = "RETRIEVE_FUNDS",
    REFUND = "REFUND",
    CREATE_BET = "CREATE_BET",
    ACCEPT_BET = "ACCEPT_BET",
    WON_BET = "WON_BET",
    LOST_BET = "LOST_BET"