class Car:
    def __init__(self,creg):
        self.__carReg = creg
        self.__carOwner = "None"

    @property
    def CarReg(self):
        return self.__carReg

    @CarReg.setter
    def CarReg(self, value):
        self.__carReg = value

    @property
    def CarOwner(self):
        return self.__carOwner

    @CarOwner.setter
    def CarOwner(self, value):
        self.__carOwner = value

    def __str__(self): 
        return self.__carReg + " " + self.CarOwner

    def __eq__(self, other):
        return self.CarReg == other.CarReg
