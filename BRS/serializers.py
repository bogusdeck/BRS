# serializers.py
from rest_framework import serializers
from User.models import Books, CustomUser


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = ['title', 'author', 'self_rating', 'genre', 'description', 'cover_image']

class SearchBooksSerializer(serializers.Serializer):
    query = serializers.CharField(required=True, max_length=255)
    genre = serializers.CharField(required=False, max_length=100)
    author = serializers.CharField(required=False, max_length=255)
    rating = serializers.DecimalField(required=False, max_digits=2, decimal_places=1)
    sort = serializers.CharField(required=False, default="relevance")

class PreferenceSerializer(serializers.Serializer):
    preferences = serializers.ListField(child=serializers.CharField(max_length=3))  # Code length of 3
