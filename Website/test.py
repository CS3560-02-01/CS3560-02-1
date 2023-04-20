from flask import Flask, render_template

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/second_page')
def second_page():
    return render_template('second_page.html') #no second html

@app.route('/third')
def third():
    return render_template('third.html') #no third html 

@app.route('/fourth')
def fourth():
    return render_template('fourth.html') #no fourth html

@app.route('/fifth')
def fifth():
    return render_template('fifth.html')

if __name__ == '__main__':
    app.run(port=7000, debug=True)
