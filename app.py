from flask import Flask, render_template, request, redirect
from src.login_validation import credentials_validations
from src.utils.emails import mail
from datetime import datetime
app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def login():
    return render_template('login.html')
@app.route('/home',methods=['POST'])
def home():
    if request.method =='POST':
        email=request.form['email']
        password=request.form['password']
        user_validation=credentials_validations.user_validation(email,password)
        value=user_validation.validate_password_and_email()
        if value:
            dt=datetime.now()
            mail_obj=mail()
            message=f'''Dear User:\n\tYou are Successfully login to Human and Plant Disease Detection with Health and fitness recommendation dated: {dt.strftime('%Y-%m-%d')}, time: {str(dt.timetz()).split('.')[0]}\nregards: Vicky AI Production'''
            print(message)
            mail_obj.send_mail(email=email,message=message)
            return render_template('home.html')
        return redirect('/')
    return redirect('/')
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)