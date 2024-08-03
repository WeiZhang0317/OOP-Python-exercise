# Example
# We want to build a simple application that will manage a
# savings account.
# The transactions supported are deposit, withdraw, calculate
# interest, and check balance.


class SavingsAccount:
      def __init__(self,accnum,accname,bal,irate):
          #accNum is attribute name
          self.accNum = accnum
          self.accName = accname
          self. balance = bal
          self. intRate=irate
## fullInfo method
      def fullInfo(self):
           return "Account name is" +str(self.accName)   
 # create object
acc1 = SavingsAccount(123,"Jane",10000,0.05)         
print(acc1.accName)

acc1.accName="Jess"
print(acc1.accName)
print(acc1.fullInfo())

# Create a class called Elevator based on the diagram below.
# Write a simple application to simulate the elevator’s operation.
# You may assume that the building has 6 floors.

class Elevator:
    def __init__(self):
        self.currentFloor = 0  # assume current foor is 0

    def gotoFloor(self, floor):
        if 0 <= floor <= 6:
            print(f"Moving from floor {self.currentFloor} to floor {floor}")
            self.currentFloor = floor
        else:
            print("Invalid floor. Please choose a floor between 0 and 6.")

    def gotoGround(self):
        print(f"Moving from floor {self.currentFloor} to ground floor")
        self.currentFloor = 0

    def openDoor(self):
        print(f"Opening door at floor {self.currentFloor}")

    def closeDoor(self):
        print(f"Closing door at floor {self.currentFloor}")

elevator = Elevator()

# simulation
elevator.openDoor()
elevator.closeDoor()
elevator.gotoFloor(3)
elevator.openDoor()
elevator.closeDoor()
elevator.gotoGround()
elevator.openDoor()
elevator.closeDoor()
elevator.gotoFloor(7) #invalid



#lecture 2

class Ele:
   def openDoor(self):
      print("open")
   def closeDoor(self):
      print("close") 
   def goFloor(self, floorNo):
      if self.currentFloor==floorNo:
         print( "you are in right one")     

   def gotoGround(self):
      self.goFloor(0)      