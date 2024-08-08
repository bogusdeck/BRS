from rest_framework import serializers
from .models import CustomUser
from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['fname', 'lname', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            fname=validated_data['fname'],
            lname=validated_data['lname'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['email', 'password']

    

class LogoutSerializer(serializers.Serializer):
    token = serializers.CharField()

    # def validate(self, data):
    #   token = data.get("token", None)
    #   token = token.lower()
    #   print(token)
    #   user = None
    #   try:
    #       user = CustomUser.objects.get(token=token)
    #       if not user.ifLogged:
    #           raise ValidationError("User is not logged in.")
    #   except Exception as e:
    #       raise ValidationError(str(e))
    #   user.ifLogged = False
    #   user.token = ""
    #   user.save()
    #   return user

    class Meta:
        model = CustomUser
        fields = ['token']
