#add class to shopping cart
class shoppingCart:
    def addClass(classID):
        return 0

#remove class from shopping cart
    def removeClass(classID):
        return 0
# class for student
class student:
    # returns classes student is enrolled in, their descriptions, and professors
    def viewSchedule(studentID):
        return 0
    # enroll in all classes in student's shopping cart
    def enrollClass(studentID):
        return 0
    # drop class that student enrolled in
    def dropClass(studentID):
        return 0
    # search for classes
    def search(classID):
        return 0
    
    
class classCourse:
    # gets/sets course number for a course
    def getCourseNum(courseID,studentID):
        return 0
    def setCourseNum(courseID,studentID):
        return 0
    # gets/sets course name for a course
    def getCourseName(courseID,studentID):
        return 0
    def setCourseName(courseID,studentID):
        return 0
    # gets/sets course requirements 
    def getCourseRequirements(courseID,studentID):
        return 0
    def setCourseRequirements(courseID,studentID):
        return 0
    
class courseSection:
    
    def getCourseID():
        return 0
    def setCourseID():
        return 0
    def getCapacity():
        return 0
    def setCapacity():
        return 0
    def getCourseTime():
        return 0
    def setCourseTime():
        return 0
    def getProfessorID():
        return 0
    def setProfessorID():
        return 0
    def getCourseRoom():
        return 0
    def setCourseRoom():
        return 0
    def addStudent():
        return 0
    def removeStudent():
        return 0
    def addStudentToWaitlist():
        return 0
    def removeStudentFromWaitlist():
        return 0
    
    
class courseEnrollment:
    
    def getGrades():
        return 0
    def getStudentID():
        return 0
    def getCourseSectionID():
        return 0
    
class Professor:
    # return professor name for a specific course
    def getProfessor(courseID):
        return 0
    # return professor ID for a specific professor
    def getProfessorID():
        return 0
    
    def getProfessorDetails():
        return 0
    def getProfessorSection():
        return 0
    
    
class Admin:
    def getAdminId(adminID):
        return 0
    def viewSchedule(adminID):
        return 0
    def courseSection(adminID):
        return 0
    def search(adminID):
        return 0

    
