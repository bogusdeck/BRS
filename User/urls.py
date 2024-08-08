from django.urls import path
from .views import SignUpGUIView, LoginGUIView, LogoutGUIView
from .views import SignUpAPIView, LoginAPIView, LogoutAPIView

urlpatterns = [
    # HTML Form URLs
    path('signup/', SignUpGUIView, name='signup'),
    path('signin/', LoginGUIView, name='signin'),
    path('logout/', LogoutGUIView, name='logout'),

    # API URLs
    path('api/signup/', SignUpAPIView.as_view(), name='signup_api'),
    path('api/login/', LoginAPIView.as_view(), name='login_api'),
    path('api/logout/', LogoutAPIView.as_view(), name='logout_api'),
]
