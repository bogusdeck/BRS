from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from .views import Welcome, Home, UpdatePreferenceGUIView, AddBookGUIView, ClearPreference, SearchBooksGUIView

from .views import AddBookAPIView, SearchBooksAPIView, UpdatePreferenceAPIView, GetTokenAPIView,FindBooksByPreferenceAPIView, GetPreferencesAPIView,GetUserBooksAPIView, GetAllBooksAPIView

urlpatterns = [
    path('user/', include('User.urls')),
    path("", Welcome, name="welcome"),
    path("home/", Home, name="home"),
    path("preference/", UpdatePreferenceGUIView, name="preference"),
    path("clear_preference/", ClearPreference, name="clear_preference"),
    path("addBook/", AddBookGUIView, name="addBook"),
    path("showcase/", SearchBooksGUIView, name="showcase"),
    
    path('api/add_book/', AddBookAPIView.as_view(), name='add_book_api'),
    path('api/update_preference/', UpdatePreferenceAPIView.as_view(), name='update_preference_api'),
    path('api/search_books/', SearchBooksAPIView.as_view(), name='search_book_api'),
    path('api/get_token/', GetTokenAPIView.as_view(), name='get_token'),
    path('api/get_preferences/', GetPreferencesAPIView.as_view(), name='get_preferences'),
    path('api/find_books_by_preference/', FindBooksByPreferenceAPIView.as_view(), name='find_books_by_preference'),
    path('api/get_user_books/', GetUserBooksAPIView.as_view(), name='get_user_books'),
    path('api/get_all_books/', GetAllBooksAPIView.as_view(), name='get_all_books'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
