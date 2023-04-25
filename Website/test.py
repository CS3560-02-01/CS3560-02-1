from flask import Flask, render_template, request, flash, redirect, url_for, session, g
from flask_login import login_user, logout_user, current_user, login_required
import mysql.connector

app = Flask(__name__, template_folder='templates')
app.secret_key = 'somesecretkey'


# method that is called before every method to get the user id of the session
@app.before_request
def before_request():
    if 'user_id' in session:
        # make a connection to the database
        mydb = mysql.connector.connect(
            host="localhost",
            user="project_user",
            password="password!@#123",
            database="enrollmentsystem"
        )
        mycursor = mydb.cursor()
        sql = "SELECT * FROM student WHERE studentid = %s"
        values = (session['user_id'],)
        mycursor.execute(sql, values)
        user = mycursor.fetchone()
        # close database connection
        mycursor.close()
        mydb.close()

        if user:
            g.user = user
        else:
            session.pop('user_id', None)
            g.user = None

# automically direct user to the index.html page when they go to the website
@app.route('/', methods =['GET', 'POST'])
def index():
    return render_template('index.html', boolean=True)


# when using the login button on the index page, this method checks if the username and password exist in the database, if it does, direct the user to the home page with their user id
@app.route('/login', methods =['GET', 'POST'])
def login():
    if request.method == 'POST':
        mydb = mysql.connector.connect(
            host="localhost",
            user="project_user",
            password="password!@#123",
            database="enrollmentsystem"
        )
        mycursor = mydb.cursor()
        username = request.form.get('username')
        password = request.form.get('password')

        sql = "SELECT * FROM student WHERE username = %s AND password = %s"
        values = (username, password)
        mycursor.execute(sql, values)
        user = mycursor.fetchone()
        # checks if valid user, it it is return set session['user_id'] to studentID
        if user:
            session['user_id'] = user[0]
            g.user = user
            return redirect(url_for('home'))  
        # if not, show invalid username or password popup 
        else:
            flash('Invalid username or password', 'error')

        mycursor.close()
        mydb.close()

    return render_template('index.html')

# when using the register button on the index page, call this method. Prompts user to enter first, last, user name, email, major, academic standing, and password and fills in the values into the student table of the database
@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        mydb = mysql.connector.connect(
            host="localhost",
            user="project_user",
            password="password!@#123",
            database="enrollmentsystem"
        )
        mycursor = mydb.cursor()

        # set variables for each of the inputs for the form
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        uname = request.form.get('uname')
        email = request.form.get('email')
        major = request.form.get('major')
        academicStanding = request.form.get('academicStanding')
        psw = request.form.get('psw')

        
        sql = "SELECT * FROM student WHERE Username = %s"
        values = (uname,)
        mycursor.execute(sql, values)
        user = mycursor.fetchone()
        
        if user:
            return render_template('index.html')
        else:
            # Insert new user and their information into student table
            sql = "INSERT INTO student (FirstName, LastName, EmailAddress, Major, AcademicStanding, Password, Username) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = (fname, lname, email, major, academicStanding, psw, uname)
            mycursor.execute(sql, values)
            mydb.commit()

            # Get userID of newly created user (for home page)
            sql = "SELECT LAST_INSERT_ID()"
            mycursor.execute(sql)
            student_id = mycursor.fetchone()[0]
            session['user_id'] = student_id
            g.user = user
            return redirect(url_for('home')) 

# method used to search classes
@app.route('/search_classes', methods=['GET', 'POST'])
def search_classes():
    # inputs the search parameters into variables to be used
    major = request.form['major']
    academic_standing = request.form['academic_standing']
    professor = request.form['professor']
    instruction_mode = request.form['instruction_mode']
    course_id = request.form.get('course_id')
    mydb = mysql.connector.connect(
            host="localhost",
            user="project_user",
            password="password!@#123",
            database="enrollmentsystem"
        )
    mycursor = mydb.cursor()
    sql = "SELECT course.CourseName, course.Description, section.SectionID, section.Schedule, section.RoomNumber, section.InstructionMode, section.Professor " \
          "FROM course " \
          "JOIN section ON course.CourseID = section.CourseID " \
          "WHERE 1=1 "
    values = ()
    # checks if there are search parameters, if not, that parameter is ignored
    if course_id:
        sql += "AND course.CourseID = %s "
        values += (course_id,)
    if major and major != 'Select One':
        sql += "AND course.Major = %s "
        values += (major,)
    if academic_standing and academic_standing != 'Select One':
        sql += "AND course.AcademicStanding = %s "
        values += (academic_standing,)
    if instruction_mode and instruction_mode != 'Select One':
        sql += "AND section.InstructionMode = %s "
        values += (instruction_mode,)
    if professor:
        sql += "AND section.Professor = %s "
        values += (professor,)
    mycursor.execute(sql, values)
    results = mycursor.fetchall()
    mycursor.close()
    mydb.close()
    # reterns the results to the searchresults.html page with the search_output being the results
    return render_template('searchresults.html', search_output = results)


# method called to drop a enrolled class
@app.route('/drop_class', methods=['POST'])
def drop_class():
    mydb = mysql.connector.connect(
        host="localhost",
        user="project_user",
        password="password!@#123",
        database="enrollmentsystem"
    )
    mycursor = mydb.cursor()
    # declares the course_id variable form the form to be used later
    course_id = request.form['course_id']
    sql = "DELETE FROM enrollment WHERE studentID = %s AND courseID = %s"

    values = (session['user_id'], course_id)
    mycursor.execute(sql, values)
    mydb.commit()
    mycursor.close()
    mydb.close()
    # direct user back to home page
    return redirect(url_for('home'))

# method to add selected class to shopping cart
@app.route('/add_class_to_shoppingcart', methods=['POST'])
def add_class_to_shoppingcart():
    mydb = mysql.connector.connect(
        host="localhost",
        user="project_user",
        password="password!@#123",
        database="enrollmentsystem"
    )
    mycursor = mydb.cursor()
    # gets the studentID and sectionID in variables
    section_id = request.form['section_id']
    student_id = session['user_id']
    sql = "SELECT * FROM enrollment WHERE SectionID = %s AND StudentID = %s"
    values = (section_id, student_id)
    mycursor.execute(sql, values)
    result = mycursor.fetchone()

    # if the combination exists in enrollment table redirect to search page
    if result:  
        return redirect(url_for('search'))
    # If the combination doesn't exist in enrollment table, check if it exists in shoppingcart table
    else:  
        sql = "SELECT * FROM shoppingcart WHERE SectionID = %s AND StudentID = %s"
        values = (section_id, student_id)
        mycursor.execute(sql, values)
        result = mycursor.fetchone()
         # if the combination exists in shoppingcart table redirect to search page
        if result:  
            return redirect(url_for('search'))
        # If the combination doesn't exist in either table, add the class to shoppingcart table
        else:  
            sql = "INSERT INTO shoppingcart (SectionID, StudentID) VALUES (%s, %s)"
            values = (section_id, student_id)
            mycursor.execute(sql, values)
            mydb.commit()

    mycursor.close()
    mydb.close()
    return redirect(url_for('search'))

# take in courseID and userID to drop the classes in shoppingcart table
@app.route('/drop_shoppingcart_class', methods =['GET', 'POST'])
def drop_shoppingcart_class():
    mydb = mysql.connector.connect(
        host="localhost",
        user="project_user",
        password="password!@#123",
        database="enrollmentsystem"
    )
    mycursor = mydb.cursor()
    # set form output to course_id
    course_id = request.form['course_id']
    sql = "SELECT SectionID FROM section WHERE CourseID = %s"
    values = (course_id,)
    mycursor.execute(sql, values)
    sectionID_rows = mycursor.fetchall()
    # if the sectionID is not found in the section table (class doesn't have a section) then redirect to enroll page
    if not sectionID_rows:
        return redirect(url_for('enroll'))
    # if sectionID is found, add class to shoppingcart table with the corresponding UserID
    sectionID_list = [row[0] for row in sectionID_rows]
    sql = "DELETE FROM shoppingcart WHERE StudentID = %s AND SectionID IN (%s)"
    values = (session['user_id'], ','.join(map(str, sectionID_list)))
    mycursor.execute(sql, values)
    mydb.commit()
    mycursor.close()
    mydb.close()
    return redirect(url_for('enroll'))


# enroll in classes selected in shopping cart
@app.route('/enroll_in_classes', methods =['GET', 'POST'])
def enroll_in_classes():
    mydb = mysql.connector.connect(
            host="localhost",
            user="project_user",
            password="password!@#123",
            database="enrollmentsystem"
        )
    # default grade is A
    grade = 'A'
    mycursor = mydb.cursor()

    # find sectionID of rows in shopping cart, wehre the studentID matches the session userID
    sql = "SELECT sectionID FROM shoppingcart WHERE studentID = %s"
    values = (session['user_id'],)
    mycursor.execute(sql, values)
    sectionIDs = mycursor.fetchall()
    courses = []
    #for each section, append values to courses
    for section in sectionIDs:
        sql = "SELECT courseID, sectionID FROM section WHERE sectionID = %s"
        values = (section[0],)
        mycursor.execute(sql, values)
        result = mycursor.fetchone()
        courses.append(result)
    # Check if student is enrolled in class first, if not enroll in class 
    for course in courses:
        sql = "SELECT * FROM enrollment WHERE courseID = %s AND sectionID = %s AND studentID = %s"
        values = (course[0], course[1], session['user_id'])
        mycursor.execute(sql, values)
        result = mycursor.fetchone()
        if result is None:
            sql = "INSERT INTO enrollment (courseID, sectionID, studentID, grade) VALUES (%s, %s, %s, %s)"
            values = (course[0], course[1], session['user_id'], grade)
            mycursor.execute(sql, values)
    sql = "DELETE FROM shoppingcart WHERE studentID = %s"
    values = (session['user_id'],)
    mycursor.execute(sql, values)
    mydb.commit()
    mycursor.close()
    mydb.close()
    return render_template('enroll.html')

# logout user and redirect them to index page
@app.route('/logout', methods =['GET', 'POST'])
def logout():
   return render_template('index.html')

# method to be called everytime a user accesses the home page
@app.route('/home', methods =['GET', 'POST'])
def home():
    mydb = mysql.connector.connect(
            host="localhost",
            user="project_user",
            password="password!@#123",
            database="enrollmentsystem"
        )
    mycursor = mydb.cursor()

    # get the shopping cart of the userID
    sql = "SELECT section.SectionID, section.Schedule, section.RoomNumber, section.InstructionMode, section.Professor, course.CourseName, course.Description " \
          "FROM shoppingcart " \
          "JOIN section ON shoppingcart.SectionID = section.SectionID " \
          "JOIN course ON section.CourseID = course.CourseID " \
          "WHERE shoppingcart.StudentID = %s"
    values = (session['user_id'],)
    
    mycursor.execute(sql, values)
    results = mycursor.fetchall()
    # get the schedule for the userID
    sql = "SELECT section.SectionID, section.Schedule, section.RoomNumber, section.InstructionMode, section.Professor, course.CourseName, course.Description " \
          "FROM section " \
          "JOIN enrollment ON section.SectionID = enrollment.SectionID " \
          "JOIN course ON section.CourseID = course.CourseID " \
          "WHERE enrollment.StudentID = %s"
    mycursor.execute(sql, (session['user_id'],))
    enrolled = mycursor.fetchall()
    print(enrolled)
    return render_template('home.html', user=g.user, shopping_cart=results, enrolled_classes=enrolled)

# redirect user to search.html
@app.route('/search', methods =['GET', 'POST'])
def search():
    if request.method == 'POST':
        return redirect(url_for('search'))
    return render_template('search.html')

# if the user calls search_resuls, redirect them to the html page
@app.route('/search_results', methods =['GET', 'POST'])
def search_results():
    return render_template('searchresults.html') 

# method to be used when user goes to the enroll page
@app.route('/enroll', methods =['GET', 'POST'])
def enroll():
    mydb = mysql.connector.connect(
            host="localhost",
            user="project_user",
            password="password!@#123",
            database="enrollmentsystem"
        )
    # get shopping cart of user
    mycursor = mydb.cursor()
    sql = "SELECT section.SectionID, section.Schedule, section.RoomNumber, section.InstructionMode, section.Professor, course.CourseName, course.Description " \
          "FROM shoppingcart " \
          "JOIN section ON shoppingcart.SectionID = section.SectionID " \
          "JOIN course ON section.CourseID = course.CourseID " \
          "WHERE shoppingcart.StudentID = %s"
    values = (session['user_id'],)
    
    mycursor.execute(sql, values)
    cart = mycursor.fetchall()
    # get schedule of user
    sql = "SELECT section.SectionID, section.Schedule, section.RoomNumber, section.InstructionMode, section.Professor, course.CourseName, course.Description " \
          "FROM section " \
          "JOIN enrollment ON section.SectionID = enrollment.SectionID " \
          "JOIN course ON section.CourseID = course.CourseID " \
          "WHERE enrollment.StudentID = %s"
    mycursor.execute(sql, (session['user_id'],))
    enrolled = mycursor.fetchall()

    return render_template('enroll.html', shopping_cart=cart, enrolled_classes=enrolled)



if __name__ == '__main__':
    app.run(port=7000, debug=True) 
