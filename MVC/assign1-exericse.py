# 题目 2：在线课程管理系统
# 题目描述
# 设计一个在线课程管理系统，包括以下三个类：
# Course 类：

# 属性：
# __course_name：课程名称
# __course_code：课程代码
# __instructor：讲师姓名
# __enrolled_students：已注册学生（列表）
# 方法：
# enroll_student(student)：注册一个学生
# unenroll_student(student)：取消一个学生的注册
# get_enrolled_students()：获取已注册学生列表
# __str__()：返回课程的详细信息
class Course:
    def __init__(self, course_name, course_code, instructor):
        self.__course_name = course_name
        self.__course_code = course_code
        self.__instructor = instructor
        self.__enrolled_students = []

    def enroll_student(self, student):
        self.__enrolled_students.append(student)
        student.register_course(self)

    def unenroll_student(self, student):
        if student in self.__enrolled_students:
            self.__enrolled_students.remove(student)
            student.drop_course(self)

    def get_enrolled_students(self):
        return self.__enrolled_students

    def __str__(self):
        return f"Course: {self.__course_name}, Code: {self.__course_code}, Instructor: {self.__instructor}"

# Student 类：

# 属性：
# __name：学生姓名
# __student_id：学生编号
# __email：学生邮箱
# __enrolled_courses：已注册课程（列表）
# 方法：
# register_course(course)：注册一门课程
# drop_course(course)：取消一门课程
# get_enrolled_courses()：获取已注册课程列表
# __str__()：返回学生的详细信息

class Student:
    def __init__(self, name, student_id, email):
        self.__name = name
        self.__student_id = student_id
        self.__email = email
        self.__enrolled_courses = []

    def register_course(self, course):
        self.__enrolled_courses.append(course)

    def drop_course(self, course):
        if course in self.__enrolled_courses:
            self.__enrolled_courses.remove(course)

    def get_enrolled_courses(self):
        return self.__enrolled_courses

    def __str__(self):
        return f"Student: {self.__name}, ID: {self.__student_id}, Email: {self.__email}"

# OnlineLearningPlatform 类：

# 属性：
# __courses：平台上的课程（列表）
# __students：平台上的学生（列表）
# 方法：
# add_course(course)：添加一门课程
# add_student(student)：添加一个学生
# register_student_for_course(student, course)：为学生注册一门课程
# drop_student_from_course(student, course)：为学生取消一门课程
# display_courses()：显示所有课程
# display_students()：显示所有学生

class OnlineLearningPlatform:
    def __init__(self):
        self.__courses = []
        self.__students = []

    def add_course(self, course):
        self.__courses.append(course)

    def add_student(self, student):
        self.__students.append(student)

    def register_student_for_course(self, student, course):
        course.enroll_student(student)

    def drop_student_from_course(self, student, course):
        course.unenroll_student(student)

    def display_courses(self):
        for course in self.__courses:
            print(course)

    def display_students(self):
        for student in self.__students:
            print(student)


# Driver Program
def main():
    # Create online learning platform
    platform = OnlineLearningPlatform()

    # Create courses
    course1 = Course("Introduction to Python", "PY101", "Dr. John Doe")
    course2 = Course("Data Structures", "CS102", "Dr. Jane Smith")

    # Add courses to platform
    platform.add_course(course1)
    platform.add_course(course2)

    # Create students
    student1 = Student("Alice", "S001", "alice@example.com")
    student2 = Student("Bob", "S002", "bob@example.com")

    # Add students to platform
    platform.add_student(student1)
    platform.add_student(student2)

    # Register students for courses
    platform.register_student_for_course(student1, course1)
    platform.register_student_for_course(student2, course2)

    # Display courses and students
    print("Courses:")
    platform.display_courses()

    print("\nStudents:")
    platform.display_students()

    print("\nAlice's enrolled courses:")
    for course in student1.get_enrolled_courses():
        print(course)

    print("\nBob's enrolled courses:")
    for course in student2.get_enrolled_courses():
        print(course)


if __name__ == "__main__":
    main()
