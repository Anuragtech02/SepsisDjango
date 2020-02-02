from django.conf.urls import url
from django.contrib import admin
from.import views
from django.urls import path 

urlpatterns = [
    path("sign",views.sign,name="signIn"),
    path("postsign",views.postsign),
    path("logout",views.logout,name="logo"),
    path("signup",views.signUp,name='signup'),
    path("postsignup",views.postsignup,name='postsignup'),
    path("test",views.test,name='t'),
    
]
