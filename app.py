from flask import Flask, render_template, request, redirect
from src.login_validation import credentials_validations
from src.utils.emails import mail
from src.signup_credentials import credentials_handling
import random
from src.mongo_db_ops.db_operations import mongo_db_atlas_ops
import numpy as np
import os
from tensorflow.keras.preprocessing.image import img_to_array,load_img
from tensorflow.keras.models import load_model
import requests
import pickle
import pandas as pd
from werkzeug.utils import secure_filename
app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def login():
    return render_template('login.html')
@app.route('/failed_login',methods=['GET','POST'])
def failed_login():
    return render_template('failed_login.html')
@app.route('/home',methods=['POST','GET'])
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
    else:
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
# ............................Plant App Started................................. 
 
#load model
model=load_model("Model/Various Plant Disease Detection Model1.h5")

print('@@ Model loaded')


def pred_plant_dieas(plant):
  test_image = load_img(plant, target_size = (150, 150)) # load image 
  print("@@ Got Image for prediction")
  test_image = img_to_array(test_image)/255 
  test_image = np.expand_dims(test_image, axis = 0) # change dimention 3D to 4D
   
  result = model.predict(test_image).round(3) 
  print('@@ Raw result = ', result)
   
  pred = np.argmax(result) 
 
  if pred == 0:
    return "Pepper bell Bacterial_spot", 'Pepper__bell___Bacterial_spot.html' 
  elif pred == 1:
      return 'Pepper bell healthy', 'Pepper__bell___healthy.html' 
  elif pred == 2:
      return 'Potato Early blight', 'Potato___Early_blight.html'  
  elif pred == 3:
      return 'Potato Late blight', 'Potato___Late_blight.html'  
  elif pred==4:
    return "Potato healthy", 'Potato___healthy.html' 
  elif pred==5:
    return "Tomato Bacterial spot", 'Tomato_Bacterial_spot.html' 
  elif pred==6:
    return "Tomato Early blight", 'Tomato_Early_blight.html' 
  elif pred==7:
    return "Tomato Late blight", 'Tomato_Late_blight.html' 
  elif pred==8:
    return "Tomato Leaf Mold", 'Tomato_Leaf_Mold.html' 
  elif pred==9:
    return "Tomato Septoria leaf spot", 'Tomato_Septoria_leaf_spot.html' 
  elif pred==10:
    return "Tomato Spider mites Two spotted spider mite", 'Tomato_Spider_mites_Two_spotted_spider_mite.html' 
  elif pred==11:
    return "Tomato Target Spot", 'Tomato__Target_Spot.html' 
  elif pred==12:
    return "Tomato Yellow Leaf Curl Virus", 'Tomato__Tomato_YellowLeaf__Curl_Virus.html' 
  elif pred==13:
    return "Tomato_mosaic_virus", 'Tomato__Tomato_mosaic_virus.html' 
  elif pred==14:
    return "Tomato healthy", 'Tomato_healthy.html' 
  elif pred==15:
    return "Diseased cotton leaf", 'diseased_cotton_leaf.html' 
  elif pred==16:
    return "Diseased cotton plant", 'diseased_cotton_plant.html' 
  elif pred==17:
    return "Fresh cotton leaf", 'fresh_cotton_leaf.html' 
  elif pred==18:
    return "Fresh cotton plant", 'fresh_cotton_plant.html' 
  else:
    return "An unknown error has been occured", 'error.html'

     
 
# render index.html page
@app.route("/Plant_disease_index", methods=['GET', 'POST'])
def Plant_disease_index():
  # return("Hellow World")
  return render_template("Plant_disease_index.html")
     
  
# get input image from client then predict class and render respective .html page for solution
@app.route("/predict", methods = ['GET','POST'])
def predict():

  if request.method == 'POST':
    file = request.files['image'] # fet input
    filename = file.filename        
    print("@@ Input posted = ", filename)
    file_path = os.path.join('static','user_upload', filename)
    file.save(file_path)
 
    print("@@ Predicting class......")
    pred, output_page = pred_plant_dieas(plant=file_path)
    print("File Path is : ",file_path)
               
    return render_template(output_page, pred_output = pred, user_image = 'user_upload'+'/'+filename)
# ............................Plant APP Ended........................................................

# ...................................Health APP Started...............................................

def pred_pnemoian(img_path):
    model=load_model("Model/Chest XRay Pnemonia xception model.h5")
    img=load_img(img_path,target_size=(224,224))
    x=img_to_array(img)/225
    x=np.expand_dims(x, axis=0)
    pred=model.predict(x)
    output=np.argmax(pred,axis=1)
    if output==0:
        return "Prediction Result: Don't worry You don't have any disease!"
    elif output==1:
        return "We found that you have Pnemonia disease please consult with the doctor"
def pred_skin(img_path):
    
    model=load_model("Model/skin cancer vgg16 model.h5")
    img=load_img(img_path,target_size=(224,224))
    x=img_to_array(img)/225
    x=np.expand_dims(x, axis=0)
    pred=model.predict(x)
    output=np.argmax(pred,axis=1)
    if output==0:
        return "Prediction Result: Don't worry You don't have any disease!"
    elif output==1:
        return "We found that you have skin cancer, please consult with the doctor"


# render index.html page
@app.route("/health_index", methods=['GET', 'POST'])
def health_index():
    return render_template('health_index.html')
@app.route("/heart", methods=['GET', 'POST'])
def heart():
    return render_template('heart.html')

@app.route('/heart_predict',methods=["GET","POST"])
def heart_predict():
    model = pickle.load(open('Model/Heart_disease_ab_0.90_model.sav', 'rb'))
    print("@@ Heart Disease Model Loaded")
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
            print("@@",e)
            return render_template('heart.html',prediction_text="Some unknown error occured please input the values in number or contact the develpor if it still occurs")

        if output==0:
            return render_template('heart.html',prediction_text="Prediction Result: Don't worry You don't have any disease!")
        elif output==1:
            return render_template('heart.html',prediction_text="We found something wrong with you please consult with the doctor")




    else:
        return render_template('heart.html')

@app.route("/breast", methods=['GET', 'POST'])
def breast():
    return render_template('breast.html')
@app.route("/breast_predict", methods=['GET', 'POST'])
def breast_predict():
    model = pickle.load(open('Model/brest_cancer_rf_model.sav', 'rb'))
    print("@@ Breast Cancer Model Loaded")
    if request.method == 'POST':
        try:
            mean_radius=float(request.form['mean_radius'])
            mean_texture=float(request.form['mean_texture'])
            mean_perimeter=float(request.form['mean_perimeter'])
            mean_area=float(request.form['mean_area'])
            mean_smoothness=float(request.form['mean_smoothness'])
        except Exception as e:
            print("@@",e)
            return render_template('breast.html',prediction_text="Some unknown error occured please input the values in number or contact the develpor if it still occurs")
        
        output=model.predict([[mean_radius,mean_texture,mean_perimeter,mean_area,mean_smoothness]])
        if output==0:
            return render_template('breast.html',prediction_text="Prediction Result: Don't worry You don't have any disease!")
        elif output==1:
            return render_template('breast.html',prediction_text="We found something wrong with you please consult with the doctor")

    return render_template('breast.html')
@app.route("/pnemonia", methods=['GET', 'POST'])
def pnemonia():
    return render_template('pnemonia.html')
@app.route("/predict_pnemonia", methods=['GET', 'POST'])
def predict_pnemonia():
    if request.method=='POST':
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
    
@app.route("/diabtes", methods=['GET', 'POST'])
def diabtes():
    return render_template('diabtes.html')
@app.route("/diabtes_predict", methods=['GET', 'POST'])
def diabtes_predict():
    model = pickle.load(open('Model/diabetes_xg_0.76_model.sav', 'rb'))
    print("@@ Diabtes Model Loaded")
    if request.method == 'POST':
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
            print("@@",e)
            return render_template('diabtes.html',prediction_text="Some unknown error occured please input the values in number or contact the develpor if it still occurs")
        df=pd.DataFrame([[Pregnancies,Glucose,BloodPressure,SkinThickness,Insulin,BMI,DiabetesPedigreeFunction,Age]],columns=['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age'])
        output=model.predict(df)
        if output==0:
            return render_template('diabtes.html',prediction_text="Prediction Result: Don't worry You don't have diabtes!")
        elif output==1:
            return render_template('diabtes.html',prediction_text="We found that you have diabtes, please consult with the doctor")

    return render_template('diabtes.html')
@app.route("/skin", methods=['GET', 'POST'])
def skin():
    return render_template('skin.html')
@app.route("/predict_skin", methods=['GET', 'POST'])
def predict_skin():
    if request.method=='POST':
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
        basepath, 'static','user_upload', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = pred_skin(file_path)
        result=preds
        return result
@app.route("/kidney", methods=['GET', 'POST'])
def kidney():
    return render_template('kidney.html')
@app.route("/kidney_predict", methods=['GET', 'POST'])
def kidney_predict():
    model = pickle.load(open('Model/kidney_disease_ab1_model.sav', 'rb'))
    print("@@ Kidney Model Loaded")
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
            print("@@",e)
            return render_template('kidney.html',prediction_text="Some unknown error occured please input the values in number or contact the develpor if it still occurs")
        pc_=request.form['pc']
        if pc_=='normal':
            pc_normal=1
            pc_nan=0
        elif pc_=='nan':
            pc_normal=0
            pc_nan=1
        else:
            pc_normal=0
            pc_nan=0
        pcc_=request.form['pcc']
        if pcc_=='present':
            pcc_present=1
        else:
            pcc_present=0
        ba_=request.form['ba']
        if ba_=='present':
            ba_present=1
        else:
            ba_present=0    
        htn_=request.form['htn']
        if htn_=='yes':
            htn_yes=1
        else:
            htn_yes=0
        dm_=request.form['dm']
        if dm_=='yes':
            dm_no=0
            dm_yes=1
        else:
            dm_no=0
            dm_yes=0

        cad_=request.form['cad']
        if cad_=='yes':
            cad_yes=1
        else:
            cad_yes=0
        appet_=request.form['appet']
        if appet_=='poor':
            appet_poor=1
        else:
            appet_poor=0
        pe_=request.form['pe']
        if pe_=='yes':
            pe_yes=1
        else:
            pe_yes=0
        ane_=request.form['ane']
        if ane_=='yes':
            ane_yes=1
        else:
            ane_yes=0
        rbc_=request.form['rbc']
        if rbc_=='normal':
            rbc_normal=1
            rbc_nan=0
        elif rbc_=='nan':
            rbc_normal=0
            rbc_nan=1
        else:
            rbc_normal=0
            rbc_nan=0
        X=pd.DataFrame([[age, bp, sg, al, su, bgr, bu, sc, sod, pot, hemo,pcv, wc, rc, rbc_normal, rbc_nan, pc_normal, pc_nan,pcc_present, ba_present, htn_yes, dm_no, dm_yes, cad_yes,appet_poor, pe_yes, ane_yes]],columns=['age', 'bp', 'sg', 'al', 'su', 'bgr', 'bu', 'sc', 'sod', 'pot', 'hemo','pcv', 'wc', 'rc', 'rbc_normal', 'rbc_nan', 'pc_normal', 'pc_nan','pcc_present', 'ba_present', 'htn_yes', 'dm_no', 'dm_yes', 'cad_yes','appet_poor', 'pe_yes', 'ane_yes'])

        X_col=X.columns[[ True,  True, False,  True, False,  True,  True,  True,  True,True,  True,  True,True,  True,  True,  True,  True, False,False, False,  True, False,  True,  True, False, False,True]]
        output=model.predict(X[X_col])
        if output==0:
            return render_template('kidney.html',prediction_text="Result: \nPrediction Result: Don't worry You don't have any Kidney disease!")
        elif output==1:
            return render_template('kidney.html',prediction_text="Result: \nWe found something wrong with your kidney, please consult with the doctor")


# ...................................Health APP Ended.................................................
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)