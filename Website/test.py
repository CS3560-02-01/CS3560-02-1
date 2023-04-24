from flask import Flask, render_template, request, flash, redirect, url_for
from database import logint
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, current_user, login_required

app = Flask(__name__, template_folder='templates') #added template_folder

# @app.route('/', methods =['GET', 'POST'])
# def index():

#     if request.method == 'POST':
#         # handle form submission
#         username = request.form['username']
#         password = request.form['password']
#         # do something with username and password
#         return render_template('home.html')
#     else:
#         return render_template('index.html', boolean=True)


@app.route('/', methods =['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = logint(username, password)
        if user:
            if check_password_hash(user.password, password):
                flash('Login in successfully' ,category='success')
                login_user(user, remember = True)
                return render_template("home.html")
            else: 
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template("index.html", boolean = True)
# @app.route('/logout', methods =['GET', 'POST'])
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('app.login'))

            



# @app.route('/sign-up', methods =['GET', 'POST'])
# def sign_up():
#     if request.method == 'POST':
#         firstName =request.form.get('firstName')
#         lastName =request.form.get('lastName')
#         email =request.form.get('email')
#         password1 =request.form.get('password')
#         password2 =request.form.get('password2')
#         if len(email) < 4:
#             pass
#         elif len(firstName)< 2:
#             pass
#         elif password1 != password2:
#             pass
#         elif len(password1)<7:
#             pass

@app.route('/', methods = ['GET', 'POST'])
def home():
     if request.method == 'POST':
        return render_template('home.html') 
    

@app.route('/search', methods =['GET', 'POST'])
def search():
    if request.method == 'POST':
        return render_template('search.html') 

@app.route('/search_results', methods =['GET', 'POST'])
def search_results():
    return render_template('searchresults.html') 

@app.route('/fifth', methods =['GET', 'POST'])
def fifth():
    return render_template('fifth.html')

if __name__ == '__main__':
    app.run(port=7000, debug=True) #changed port
