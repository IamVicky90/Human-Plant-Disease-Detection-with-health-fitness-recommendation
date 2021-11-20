from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array,load_img
import numpy as np
import os
def pred_pnemoian(img_path):
    model=load_model(os.path.join("Model","Chest XRay Pnemonia xception model.h5"))
    img=load_img(img_path,target_size=(224,224))
    x=img_to_array(img)/225
    x=np.expand_dims(x, axis=0)
    pred=model.predict(x)
    output=np.argmax(pred,axis=1)
    if output==0:
        return "Prediction Result: Don't worry You don't have any disease!"
    elif output==1:
        return "We found that you have Pnemonia disease please consult with the doctor"
def pred_plant_dieas(plant):
  model=load_model(os.path.join("Model","Various Plant Disease Detection Model1.h5"))
  test_image = load_img(plant, target_size = (150, 150)) # load image 
  test_image = img_to_array(test_image)/255 
  test_image = np.expand_dims(test_image, axis = 0) # change dimention 3D to 4D
   
  result = model.predict(test_image).round(3) 
   
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
def pred_skin(img_path):
    
    model=load_model(os.path.join("Model","skin cancer vgg16 model.h5"))
    img=load_img(img_path,target_size=(224,224))
    x=img_to_array(img)/225
    x=np.expand_dims(x, axis=0)
    pred=model.predict(x)
    output=np.argmax(pred,axis=1)
    if output==0:
        return "Prediction Result: Don't worry You don't have any disease!"
    elif output==1:
        return "We found that you have skin cancer, please consult with the doctor"