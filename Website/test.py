from flask import Flask, render_template, request, flash, redirect, url_for, session, g
from flask_login import login_user, logout_user, current_user, login_required
import mysql.connector

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
    if request.method == 'POST':
        return redirect(url_for('home'))
    return render_template('home.html', user=g.user)
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
    return render_template('fifth.html')

if __name__ == '__main__':
    app.run(port=7000, debug=True) #changed port
