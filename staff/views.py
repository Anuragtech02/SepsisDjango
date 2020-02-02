from django.shortcuts import render
from .forms import TestReportForms
from .models import TestReport
import pyrebase
from django.contrib import auth
import pyrebase
from django.contrib import auth
import time
from datetime import datetime, timezone
import pytz
# import numpy as np
# import pickle


# import pandas as pd

# import joblib


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


def classify(unit):
    try: 
        print (unit)
        mdl=joblib.load('C:/Users/hp/Desktop/SIH 2020/sepsis/sepsis/sepsis.pkl')
        
        y_predict=mdl.predict(unit)
       
        return y_predict
    except ValueError as e:
        print (e.args[0]) 


def test(request):
    # if request.method=='POST':
    #     form=TestReportForms(request.POST)
    #     if form.is_valid():
    #         obj=form.save()
    #         print(form.cleaned_data)
    #         Age=form.cleaned_data.get('Age')
    #         SBP=form.cleaned_data.get('SBP')
    #         DBP=form.cleaned_data.get('DBP')
    #         Resp=form.cleaned_data.get('Resp')
    #         Temp=form.cleaned_data.get('Temp')
    #         O2Sat=form.cleaned_data.get('O2Sat')
    #         HR=form.cleaned_data.get('HR')
    #         MAP=(((2*float(DBP))+float(SBP))/3)
    #         obj.MAP=(((2*float(DBP))+float(SBP))/3)
    #         obj.save()
    if request.method=='POST':
        form=TestReportForms(request.POST)
        if form.is_valid():
            obj=form.save(commit=False)
            
            print(form.cleaned_data)
            Age=form.cleaned_data.get('Age')
            nage=Age- 63.016672/16.130546            
            SBP=form.cleaned_data.get('SBP')
            nsbp=SBP-119.280812/20.183439





            DBP=form.cleaned_data.get('DBP')
            ndbp= DBP- 57.581449/9.384823
            Resp=form.cleaned_data.get('Resp')
            nrsp=Resp- 18.500810/5.186035
            Temp=form.cleaned_data.get('Temp')
            ntemp=Temp- 98.615987/0.816691
            O2Sat=form.cleaned_data.get('O2Sat')
            no2sat=O2Sat-97.592653/2.868536
            HR=form.cleaned_data.get('HR')
            nhr=HR- 84.578042/16.325395
            MAP=(((2*DBP)+SBP)/3)
            print(MAP)
            obj.MAP=(((2*DBP)+SBP)/3)
            nmap=MAP-78.02193/14.392553
            obj.save()
        
            myDict = {
                "Age":nage,
                "Resp":nrsp,
                "SBP":nsbp,
                "MAP":nmap,
                "HR": nhr,
                "DBP": ndbp,
                "Temp": ntemp,
                "O2Sat": no2sat




            }
            print (myDict)
            df=pd.DataFrame(myDict, index=[0])  
            print (df)
            answer= classify(df)
            

            if (answer > 0.045 ):
                print (" You May Hav Sepsis")
                message="You Have Sepsis"
                return render(request,"test.html",{"msg":message})
            
            elif(Resp> 20 and SBP >80 and DBP >120 and Temp >100 or Temp< 94 and HR>90):
                print ("You May Have Sepsis")
                message="You Have Sepsis"
                return render(request,"test.html",{"msg":message})
            
            else:
                print ("You Don't Have Sepsis ")   
                message="You Dont Have Sepsis"
                return render(request,"test.html",{"msg":message})
        
            data = {
                     "Age":Age,
                     'SBP':SBP,
                     'DBP':DBP,
                     'MAP':MAP,
                    'O2Sat':O2Sat,
                     'HR':HR,
                     'Temp':Temp,
                     'Resp':Resp
                    }
            database.child('SIRS').child('name').set(data)
        no=request.POST.get('no')
        import requests
        import json
        # URL = 'https://www.sms4india.com/api/v1/sendCampaign'
        # def sendPostRequest(reqUrl, apiKey, secretKey, useType, phoneNo, senderId, textMessage):
        #         req_params = {
        #         'apikey':apiKey,
        #         'secret':secretKey,
        #         'usetype':useType,
        #         'phone': phoneNo,
        #         'message':textMessage,
        #         'senderid':senderId
        #         }
        #         return requests.post(reqUrl, req_params)
    

        
        # response = sendPostRequest(URL, 'OZ9VM8YDPSZWL6MAAM39CBKGL3XUPVPT', 'O0FXKYZ1866Y6Q1E', 'stage', no, 'somufiit@gmail.com', 'Your Report will be shown here')
        # print (response.text)

    else:        
        form=TestReportForms()
    return render(request,"test.html",{"form":form})
def sign(request):
    return render(request,"docsignIn.html")
def postsign(request):
    email=request.POST.get('email')
    password=request.POST.get('password')

    try:
        staff = authe.sign_in_with_email_and_password(email,password)
    except:
        message = "invalid cerediantials"
        return render(request,"docsignIn.html",{"msg":message})
    print(staff['idToken'])
    session_id=staff['idToken']
    request.session['uid']=str(session_id)
    idtoken= request.session['uid']
    uid = staff['localId']
   # name = database.child('users').child('details').child(uid).child('name').get().val()
    return render(request, "docwelcome.html")   
def logout(request):
    auth.logout(request)
    return render(request,'docsignIn.html')
def signUp(request):
    return render(request,"docsignup.html") 
def postsignup(request):
    name=request.POST.get('name')
    email=request.POST.get('email')
    password=request.POST.get('password')
    empno=request.POST.get('empno')
    password1=request.POST.get('password1')
    if password==password1 :
       try:
         staff=authe.create_user_with_email_and_password(email,password)
         uid = staff['localId']
         data={"name":name,"username":email,"password":password,"empno":empno}
         database.child('staff').child("details").child(uid).set(data)
       except:
         message="Unable to create account try again"
         return render(request,"docsignup.html",{"msg":message})
    else :
        message="Password did not match"
        return render(request,"docsignup.html",{"msg":message})     
    return render(request,"docsignIn.html")

