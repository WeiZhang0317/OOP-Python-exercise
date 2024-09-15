class BankAccount:
    def __init__(self, balance, fee):
        self.balance = balance
        self.fee = fee
    
    def deposit(self, amt):
        self.balance = self.balance + amt
    
    def withdraw(self, amt):
        if (amt <= self.balance):
            self.balance = self.balance - amt
            return 1
        else:
            self.balance = self.balance - self.fee            
            return 0

class Transaction:
    def __init__(self, adate, amt, type, account):
        self.Amount = amt
        self.Date = adate
        self.Type = account
