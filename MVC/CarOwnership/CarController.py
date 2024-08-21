from Person import Person
from Car import Car

class CarController:
    def __init__(self):
        self.allCars = []
        self.allPeople = []

    def newCar(self, creg):
        aCar = Car(creg)
        self.allCars.append(aCar)

    def newPerson(self, pname):
        aPerson = Person(pname)
        self.allPeople.append(aPerson)

    def findCar(self, creg):
        for car in self.allCars:
            if car.CarReg == creg:
                return car
        return None

    def findPerson(self, pname):
        for person in self.allPeople:
            if  person.PersonName == pname:
                return person
        return None


    def changeOwner(self, pname, creg):
        aCar = self.findCar(creg)
        aPerson = self.findPerson(pname)
        print(aCar)
        print(aPerson)
        print("Previous Owner is " + aCar.CarOwner)
        pOwner = aCar.CarOwner
        if aCar.CarOwner == "None":
            aCar.CarOwner = aPerson.PersonName
        else:
            prevOwner = self.findPerson(pOwner)
            print(prevOwner)
            prevOwner.removeCar(aCar)
            aCar.CarOwner = aPerson.PersonName
        

        print(aCar.CarReg + " is owned by " + aCar.CarOwner)

        aPerson.addCars(aCar)
        print(aPerson.PersonName + " has " + str(aPerson.numCars()))

        for person in self.allPeople:
            person.personDetail()

    def whoIsOwner(self, creg):
        print("creg " + creg)
        aCar = self.findCar(creg)
        print("Car found " + aCar.CarReg)
        anOwner = aCar.CarOwner
        if anOwner == "None":
            return "No Owner"
        else:
            return anOwner + " owns " + creg

    def listCars(self, pname):
        myList = ""
        aPerson = self.findName(pname)

        for car in aPerson.Cars:
            myList += myList + car.CarReg + "\n"

        return myList

    
