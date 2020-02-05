from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request,"home.html")
def p(request):
    return render(request,"prevention.html")   
def a(request):
    return render(request, "index.html")
def s(request):
    message="Please Login"
    return render(request,"home.html",{"msg":message})     