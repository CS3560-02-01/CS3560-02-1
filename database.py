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
    sql = "SELECT section.SectionID, section.Schedule, section.RoomNumber, section.InstructionMode, section.Professor " \
          "FROM section " \
          "JOIN enrollment ON section.SectionID = enrollment.SectionID " \
          "WHERE enrollment.StudentID = %s"
    mycursor.execute(sql, (student_id,))
    results = mycursor.fetchall()
    return results

#search function calling (all parameters dont need to be declared, default NONE)
#searchclass = search_courses(course_id = '1', major = 'Computer Science', academic_standing = "Sophomore", professor = "John Smith", instruction_mode ='In-Person')
#print(searchclass)

#returns classes that studnet is enrolled in
#schedule = get_schedule(1)
#print(schedule)

#add class to cart

#remove class from cart

#enroll in selected classes

#drop course




mycursor.close()




