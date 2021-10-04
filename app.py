from flask import Flask, render_template

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def login():
    return render_template('login.html')
@app.route('/home',methods=['GET','POST'])
def home():
    return render_template('home.html')
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)