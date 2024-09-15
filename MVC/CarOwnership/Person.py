from Car import Car

class Person:
    nextID = 100
    def __init__(self, pname):
        self.__personID = Person.nextID
        self.__personName = pname
        self.__personCars = []
        Person.nextID += 1

    def addCars(self, aCar):
        self.__personCars.append(aCar)

    def removeCar(self, aCar):
        self.__personCars.remove(aCar)

    def numCars(self):
        return len(self.__personCars)
        
    @property
    def PersonID(self):
        return self.__personID

    @property
    def PersonName(self,):
        return self.__personName

    @PersonName.setter
    def PersonName(self, value):
        self.__personName = value

    @property
    def Cars(self):
        return self.__personCars

    def __str__(self):
        return str(self.__personID) + " " + self.__personName

    def personDetail(self):
        print(self.PersonName)
        for car in self.Cars:
            print(car)

aCar = Car('CAR')
print(aCar)
aPerson = Person("Estela")
print(aPerson)
aPerson.addCars(aCar)
aCar.CarOwner = "Estela"
aPerson.personDetail()
print(aPerson.numCars())
    