from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages

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
    return render(request, "welcome.html")

def home(request):
    if not request.user.is_authenticated:
        messages.info(request, "You need to log in first.")
        return redirect('signin')
    return render(request, "home.html")

def search(request):
    if not request.user.is_authenticated:
        messages.info(request, "You need to log in first.")
        return redirect('signin')
    return render(request, "search.html")

def addBook(request):
    if not request.user.is_authenticated:
        messages.info(request, "You need to log in first.")
        return redirect('signin')
    return render(request, "addBook.html")


