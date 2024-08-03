class SavingsAccount:
    # Initialise the SavingsAccount object with account number, account name, balance, and interest rate
    def __init__(self, accnum, accname, bal, irate):
        self.accNum = accnum
        self.accName = accname
        self.balance = bal
        self.intRate = irate

    def fullInfo(self):
        # Return a string with the account number and account name

