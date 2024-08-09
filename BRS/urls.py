from django.urls import path, include
from .views import welcome, home, preference, addBook, clear_preference, showcase

urlpatterns = [
    path('user/', include('User.urls')),
    path("", welcome, name="welcome"),
    path("home/", home, name="home"),
    path("preference/", preference, name="preference"),
    path("clear_preference/", clear_preference, name="clear_preference"),
    path("addBook/", addBook, name="addBook"),
    path("showcase/", showcase, name="showcase"),
]
