class Elevator:
      def __init__(self) :
          self.currentFloor=0

      def openDoor(self):
          print("Door Open")

      def closeDoor(self):
          print("Door Open")

      def gotoFloor(self,floorNo):
           if self.currentFloor == floorNo:  
             print("you are in right foor")
           elif floorNo > 6 or floorNo < 0:
             print("its invalid floor")
           else:
               self.currentFloor=floorNo
               print("Going to floor No:" + str(floorNo))  
      def gotoGround(self):
          self.gotoFloor(0)
               
myElevator = Elevator()

myElevator.openDoor()

myElevator.closeDoor()

myElevator.gotoFloor(9)
