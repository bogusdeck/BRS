from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.views.generic import View
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework.generics import CreateAPIView
from .models import CustomUser
from .serializers import UserSerializer, LoginSerializer, LogoutSerializer
from rest_framework.views import APIView
from uuid import uuid4
from .forms import UserLoginForm, UserLogoutForm, UserSignupForm
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required




# SignUp API
class SignUpAPIView(CreateAPIView):
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return redirect('signup')  
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            if serializer.is_valid():
                user = serializer.save()
                return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
            raise ValidationError(serializer.errors)
        except ValidationError as e:
            return Response({'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Login API

class LoginAPIView(CreateAPIView):
    serializer_class = LoginSerializer
    
    def get(self, request, *args, **kwargs):
        return redirect('signin')  

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            if serializer.is_valid():
                email = serializer.validated_data['email']
                password = serializer.validated_data['password']
                user = authenticate(request, email=email, password=password)
                if user is not None:
                    login(request, user)

                    new_token = str(uuid4())
                    user.token = new_token
                    user.save() 

                    return Response({
                        'message': 'Login successful',
                        'token': new_token,
                    }, status=status.HTTP_200_OK)

                raise AuthenticationFailed('Invalid credentials')
                
            raise ValidationError(serializer.errors)
        except AuthenticationFailed as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except ValidationError as e:
            return Response({'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Logout API
class LogoutAPIView(CreateAPIView):
    serializer_class = LogoutSerializer

    def get(self, request, *args, **kwargs):
        return redirect('home')  

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        user = None
        if serializer.is_valid():
            token = serializer.validated_data['token']
            token = token.lower()
            user = CustomUser.objects.get(token=token) 
            print(user)
            user.token = ""
            user.save()
            logout(request)  
            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# SignUp View
def LoginGUIView(request,user=None):
    if request.user.is_authenticated:
        messages.info(request, 'LogOut first')
        return redirect('home')

    if request.method=="POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email=form.cleaned_data["email"]
            password=form.cleaned_data["password"]
            print(email, password)
            # user = CustomUser.objects.get(email=email)
            # print(check_password(password, user.password))
            user = authenticate(request, email=email, password=password)
            print(user)
            # if user = authenticate(request, email=email, password=password):
            if user is not None:
                login(request,user=user)
                new_token = str(uuid4())
                user.token = new_token
                user.save() 
                # return redirect("/home/{}".format(user.email))
                return redirect("home")
            else:
                print("nahi hua")
                messages.error(request, "Invalid  email or password")
                return redirect("signin")
    else:
        form = UserLoginForm()

    return render(request, "signin.html", {"form":form})

def SignUpGUIView(request):
    if request.user.is_authenticated:
        messages.info(request, 'LogOut first')
        return redirect('home')

    if request.method == "POST":
        form = UserSignupForm(request.POST)
        if form.is_valid():
            fname = form.cleaned_data["fname"]
            lname = form.cleaned_data["lname"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user_to_create = CustomUser(
                fname= fname, lname=lname, email=email, password=password
            )
            user_to_create.save()
            print(user_to_create)
            print(fname, lname, email, password)
            print("account bn gaya")
            messages.success(request, "account created successfully, please login")
            return redirect("signin")
    else:
        form = UserSignupForm()

    return render(request, "signup.html", {"form":form})

@login_required
def LogoutGUIView(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, "You have been logged out successfully.")
        return redirect('signin')  

