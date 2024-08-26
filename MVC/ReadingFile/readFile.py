class Person:
    def __init__(self, pName, pCity, pAge):
        self.personName = pName
        self.personCity = pCity
        self.personAge = pAge

    def __str__(self):
        return "Name: " + self.personName + " City: " + self.personCity + \
            " Age: " + str(self.personAge)
    

pList = []

fileName = open("myFile.txt", "r")
count = 0
for line in fileName:
    data=line.strip()
    data = data.split(",")
    print(data)
    count = count + 1
    pName = data[0]
    pCity = data[1]
    pAge = int(data[2])
    aPerson = Person(pName, pCity, pAge)
    pList.append(aPerson)

print("File Read Completed. Number of line is " + str(count))
print()

for p in pList:
    print(p)