from django.shortcuts import render
import pyrebase
from django.contrib import auth
import time
from datetime import datetime, timezone
#import cv2
import numpy as np
# import pickle
from os import listdir
from os.path import  isfile, join
import pytz
config = {
   'apiKey': "AIzaSyC6jNBg8QlyHA3cLH0w0TeJzObkslzdpzE",
   'authDomain': "patient-da06d.firebaseapp.com",
   'databaseURL': "https://patient-da06d.firebaseio.com",
   'projectId': "patient-da06d",
   'storageBucket': "patient-da06d.appspot.com",
   'messagingSenderId': "60282937045",
}
firebase = pyrebase.initialize_app(config);
authe = firebase.auth()
database=firebase.database()
def sign(request):
    return render(request,"signIn.html")
def postsign(request):
    email=request.POST.get('email')
    password=request.POST.get('password')
    try:
        user= authe.sign_in_with_email_and_password(email,password)
    except:
        message = "invalid cerediantials"
        return render(request,"signIn.html",{"msg":message})
    print(user['idToken'])
    session_id=user['idToken']
    request.session['uid']=str(session_id)
    idtoken= request.session['uid']
    uid = user['localId']
    nam = database.child('users').child('details').child(uid).child('name').get().val()
    a = database.child('SIRS').child('name').child('age').get().val()
    b = database.child('SIRS').child('name').child('SBP').get().val()
    c = database.child('SIRS').child('name').child('DBP').get().val()
    d = database.child('SIRS').child('name').child('Resp').get().val()
    e = database.child('SIRS').child('name').child('Temp').get().val()
    f = database.child('SIRS').child('name').child('O2Sat').get().val()
    return render(request, "welcome.html",{"a":a,"b":b,"c":c,"d":d,"e":e,"f":f ,"n":nam})   
def logout(request):
    auth.logout(request)
    return render(request,'signIn.html')
def signUp(request):
    return render(request,"signup.html") 
def postsignup(request):
    name=request.POST.get('name')
    email=request.POST.get('email')
    number=request.POST.get('number')
    gender=request.POST.get('gender')
    password=request.POST.get('password')
    try:
       user=authe.create_user_with_email_and_password(email,password)
       uid = user['localId']
       data={"name":name,"email":email,"number":number,"gender":gender,"status":"1"}
       database.child('users').child("details").child(uid).set(data)
    except:
        message="Unable to create account try again"
        return render(request,"signup.html",{"msg":message})
    return render(request,"signIn.html")


def check(request):
    
    model=cv2.face.LBPHFaceRecognizer_create()
    

    data_path='C:/Users/hp/Desktop/project 1/face recog/'
    only_face= [f for f in listdir(data_path) if isfile (join(data_path,f))]
    training_data, labels=[],[]

    for i , files in enumerate(only_face):
        images_path= data_path+ only_face[i]
        images= cv2.imread(images_path, cv2.IMREAD_GRAYSCALE)
        training_data.append(np.asarray(images,dtype= np.uint8))

        labels.append(i)
    labels= np.asarray(labels, dtype=np.int32)
    model.train(np.asarray(training_data),np.asarray(labels))
    print ('trained')



  





    face_classifier = cv2.CascadeClassifier('C:/ProgramData/Anaconda3/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml')

    def face_detector(img1, size = 0.5):
        gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        faces1 = face_classifier.detectMultiScale(gray,1.3,5)

        if faces1 is():
            return img1,[]

        for(x,y,w,h) in faces1:
            cv2.rectangle(img1, (x,y),(x+w,y+h),(0,255,255),2)
            roi = img1[y:y+h, x:x+w]
            roi = cv2.resize(roi, (200,200))

            return img1,roi

    cap = cv2.VideoCapture(0)
    while True:

        ret, frame1 = cap.read()

        image, face1 = face_detector(frame1)

        try:
            face1 = cv2.cvtColor(face1, cv2.COLOR_BGR2GRAY)
            result = model.predict(face1)

            if result[1] < 500:
                confidence = int(100*(1-(result[1])/300))
                display_string = str(confidence)+'% Confidence it is user'
            cv2.putText(image,display_string,(100,120), cv2.FONT_HERSHEY_COMPLEX,1,(250,120,255),2)
            

            if confidence > 85:
                cv2.putText(image, "Unlocked", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                cv2.imshow('Face Cropper', image)

                # session_id=user['idToken']
                # request.session['uid']=str(session_id)
                # idtoken= request.session['uid']
                # uid = user['localId']
                # nam = database.child('users').child('details').child(uid).child('name').get().val()
                # a = database.child('SIRS').child('name').child('age').get().val()
                # b = database.child('SIRS').child('name').child('SBP').get().val()
                # c = database.child('SIRS').child('name').child('DBP').get().val()
                # d = database.child('SIRS').child('name').child('Resp').get().val()
                # e = database.child('SIRS').child('name').child('Temp').get().val()
                # f = database.child('SIRS').child('name').child('O2Sat').get().val()


                return render(request , "welcome.html")

            else:
                cv2.putText(image, "Locked", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
                cv2.imshow('Face Cropper', image)


        except:
            cv2.putText(image, "Face Not Found", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
            
            cv2.imshow('Face Cropper', image)
            pass

            
        if cv2.waitKey(1)==13:
            break





    cap.release()
    cv2.destroyAllWindows()

    return render(request, "abc.html")

def open(request):
    face_classifier=cv2.CascadeClassifier("C:/ProgramData/Anaconda3/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml")
    cap=cv2.VideoCapture(0)

    count=0

    def face_extracter(img):
        gray_img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces=face_classifier.detectMultiScale(gray_img,1.3,5)

        if faces is ():
            return None

        for (x,y,z,w) in faces:
            cropped_faces= img[y:y+w, x:x+z]
        return cropped_faces

    while True:
        ret, frame = cap.read()

        if face_extracter(frame) is not None:
            count+=1
            face = cv2.resize(face_extracter(frame),(200,200))
            face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        
            file_name_path = "C:/Users/hp/Desktop/project 1/face recog/digit"+str(count)+".jpg"
            cv2.imwrite(file_name_path, face)
            cv2.putText(face, str(count), (50,50),cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0),2)
        
            cv2.imshow("face_cropper", face)
        
        else:
            print("Face not found ")
            pass
     
        
        if cv2.waitKey(1)==13 or count==100:
            break

    cap.release()
    cv2.destroyAllWindows
    print ('Collecting samples completed')      
    return render (request, "signup.html")
