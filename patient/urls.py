from django.conf.urls import url
from django.contrib import admin
from.import views
from django.urls import path 

urlpatterns = [
    path("sign",views.sign,name="patsignIn"),
    path("postsign",views.postsign),
    path("logout",views.logout,name="log"),
    path("signup",views.signUp,name='patsignup'),
    path("postsignup",views.postsignup,name='postsignup'),
    path("check", views.check, name="naman"),
    path("capture", views.open, name="mehra")
    
]

