from flask import Flask, render_template, request, redirect
from src.login_validation import credentials_validations
from src.utils.emails import mail
from src.signup_credentials import credentials_handling
from src.mongo_db_ops.db_operations import mongo_db_atlas_ops
import numpy as np
import os
import pickle
import pandas as pd
from werkzeug.utils import secure_filename
from src.app_utils.generate_random_code_for_validation import generate_code, read_code
from src.app_utils.predict_images import pred_plant_dieas,pred_pnemoian,pred_skin
from src.app_utils.kidney_disease_prediction import kidney_disease_pred
from src.utils.common_utils import create_directory
from src.cassandra_db_ops.dump_data_into_cassandra import cassandra_ops
from src.medical_report.create_medical_report import medical_report_management
from src.loggings import add_logger
from flask_cors import CORS
os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'
create_directory([os.path.join('static','user_upload')])
log=add_logger()
medical_rep_obj=medical_report_management()
email_from_home=[]
app = Flask(__name__)
CORS(app)
@app.route('/',methods=['GET','POST'])
def login():
    cassandra_obj=cassandra_ops()
    cassandra_obj.dump_logging_files_into_cassandra_db()
    create_directory(['Project_Logs'])
    return render_template('login.html')
@app.route('/failed_login',methods=['GET','POST'])
def failed_login():
    return render_template('failed_login.html')
home_login_flag=[False]
@app.route('/home',methods=['POST','GET'])
def home():
    if request.method =='POST':
        try:
            email=request.form['email']
            email_from_home.append(email)
            password=request.form['password']
            user_validation=credentials_validations.user_validation(email,password)
            email_validation_flag, password_validation_flag=user_validation.validate_password_and_email()
            mail_obj=mail()
            if email_validation_flag==True and password_validation_flag==True:
                mail_obj.user_login_mail(email)
                home_login_flag[0]=True 
                return render_template('home.html')
            mail_obj.failed_login_mail(email,email_validation_flag)
            return redirect('/failed_login')
        except Exception as e:
            log.log(f'Some Unknown Error Occured in home funtion, error {str(e)}','app.log',3)
            return '<center><h1>Sorry due to some reason we are unable to show you the results. Please Consult with the Developer Team</h1></center>'
    elif home_login_flag[0]:
        return render_template('home.html')
    else:
        return redirect('/')
@app.route('/forget_password',methods=['GET','POST'])
def forget_password():
    return render_template("Password_Forget.html")
email_retrival=[]
@app.route('/send_code',methods=['POST','GET'])
def send_code():
    if request.method == 'POST':
        try:
            email=request.form['email']
            user_validation=credentials_validations.user_validation(email,'password')
            email_validation_flag, _=user_validation.validate_password_and_email()
            email_retrival.append(email)
            if email_validation_flag:
                mail_obj=mail()
                generate_code()
                number=read_code()
                mail_obj.send_code(number,email)
                return render_template("code_validation.html")
            return "<h1>Your Email is not registered with us please Sign-Up with Us! Refresh this page</h1>"
        except Exception as e:
            log.log(f'Some Unknown Error Occured in send_code funtion, error {str(e)}','app.log',3)
            return '<center><h1>Sorry due to some reason we are unable to show you the results. Please Consult with the Developer Team</h1></center>'
    return redirect('/forget_password')
@app.route('/validate_code',methods=['GET','POST'])
def validate_code():
    if request.method == 'POST':
        try:
            code=request.form['code']
            number=read_code()
            if str(code) == str(number):
                return render_template('new_password.html')
            return "<h1>Code is not correct Please try again! Please refresh the page</h1>"
        except Exception as e:
            log.log(f'Some Unknown Error Occured in validate_code funtion, error {str(e)}','app.log',3)
            return '<center><h1>Sorry due to some reason we are unable to show you the results. Please Consult with the Developer Team</h1></center>'
    return redirect('/forget_password')
@app.route('/generate_new_password',methods=['GET','POST'])
def generate_new_password():
    if request.method == 'POST':
        try:
            new_password =request.form['new_password']
            mongo_obj=mongo_db_atlas_ops()
            email_=email_retrival.pop()
            mongo_obj.update_password(email_,new_password)
            return "<h1>Password Generated Sucessfully now you can log-in. Please refresh the page</h1>"
        except Exception as e:
            log.log(f'Some Unknown Error Occured in generate_new_password funtion, error {str(e)}','app.log',3)
            return '<center><h1>Sorry due to some reason we are unable to show you the results. Please Consult with the Developer Team</h1></center>'
    return redirect('/forget_password')
@app.route('/signup',methods=['GET','POST'])
def signup():
    return render_template('signup.html')
@app.route('/demo',methods=['GET','POST'])
def demo():
    return "<h1>No Demo Available, Work in progress </h1>"
@app.route('/submit_sign_up_form',methods=['POST'])
def submit_sign_up_form():
    if request.method == 'POST':
        try:
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
        except Exception as e:
            log.log(f'Some Unknown Error Occured in submit_sign_up_form funtion, error {str(e)}','app.log',3)
            return '<center><h1>Sorry due to some reason we are unable to show you the results. Please Consult with the Developer Team</h1></center>'
        return dump_data
@app.route('/sign_up_sucessfull',methods=['GET','POST'])
def sign_up_sucessfull():
    return redirect('/')
# ............................Plant App Started.................................  
@app.route("/Plant_disease_index", methods=[ 'POST','GET'])
def Plant_disease_index():
    if home_login_flag[0]:
        return render_template("Plant_disease_index.html")
    return redirect('/')
# get input image from client then predict class and render respective .html page for solution
@app.route("/predict", methods = ['GET','POST'])
def predict():
    if request.method == 'POST':
        try:
            file = request.files['image'] # fet input
            filename = file.filename        
            file_path = os.path.join('static','user_upload', filename)
            file.save(file_path)

            pred, output_page = pred_plant_dieas(plant=file_path)
            return render_template(output_page, pred_output = pred, user_image = 'user_upload/'+filename)
        except Exception as e:
            log.log(f'Some Unknown Error Occured in predict funtion, error {str(e)}','app.log',3)
            return '<center><h1>Sorry due to some reason we are unable to show you the results. Please Consult with the Developer Team</h1></center>'
    return redirect('/') 
# ............................Plant APP Ended........................................................

# ...................................Health APP Started...............................................

# render index.html page
@app.route("/health_index", methods=['GET', 'POST'])
def health_index():
    if home_login_flag:
        return render_template('health_index.html')
    return redirect('/')
@app.route("/heart", methods=['GET', 'POST'])
def heart():
    if home_login_flag:
        return render_template('heart.html')
    return redirect('/')

@app.route('/heart_predict',methods=["GET","POST"])
def heart_predict():
    if home_login_flag:
        try:
            model = pickle.load(open(os.path.join('Model','Heart_disease_ab_0.90_model.sav'), 'rb'))
            if request.method == 'POST':
                age=request.form['age']
                
                sex=request.form['sex']
                cp=request.form['cp']
                trestbps=request.form['trestbps']
                chol=request.form['chol']
                fbs=request.form['fbs']
                restecg=request.form['restecg']
                thalach=request.form['thalach']
                exang=request.form['exang']
                oldpeak=request.form['oldpeak']
                slope=request.form['slope']

                ca=request.form['ca']

                thal=request.form['thal']
                values=[age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal]
                X=[]
                try:
                    for value in values:
                        X.append(np.log(float(value)+1))
                    output=model.predict([X])
                except Exception as e:
                    return render_template('heart.html',prediction_text="Some unknown error occured please input the values in number or contact the develpor if it still occurs")
                if output==0:
                    prediction_text="Prediction Result: Don't worry You don't have any disease! "
                    email=email_from_home[-1]
                    medical_rep_obj.generate_the_report(email,prediction_text)
                    return render_template('heart.html',prediction_text=prediction_text,link="https://my-medical-report-docfile.s3.us-east-2.amazonaws.com/file.docx",text="Click Here to generate report")
                elif output==1:
                    prediction_text="We found something wrong with you please consult with the doctor! "
                    email=email_from_home[-1]
                    medical_rep_obj.generate_the_report(email,prediction_text)
                    return render_template('heart.html',prediction_text=prediction_text,link="https://my-medical-report-docfile.s3.us-east-2.amazonaws.com/file.docx",text="Click Here to generate report")
            else:
                return render_template('heart.html')
        except Exception as e:
            log.log(f'Some Unknown Error Occured in heart_predict funtion, error {str(e)}','app.log',3)
            return '<center><h1>Sorry due to some reason we are unable to show you the results. Please Consult with the Developer Team</h1></center>'
    return redirect('/')

@app.route("/breast", methods=['GET', 'POST'])
def breast():
    if home_login_flag:
        return render_template('breast.html')
    return redirect('/')
@app.route("/breast_predict", methods=['GET', 'POST'])
def breast_predict():
    if home_login_flag:
        try:
            model = pickle.load(open(os.path.join('Model','brest_cancer_rf_model.sav'), 'rb'))
            if request.method == 'POST':
                try:
                    mean_radius=float(request.form['mean_radius'])
                    mean_texture=float(request.form['mean_texture'])
                    mean_perimeter=float(request.form['mean_perimeter'])
                    mean_area=float(request.form['mean_area'])
                    mean_smoothness=float(request.form['mean_smoothness'])
                except Exception as e:
                    return render_template('breast.html',prediction_text="Some unknown error occured please input the values in number or contact the develpor if it still occurs")
            
                output=model.predict([[mean_radius,mean_texture,mean_perimeter,mean_area,mean_smoothness]])
                if output==0:
                    prediction_text="Prediction Result: Don't worry You don't have any disease! "
                    email=email_from_home[-1]
                    medical_rep_obj.generate_the_report(email,prediction_text)
                    return render_template('breast.html',prediction_text=prediction_text,link="https://my-medical-report-docfile.s3.us-east-2.amazonaws.com/file.docx",text="Click Here to generate report")
                elif output==1:
                    prediction_text="We found something wrong with you please consult with the doctor! "
                    email=email_from_home[-1]
                    medical_rep_obj.generate_the_report(email,prediction_text)
                    return render_template('breast.html',prediction_text=prediction_text,link="https://my-medical-report-docfile.s3.us-east-2.amazonaws.com/file.docx",text="Click Here to generate report")
                    
        except Exception as e:
            log.log(f'Some Unknown Error Occured in breast_predict funtion, error {str(e)}','app.log',3)
            return '<center><h1>Sorry due to some reason we are unable to show you the results. Please Consult with the Developer Team</h1></center>'

        return render_template('breast.html')
    return redirect('/')
@app.route("/pnemonia", methods=['GET', 'POST'])
def pnemonia():
    if home_login_flag:
        return render_template('pnemonia.html')
    return redirect('/')
@app.route("/predict_pnemonia", methods=['GET', 'POST'])
def predict_pnemonia():
    if home_login_flag:
        if request.method=='POST':
            try:
                f = request.files['file']

                # Save the file to ./uploads
                basepath = os.path.dirname(__file__)
                file_path = os.path.join(
                basepath, 'static','user_upload', secure_filename(f.filename))
                f.save(file_path)

                # Make prediction
                preds = pred_pnemoian(file_path)
                result=preds
                return result
            except Exception as e:
                log.log(f'Some Unknown Error Occured in predict_pnemonia funtion, error {str(e)}','app.log',3)
                return '<center><h1>Sorry due to some reason we are unable to show you the results. Please Consult with the Developer Team</h1></center>'
        return redirect('/')
    return redirect('/')
    
@app.route("/diabtes", methods=['GET', 'POST'])
def diabtes():
    if home_login_flag:
        return render_template('diabtes.html')
    return redirect('/')
@app.route("/diabtes_predict", methods=['GET', 'POST'])
def diabtes_predict():
    if home_login_flag:
        model = pickle.load(open(os.path.join('Model','diabetes_xg_0.76_model.sav'), 'rb'))
        if request.method == 'POST':
            try:
                try:
                    Pregnancies=float(request.form['Pregnancies'])
                    Glucose=float(request.form['Glucose'])
                    BloodPressure=float(request.form['BloodPressure'])
                    SkinThickness=float(request.form['SkinThickness'])
                    Insulin=float(request.form['Insulin'])
                    BMI=float(request.form['BMI'])
                    DiabetesPedigreeFunction=float(request.form['DiabetesPedigreeFunction'])
                    Age=float(request.form['Age'])
                except Exception as e:
                    return render_template('diabtes.html',prediction_text="Some unknown error occured please input the values in number or contact the develpor if it still occurs")
                df=pd.DataFrame([[Pregnancies,Glucose,BloodPressure,SkinThickness,Insulin,BMI,DiabetesPedigreeFunction,Age]],columns=['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age'])
                output=model.predict(df)
                if output==0:
                    prediction_text="Prediction Result: Don't worry You don't have diabtes! "
                    email=email_from_home[-1]
                    medical_rep_obj.generate_the_report(email,prediction_text)
                    return render_template('diabtes.html',prediction_text=prediction_text,link="https://my-medical-report-docfile.s3.us-east-2.amazonaws.com/file.docx",text="Click Here to generate report")
                    
                elif output==1:
                    prediction_text="We found that you have diabtes, please consult with the doctor!"
                    email=email_from_home[-1]
                    medical_rep_obj.generate_the_report(email,prediction_text)
                    return render_template('diabtes.html',prediction_text=prediction_text,link="https://my-medical-report-docfile.s3.us-east-2.amazonaws.com/file.docx",text="Click Here to generate report")
            except Exception as e:
                log.log(f'Some Unknown Error Occured in diabtes_predict funtion, error {str(e)}','app.log',3)
                return '<center><h1>Sorry due to some reason we are unable to show you the results. Please Consult with the Developer Team</h1></center>'
        return render_template('diabtes.html')
    return redirect('/')
@app.route("/skin", methods=['GET', 'POST'])
def skin():
    if home_login_flag:
        return render_template('skin.html')
    return redirect('/')
@app.route("/predict_skin", methods=['GET', 'POST'])
def predict_skin():
    if home_login_flag:
        if request.method=='POST':
            try:
                f = request.files['file']

                # Save the file to ./uploads
                basepath = os.path.dirname(__file__)
                file_path = os.path.join(
                basepath, 'static','user_upload', secure_filename(f.filename))
                f.save(file_path)

                # Make prediction
                preds = pred_skin(file_path)
                result=preds
            except Exception as e:
                log.log(f'Some Unknown Error Occured in predict_skin funtion, error {str(e)}','app.log',3)
                return '<center><h1>Sorry due to some reason we are unable to show you the results. Please Consult with the Developer Team</h1></center>'
            return result
    return redirect('/')
@app.route("/kidney", methods=['GET', 'POST'])
def kidney():
    if home_login_flag:
        return render_template('kidney.html')
    return redirect('/')
@app.route("/kidney_predict", methods=['GET', 'POST'])
def kidney_predict():
    if home_login_flag:
        if request.method=='POST':
            try:
                age=float(request.form['age'])
                bp=float(request.form['bp'])
                sg=float(request.form['sg'])
                al=float(request.form['al'])
                su=float(request.form['su'])
                bgr=float(request.form['bgr'])
                bu=float(request.form['bu'])
                sc=float(request.form['sc'])
                sod=float(request.form['sod'])
                pot=float(request.form['pot'])
                hemo=float(request.form['hemo'])
                pcv=float(request.form['pcv'])
                wc=float(request.form['wc'])
                rc=float(request.form['rc'])
            except Exception as e:
                return render_template('kidney.html',prediction_text="Some unknown error occured please input the values in number or contact the develpor if it still occurs")
            output=kidney_disease_pred(age, bp, sg, al, su, bgr, bu, sc, sod, pot, hemo,pcv, wc, rc)
            if output==0:
                
                prediction_text="Result: Prediction Result: Don't worry You don't have any Kidney disease!"
                email=email_from_home[-1]
                medical_rep_obj.generate_the_report(email,prediction_text)
                return render_template('kidney.html',prediction_text=prediction_text,link="https://my-medical-report-docfile.s3.us-east-2.amazonaws.com/file.docx",text="Click Here to generate report")
            elif output==1:
                prediction_text="Result: We found something wrong with your kidney, please consult with the doctor"
                email=email_from_home[-1]
                medical_rep_obj.generate_the_report(email,prediction_text)
                return render_template('kidney.html',prediction_text=prediction_text,link="https://my-medical-report-docfile.s3.us-east-2.amazonaws.com/file.docx",text="Click Here to generate report")
        return render_template('diabtes.html')
    return redirect('/')


# ...................................Health APP Ended.................................................
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)