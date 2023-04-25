from flask import Flask, render_template, request, flash, redirect, url_for, session, g
from flask_login import login_user, logout_user, current_user, login_required
import mysql.connector
import database;

app = Flask(__name__, template_folder='templates')
app.secret_key = 'somesecretkey'

@app.before_request
def before_request():
    if 'user_id' in session:
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
        mycursor.close()
        mydb.close()

        if user:
            g.user = user
        else:
            session.pop('user_id', None)
            g.user = None

@app.route('/', methods =['GET', 'POST'])
def index():
    return render_template('index.html', boolean=True)

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

        if user:
            session['user_id'] = user[0]
            g.user = user
            return redirect(url_for('home'))   
        else:
            flash('Invalid username or password', 'error')

        mycursor.close()
        mydb.close()

    return render_template('index.html')

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
            # Insert new user
            sql = "INSERT INTO student (FirstName, LastName, EmailAddress, Major, AcademicStanding, Password, Username) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = (fname, lname, email, major, academicStanding, psw, uname)
            mycursor.execute(sql, values)
            mydb.commit()
            # Fetch the studentID of the newly inserted row
            sql = "SELECT LAST_INSERT_ID()"
            mycursor.execute(sql)
            student_id = mycursor.fetchone()[0]
            session['user_id'] = student_id
            g.user = user
            
            return redirect(url_for('home')) 

@app.route('/search_classes', methods=['GET', 'POST'])
def search_classes():
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

    return render_template('searchresults.html', search_output = results)

   
@app.route('/drop_class', methods=['POST'])
def drop_class():
    mydb = mysql.connector.connect(
        host="localhost",
        user="project_user",
        password="password!@#123",
        database="enrollmentsystem"
    )
    mycursor = mydb.cursor()

    course_id = request.form['course_id']
    sql = "DELETE FROM enrollment WHERE studentID = %s AND courseID = %s"

    values = (session['user_id'], course_id)
    mycursor.execute(sql, values)
    mydb.commit()
    mycursor.close()
    mydb.close()

    return redirect(url_for('home'))

@app.route('/drop_shoppingcart_class', methods =['GET', 'POST'])
def drop_shoppingcart_class():
    mydb = mysql.connector.connect(
        host="localhost",
        user="project_user",
        password="password!@#123",
        database="enrollmentsystem"
    )
    mycursor = mydb.cursor()
    course_id = request.form['course_id']
    sql = "SELECT SectionID FROM section WHERE CourseID = %s"
    values = (course_id,)
    mycursor.execute(sql, values)
    sectionID_rows = mycursor.fetchall()
    if not sectionID_rows:
        return "Course not found in section table"
    sectionID_list = [row[0] for row in sectionID_rows]
    sql = "DELETE FROM shoppingcart WHERE StudentID = %s AND SectionID IN (%s)"
    values = (session['user_id'], ','.join(map(str, sectionID_list)))
    mycursor.execute(sql, values)
    mydb.commit()
    mycursor.close()
    mydb.close()
    return redirect(url_for('fifth'))



@app.route('/enroll_in_classes', methods =['GET', 'POST'])
def enroll_in_classes():
    mydb = mysql.connector.connect(
            host="localhost",
            user="project_user",
            password="password!@#123",
            database="enrollmentsystem"
        )
    grade = 'A'
    mycursor = mydb.cursor()
    sql = "SELECT sectionID FROM shoppingcart WHERE studentID = %s"
    values = (session['user_id'],)
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
    return render_template('fifth.html')

    # if request.method == 'POST':
    #     session.pop('user_id', None)

    #     username = request.form.get('username')
    #     password = request.form.get('password')

    #     user = [x for x in users if x.username == username][0]
    #     if user and user.password == password:
    #         session['user_id'] = user.id
    #         return redirect(url_for('home'))
        
    #     return redirect(url_for('login'))
    
    # return render_template('index.html')

@app.route('/logout', methods =['GET', 'POST'])
def logout():
   
   return render_template('index.html')


@app.route('/home', methods =['GET', 'POST'])
def home():
    mydb = mysql.connector.connect(
            host="localhost",
            user="project_user",
            password="password!@#123",
            database="enrollmentsystem"
        )
    mycursor = mydb.cursor()
    sql = "SELECT section.SectionID, section.Schedule, section.RoomNumber, section.InstructionMode, section.Professor, course.CourseName, course.Description " \
          "FROM shoppingcart " \
          "JOIN section ON shoppingcart.SectionID = section.SectionID " \
          "JOIN course ON section.CourseID = course.CourseID " \
          "WHERE shoppingcart.StudentID = %s"
    values = (session['user_id'],)
    
    mycursor.execute(sql, values)
    results = mycursor.fetchall()
    sql = "SELECT section.SectionID, section.Schedule, section.RoomNumber, section.InstructionMode, section.Professor, course.CourseName, course.Description " \
          "FROM section " \
          "JOIN enrollment ON section.SectionID = enrollment.SectionID " \
          "JOIN course ON section.CourseID = course.CourseID " \
          "WHERE enrollment.StudentID = %s"
    mycursor.execute(sql, (session['user_id'],))
    enrolled = mycursor.fetchall()
    print(enrolled)
    return render_template('home.html', user=g.user, shopping_cart=results, enrolled_classes=enrolled)
    #return render_template('home.html') 


# @app.route('/search', methods =['GET', 'POST'])
# def search():
#     if request.method == 'POST':
#         return redirect(url_for('search'))
#         #return render_template('search.html') 

@app.route('/search', methods =['GET', 'POST'])
def search():
    if request.method == 'POST':
        return redirect(url_for('search'))
    return render_template('search.html')


@app.route('/search_results', methods =['GET', 'POST'])
def search_results():
    return render_template('searchresults.html') 

@app.route('/fifth', methods =['GET', 'POST'])
def fifth():
    mydb = mysql.connector.connect(
            host="localhost",
            user="project_user",
            password="password!@#123",
            database="enrollmentsystem"
        )
    mycursor = mydb.cursor()
    sql = "SELECT section.SectionID, section.Schedule, section.RoomNumber, section.InstructionMode, section.Professor, course.CourseName, course.Description " \
          "FROM shoppingcart " \
          "JOIN section ON shoppingcart.SectionID = section.SectionID " \
          "JOIN course ON section.CourseID = course.CourseID " \
          "WHERE shoppingcart.StudentID = %s"
    values = (session['user_id'],)
    
    mycursor.execute(sql, values)
    cart = mycursor.fetchall()
    sql = "SELECT section.SectionID, section.Schedule, section.RoomNumber, section.InstructionMode, section.Professor, course.CourseName, course.Description " \
          "FROM section " \
          "JOIN enrollment ON section.SectionID = enrollment.SectionID " \
          "JOIN course ON section.CourseID = course.CourseID " \
          "WHERE enrollment.StudentID = %s"
    mycursor.execute(sql, (session['user_id'],))
    enrolled = mycursor.fetchall()

    return render_template('fifth.html', shopping_cart=cart, enrolled_classes=enrolled)






if __name__ == '__main__':
    app.run(port=7000, debug=True) #changed port