from flask import Flask, render_template, request, redirect
from src.login_validation import credentials_validations
from src.utils.emails import mail
from src.signup_credentials import credentials_handling
import random
from src.mongo_db_ops.db_operations import mongo_db_atlas_ops
app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def login():
    return render_template('login.html')
@app.route('/failed_login',methods=['GET','POST'])
def failed_login():
    return render_template('failed_login.html')
@app.route('/home',methods=['POST'])
def home():
    if request.method =='POST':
        email=request.form['email']
        password=request.form['password']
        user_validation=credentials_validations.user_validation(email,password)
        email_validation_flag, password_validation_flag=user_validation.validate_password_and_email()
        mail_obj=mail()
        if email_validation_flag==True and password_validation_flag==True:
            mail_obj.user_login_mail(email)
            return render_template('home.html')
        mail_obj.failed_login_mail(email,email_validation_flag)
        return redirect('/failed_login')
    return redirect('/')
@app.route('/forget_password',methods=['GET','POST'])
def forget_password():
    return render_template("Password_Forget.html")
email_retrival=[]
number=random.randint(10000,200000)
@app.route('/send_code',methods=['POST'])
def send_code():
    email=request.form['email']
    user_validation=credentials_validations.user_validation(email,'password')
    email_validation_flag, _=user_validation.validate_password_and_email()
    email_retrival.append(email)
    if email_validation_flag:
        mail_obj=mail()
        mail_obj.send_code(number,email)
        return render_template("code_validation.html")
    return "<h1>Your Email is not registered with us please Sign-Up with Us!</h1>"
@app.route('/validate_code',methods=['GET','POST'])
def validate_code():
    code=request.form['code']
    if str(code) == str(number):
        return render_template('new_password.html')
    return "<h1>Code is not correct Please try again!</h1>"
@app.route('/generate_new_password',methods=['GET','POST'])
def generate_new_password():
    new_password =request.form['new_password']
    mongo_obj=mongo_db_atlas_ops()
    email_=email_retrival.pop()
    print(email_)
    mongo_obj.update_password(email_,new_password)
    return "<h1>Password Generated Sucessfully now you can log-in</h1>"
@app.route('/signup',methods=['GET','POST'])
def signup():
    return render_template('signup.html')
@app.route('/demo',methods=['GET','POST'])
def demo():
    return "<h1>No Demo Available, Work in progress </h1>"
@app.route('/submit_sign_up_form',methods=['POST'])
def submit_sign_up_form():
    if request.method == 'POST':
        fname=request.form['fname']
        lname=request.form['lname']
        email=request.form['email']
        password=request.form['password']
        city=request.form['city']
        state=request.form['state']
        zip=request.form['zip']
        credentials_obj=credentials_handling.sign_up_credentials()
        dump_data=credentials_obj.dump_credentials_to_mongo_atlas(fname,lname,email,password,city,state,zip)
        if dump_data is None:
            mail_obj=mail()
            mail_obj.user_signup_confirmation_mail(email)
            return render_template('Sign_up_sucessfull.html')
        return dump_data
@app.route('/sign_up_sucessfull',methods=['GET','POST'])
def sign_up_sucessfull():
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)