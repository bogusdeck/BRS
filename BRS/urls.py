from django.urls import path, include
from .views import welcome, home, search, addBook

urlpatterns = [
    path('user/', include('User.urls')),
    # path('',),
    path("", welcome, name="welcome"),
    path("home/", home, name="home"),
    path("search/", search, name="search"),
    path("addBook/", addBook, name="addBook"),
]
