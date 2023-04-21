import mysql.connector


class Database():
    #establish initial connection to mySQL database 
    def __init__(self, host="localhost", user="project_user", password="password!@#123", db="enrollmentsystem"):
        self.mydb = mysql.connector.connect(
                host = host,
                user = user,
                password = password,
                database = db
            )
        self.mycursor = self.mydb.cursor()
    #search courses with courseID, major, academic Standing, instruction mode, and professor (fields can be left empty)
    def search_courses(self, course_id=None, major=None, academic_standing=None, instruction_mode=None, professor=None):
        sql = "SELECT course.CourseName, course.Description, section.SectionID, section.Schedule, section.RoomNumber, section.InstructionMode, section.Professor " \
            "FROM course " \
            "JOIN section ON course.CourseID = section.CourseID " \
            "WHERE 1=1 "
        values = ()
        if course_id:
            sql += "AND course.CourseID = %s "
            values += (course_id,)
        if major:
            sql += "AND course.Major = %s "
            values += (major,)
        if academic_standing:
            sql += "AND course.AcademicStanding = %s "
            values += (academic_standing,)
        if instruction_mode:
            sql += "AND section.InstructionMode = %s "
            values += (instruction_mode,)
        if professor:
            sql += "AND section.Professor = %s "
            values += (professor,)
        self.mycursor.execute(sql, values)
        results = self.mycursor.fetchall()
        return results
    
    #returns the classes that a student is enrolled in
    def get_schedule(self, student_id):
        sql = "SELECT section.SectionID, section.Schedule, section.RoomNumber, section.InstructionMode, section.Professor " \
            "FROM section " \
            "JOIN enrollment ON section.SectionID = enrollment.SectionID " \
            "WHERE enrollment.StudentID = %s"
        self.mycursor.execute(sql, (student_id,))
        results = self.mycursor.fetchall()
        return results

    #register a new student into the system
    def register(self, first_name, last_name, email_address, major, academic_standing, password, username):
        sql = "INSERT INTO student (FirstName, LastName, EmailAddress, Major, AcademicStanding, Password, Username) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (first_name, last_name, email_address, major, academic_standing, password, username)
        self.mycursor.execute(sql, values)
        self.mydb.commit()

    #add a course to a user's shopping cart
    def add_class_to_shoppingcart (self, section_id, student_id):
        sql = "INSERT INTO shoppingcart (SectionID, StudentID) VALUES (%s, %s)"
        values = (section_id, student_id)
        self.mycursor.execute(sql, values)
        self.mydb.commit()

    #show courses that student added to their shopping cart
    def get_shoppingcart(self, student_id):
        sql = "SELECT section.SectionID, section.Schedule, section.RoomNumber, section.InstructionMode, section.Professor, course.CourseName, course.Description " \
            "FROM shoppingcart " \
            "JOIN section ON shoppingcart.SectionID = section.SectionID " \
            "JOIN course ON section.CourseID = course.CourseID " \
            "WHERE shoppingcart.StudentID = %s"
        values = (student_id,)
        self.mycursor.execute(sql, values)
        results = self.mycursor.fetchall()
        return results

    #delete a course from shopping cart
    def remove_class_from_shoppingcart(self, section_id, student_id):
        sql = "DELETE FROM shoppingcart WHERE SectionID = %s AND StudentID = %s"
        values = (section_id, student_id)
        self.mycursor.execute(sql, values)
        self.mydb.commit()
        sql = "DELETE FROM shoppingcart WHERE StudentID = %s"
        values = (student_id,)
        self.mycursor.execute(sql, values)
        self.mydb.commit()

    #enroll student in all couurses selected in their shopping cart (default grade is A+)
    def enroll_in_shoppingcart_classes(self, studentID, grade='A+'):
        sql = "SELECT sectionID FROM shoppingcart WHERE studentID = %s"
        values = (studentID,)
        self.mycursor.execute(sql, values)
        sectionIDs = self.mycursor.fetchall()
        courses = []
        for section in sectionIDs:
            sql = "SELECT courseID, sectionID FROM section WHERE sectionID = %s"
            values = (section[0],)
            self.mycursor.execute(sql, values)
            result = self.mycursor.fetchone()
            courses.append(result)
        for course in courses:
            sql = "SELECT * FROM enrollment WHERE courseID = %s AND sectionID = %s AND studentID = %s"
            values = (course[0], course[1], studentID)
            self.mycursor.execute(sql, values)
            result = self.mycursor.fetchone()
            if result is None:
                sql = "INSERT INTO enrollment (courseID, sectionID, studentID, grade) VALUES (%s, %s, %s, %s)"
                values = (course[0], course[1], studentID, grade)
                self.mycursor.execute(sql, values)
        sql = "DELETE FROM shoppingcart WHERE studentID = %s"
        values = (studentID,)
        self.mycursor.execute(sql, values)
        self.mydb.commit()

    #drop course that student is already enrolled in
    def drop_course(self, student_id, section_id):
        sql = "DELETE FROM enrollment WHERE studentID = %s AND sectionID = %s"
        values = (student_id, section_id)
        self.mycursor.execute(sql, values)
        self.mydb.commit()
        
    #close connection to database
    def __del__(self):
        self.mycursor.close()
        self.mydb.close()

    #examples of each method being called:
    
    #search function calling (all parameters dont need to be declared, default NONE)
    #searchclass = search_courses(course_id = '1', major = 'Computer Science', academic_standing = "Sophomore", professor = "John Smith", instruction_mode ='In-Person')
    #print(searchclass)

    #returns classes that studnet is enrolled in
    #schedule = get_schedule(1)
    #print(schedule)

    #register new student
    #register_output = register('test', 'test', 'test@gmail.com', 'Electrical Engineering', 'Junior', 'password','testing1234')


    #add class to cart
    #add_class_to_shoppingcart(section_id=6, student_id=1)

    #get shopping cart classes
    #shoppingcart = get_shoppingcart(1)
    #print(shoppingcart)

    #remove class from cart
    #remove_class_from_shoppingcart(2, 1)

    #enroll in selected classes
    #enroll_in_shoppingcart_classes(1)

    #drop course
    #drop_course(1, 1)






