class Enrolment:
    def __init__(self, cCode, cGrade):
        self.courseCode = cCode
        self.courseGrade = cGrade

    def __str__(self):
        return f"Course Code: {self.courseCode} Grade: {self.courseGrade}"
    

class Student:
    def __init__(self, sId, sFName, sLName):
        self.studentID = sId
        self.studentFName = sFName
        self.studentLName = sLName
        self.courses = []


    def __str__(self):
        course_str = '\n'.join(str(course) for course in self.courses)
        return (f"ID: {self.studentID} Name: {self.studentFName} {self.studentLName}\n" 
                f"Courses:\n"
                f"{course_str}")
    
    def addEnrolment(self, course):
        self.courses.append(course)

    def numOfCoursesEnrolled(self):
        return len(self.courses)
    
    def getCourses(self):
        strCourses = ""
        for c in self.courses:
            strCourses += c.__str__()
            strCourses += "\n"
        return strCourses

    def updateGrade(self, ccode, cgrade):
        for c in self.courses:
            if c.courseCode == ccode:
                c.courseGrade = cgrade
                return 1
        return 0
        



course1 = Enrolment('COMP642', 'None')
course2 = Enrolment('COMP639', 'None')
course3 = Enrolment('COMP636', 'A')

student1 = Student('10001', 'James', 'Hanson')
student2 = Student('10002', 'Jade', 'Chan')

student1.addEnrolment(course1)
student1.addEnrolment(course2)
student1.addEnrolment(course3)

#print(student1.numOfCoursesEnrolled())
#print(student1.getCourses())



print(student1.updateGrade("COMP643", "A+"))
print(student1)

