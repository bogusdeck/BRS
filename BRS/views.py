from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
# from api.models import User


'''

                welcome  
                   |
                   v
     login<--------------->signup
        |
        v
      home -----> search
        |
        v
     AddBook

'''

def welcome(request):
    return render(request,"welcome.html")

@login_required
def home(request):
    return render(request,"home.html")

@login_required
def search(request):
    return render(request, "search.html") 

@login_required
def addBook(request):
    return render(request, "addBook.html")




