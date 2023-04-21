from flask import Flask, render_template

app = Flask(__name__, template_folder='templates') #added template_folder

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def second_page():
    return render_template('home.html') 

@app.route('/search')
def third():
    return render_template('search.html') 

@app.route('/search_results')
def fourth():
    return render_template('searchresults.html') 

@app.route('/fifth')
def fifth():
    return render_template('fifth.html')

if __name__ == '__main__':
    app.run(port=7000, debug=True) #changed port
