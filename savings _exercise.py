class SavingsAccount:
    # Initialise the SavingsAccount object with account number, account name, balance, and interest rate
    def __init__(self, accnum, accname, bal, irate):
        self.accNum = accnum
        self.accName = accname
        self.balance = bal
        self.intRate = irate

    def fullInfo(self):
        # Return a string with the account number and account name
        return "AccNum: " + str(self.accNum) + " AccName: " + self.accName

# Create a SavingsAccount object with initial values
acc1 = SavingsAccount(123, "Jonh", 100.00, 0.05)
# Print the current account name
print(acc1.accName)
# Change the account name
acc1.accName = "Jane"
# Print the updated account name
print(acc1.accName)
# Print the full information of the account
print(acc1.fullInfo())