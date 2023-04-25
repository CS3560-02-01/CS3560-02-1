import mysql.connector

mydb = mysql.connector.connect(
        host="localhost",
        user="project_user",
        password="password!@#123",
        database="enrollmentsystem"
    )
mycursor = mydb.cursor()

def search_courses(course_id=None, major=None, academic_standing=None, instruction_mode=None, professor=None):
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
    mycursor.execute(sql, values)
    results = mycursor.fetchall()
    return results

def get_schedule(student_id):
    sql = "SELECT section.SectionID, section.Schedule, section.RoomNumber, section.InstructionMode, section.Professor, course.CourseName, course.Description " \
          "FROM section " \
          "JOIN enrollment ON section.SectionID = enrollment.SectionID " \
          "JOIN course ON section.CourseID = course.CourseID " \
          "WHERE enrollment.StudentID = %s"
    mycursor.execute(sql, (student_id,))
    results = mycursor.fetchall()
    return results


def register(first_name, last_name, email_address, major, academic_standing, password, username):


    sql = "INSERT INTO student (FirstName, LastName, EmailAddress, Major, AcademicStanding, Password, Username) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = (first_name, last_name, email_address, major, academic_standing, password, username)


    mycursor.execute(sql, values)
    mydb.commit()

def add_class_to_shoppingcart (section_id, student_id):

    sql = "INSERT INTO shoppingcart (SectionID, StudentID) VALUES (%s, %s)"
    values = (section_id, student_id)
    mycursor.execute(sql, values)
    mydb.commit()

def get_shoppingcart(student_id):

    sql = "SELECT section.SectionID, section.Schedule, section.RoomNumber, section.InstructionMode, section.Professor, course.CourseName, course.Description " \
          "FROM shoppingcart " \
          "JOIN section ON shoppingcart.SectionID = section.SectionID " \
          "JOIN course ON section.CourseID = course.CourseID " \
          "WHERE shoppingcart.StudentID = %s"
    values = (student_id,)
    mycursor.execute(sql, values)
    results = mycursor.fetchall()
    return results

def remove_class_from_shoppingcart(section_id, student_id):
    sql = "DELETE FROM shoppingcart WHERE SectionID = %s AND StudentID = %s"
    values = (section_id, student_id)
    mycursor.execute(sql, values)
    mydb.commit()
    sql = "DELETE FROM shoppingcart WHERE StudentID = %s"
    values = (student_id,)
    mycursor.execute(sql, values)
    mydb.commit()

def enroll_in_shoppingcart_classes(studentID, grade='A+'):
    sql = "SELECT sectionID FROM shoppingcart WHERE studentID = %s"
    values = (studentID,)
    mycursor.execute(sql, values)
    sectionIDs = mycursor.fetchall()
    courses = []
    for section in sectionIDs:
        sql = "SELECT courseID, sectionID FROM section WHERE sectionID = %s"
        values = (section[0],)
        mycursor.execute(sql, values)
        result = mycursor.fetchone()
        courses.append(result)
    for course in courses:
        sql = "SELECT * FROM enrollment WHERE courseID = %s AND sectionID = %s AND studentID = %s"
        values = (course[0], course[1], studentID)
        mycursor.execute(sql, values)
        result = mycursor.fetchone()
        if result is None:
            sql = "INSERT INTO enrollment (courseID, sectionID, studentID, grade) VALUES (%s, %s, %s, %s)"
            values = (course[0], course[1], studentID, grade)
            mycursor.execute(sql, values)
    sql = "DELETE FROM shoppingcart WHERE studentID = %s"
    values = (studentID,)
    mycursor.execute(sql, values)
    mydb.commit()


def drop_course(student_id, section_id):
    sql = "DELETE FROM enrollment WHERE studentID = %s AND sectionID = %s"
    values = (student_id, section_id)
    mycursor.execute(sql, values)
    mydb.commit()

def logint(username, password):
    print('test')
    sql = "SELECT * FROM student WHERE username = %s AND password = %s"
    values = (username, password)
    mycursor.execute(sql, values)
    result = mycursor.fetchone()
    if result:
        # user is authenticated, return user's id
        return result[0]
    else:
        # user is not authenticated, return None
        return None

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

#login returns ID if login correct, if login incorrect, return NONE
#print(logint('jp', 'passwor1d'))

mycursor.close()
mydb.close()




