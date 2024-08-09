from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from User.forms import BookForm
from User.models import Books, CustomUser

from BRS.services import fetch_books, fetch_book_for_preference
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from User.models import Books
from .serializers import BookSerializer, SearchBooksSerializer, PreferenceSerializer
from rest_framework.exceptions import ValidationError

"""

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
"""
CATEGORY_CODES = {
    "FIC": "Fiction",
    "NF": "Non-Fiction",
    "SF": "Science Fiction",
    "FAN": "Fantasy",
    "MYS": "Mystery",
    "THR": "Thriller",
    "ROM": "Romance",
    "HIS": "Historical",
    "BIO": "Biography",
    "SH": "Self-Help",
    "YA": "Young Adult",
    "CH": "Children's",
    "HOR": "Horror",
    "CLA": "Classic",
    "POE": "Poetry",
}

class GetTokenAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        return Response({'token': user.token})

def Welcome(request):
    return render(request, "welcome.html")


def process_books(response_json):
    return response_json.get("items", [])


def Home(request):
    if not request.user.is_authenticated:
        messages.info(request, "You need to log in first.")
        return redirect("signin")

    api_key = settings.GOOGLE_BOOKS_API_KEY
    user_preference = request.user.preference
    try:
        trending_books_response = fetch_books("trending", api_key, 10)
        all_time_favorites_response = fetch_books("bestsellers", api_key, 12)
        if not user_preference:
            user_recommendations = []
        else:
            recommended_book_response = fetch_book_for_preference(
                user_preference, api_key
            )
            user_recommendations = process_books({"items": recommended_book_response})

        trending_books = process_books(trending_books_response)
        all_time_favorites = process_books(all_time_favorites_response)
        user_added_books = Books.objects.all()
        context = {
            "trending_books": trending_books,
            "all_time_favorites": all_time_favorites,
            "user_recommendations": user_recommendations,
            "user_added_books": user_added_books,
        }

    except Exception as e:
        messages.error(request, f"An error occured: {e}")
        context = {}

    return render(request, "home.html", context)


def UpdatePreferenceGUIView(request):
    if not request.user.is_authenticated:
        messages.info(request, "You need to log in first.")
        return redirect("signin")

    if request.method == "POST":
        selected_categories = request.POST.get("categories", "")
        selected_categories_list = (
            list(set(selected_categories.split(","))) if selected_categories else []
        )
        user = request.user
        user.preference = selected_categories_list
        user.save()
        messages.success(request, "Preferences updated successfully!")
        return redirect("home")

    categories = [
        "Fiction",
        "Non-Fiction",
        "Science Fiction",
        "Fantasy",
        "Mystery",
        "Thriller",
        "Romance",
        "Historical",
        "Biography",
        "Self-Help",
        "Young Adult",
        "Children's",
        "Horror",
        "Classic",
        "Poetry",
    ]

    selected_categories = request.user.preference or []

    return render(
        request,
        "preference.html",
        {
            "categories": categories,
            "selected_categories": selected_categories,
        },
    )


@login_required
def ClearPreference(request):
    user = request.user
    user.preference = []
    user.save()
    messages.success(request, "All preferences have been cleared!")
    return redirect("preference")


def SearchBooksGUIView(request):
    query = request.GET.get("query", "")
    genre = request.GET.get("genre", "")
    author = request.GET.get("author", "")
    rating = request.GET.get("rating", "")
    sort = request.GET.get("sort", "relevance")
    page_number = request.GET.get("page", 1)

    if author:
        query = author

    filters = {
        "q": query,
        "genre": genre,
        "author": author,
        "rating": rating,
        "sort": sort,
    }

    api_key = settings.GOOGLE_BOOKS_API_KEY
    default_image = "/static/default_for_cover.jpg"

    search_params = []
    if query:
        search_params.append(f"intitle:{query}")
    if genre:
        search_params.append(f"subject:{genre}")
    if author:
        search_params.append(f"inauthor:{author}")
    if rating:
        search_params.append(f"averageRating:{rating}")

    search_query = "+".join(search_params)

    books = []
    total_items = 0

    if search_query:
        try:
            start_index = 0
            max_results = 10
            fetched_books = []
            while True:
                response = fetch_books(search_query, api_key, max_results, start_index)
                items = response.get("items", [])
                total_items = response.get("totalItems", 0)
                fetched_books.extend(items)
                if len(items) < max_results:
                    break
                start_index += max_results

            if sort == "title_asc":
                fetched_books.sort(
                    key=lambda x: x.get("volumeInfo", {}).get("title", "").lower()
                )
            elif sort == "title_desc":
                fetched_books.sort(
                    key=lambda x: x.get("volumeInfo", {}).get("title", "").lower(),
                    reverse=True,
                )

            paginator = Paginator(fetched_books, per_page=max_results)
            try:
                books = paginator.page(page_number)
            except PageNotAnInteger:
                books = paginator.page(1)
            except EmptyPage:
                books = paginator.page(paginator.num_pages)

        except Exception as e:
            messages.error(request, f"An error occurred: {e}")

    context = {
        "books": books,
        "query": query,
        "default_image": default_image,
        "selected_genre": genre,
        "selected_author": author,
        "selected_rating": rating,
        "selected_sort": sort,
        "total_items": total_items,
    }

    return render(request, "showcase.html", context)


@login_required
def AddBookGUIView(request):
    if not request.user.is_authenticated:
        messages.info(request, "You need to log in first.")
        return redirect("signin")

    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            fname = request.user.fname
            lname = request.user.lname
            name = fname + " " + lname
            book = Books(
                title=form.cleaned_data["title"],
                author=form.cleaned_data["author"],
                self_rating=form.cleaned_data["self_rating"],
                genre=form.cleaned_data["genre"],
                description=form.cleaned_data["description"],
                cover_image=form.cleaned_data["cover_image"],
                user_email=request.user.email,
                user_name=name,
            )
            book.save()
            return redirect("home")
            messages.success(request, "Book added Successfully")
    else:
        form = BookForm()

    return render(request, "addBook.html", {"form": form})


class AddBookAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            if serializer.is_valid():
                book = serializer.save(user_email=request.user.email, user_name=f"{request.user.fname} {request.user.lname}")
                return Response({'message': 'Book added successfully'}, status=status.HTTP_201_CREATED)
            raise ValidationError(serializer.errors)
        except ValidationError as e:
            return Response({'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SearchBooksAPIView(APIView):
    def get(self, request, *args, **kwargs):
        serializer = SearchBooksSerializer(data=request.GET)
        if serializer.is_valid():
            query = serializer.validated_data.get("query")
            genre = serializer.validated_data.get("genre", "")
            author = serializer.validated_data.get("author", "")
            rating = serializer.validated_data.get("rating", "")
            sort = serializer.validated_data.get("sort", "relevance")

            search_params = []
            if query:
                search_params.append(f"intitle:{query}")
            if genre:
                search_params.append(f"subject:{genre}")
            if author:
                search_params.append(f"inauthor:{author}")
            if rating:
                search_params.append(f"averageRating:{rating}")

            search_query = "+".join(search_params)
            api_key = settings.GOOGLE_BOOKS_API_KEY

            try:
                response = fetch_books(search_query, api_key, 10)
                return Response(response, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdatePreferenceAPIView(APIView):
    def post(self, request, *args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(token=token)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PreferenceSerializer(data=request.data)
        if serializer.is_valid():
            codes = serializer.validated_data['preferences']
            # Convert codes to category names
            preferences = [CATEGORY_CODES.get(code, code) for code in codes]
            user.preference = preferences
            user.save()
            return Response({'message': 'Preferences updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FindBooksByPreferenceAPIView(APIView):
    def get(self, request, *args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(token=token)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        preferences = user.preference
        if not preferences:
            return Response({'error': 'No preferences found'}, status=status.HTTP_400_BAD_REQUEST)

        api_key = settings.GOOGLE_BOOKS_API_KEY
        total_books = 20
        books_per_preference = max(1, total_books // len(preferences))
        books_by_preference = []
        seen_books = set()

        for preference in preferences:
            search_query = f"subject:{preference}"
            try:
                fetched_books = fetch_books(search_query, api_key, books_per_preference)
                for book in fetched_books.get("items", []):
                    book_id = book.get("id")
                    if book_id not in seen_books:
                        books_by_preference.append(book)
                        seen_books.add(book_id)
                        if len(books_by_preference) >= total_books:
                            break
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            if len(books_by_preference) >= total_books:
                break

        return Response({
            'books': books_by_preference,
            'total_books_fetched': len(books_by_preference)
        }, status=status.HTTP_200_OK)


class GetPreferencesAPIView(APIView):
    def get(self, request, *args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(token=token)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        preferences = user.preference

        return Response({'preferences': preferences}, status=status.HTTP_200_OK)

class GetUserBooksAPIView(APIView):
    def get(self, request, *args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(token=token)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        books = Books.objects.filter(user_email=user.email)
        books_data = [
            {
                'title': book.title,
                'author': book.author,
                'self_rating': book.self_rating,
                'genre': book.genre,
                'description': book.description,
                'cover_image': request.build_absolute_uri(book.cover_image.url) if book.cover_image else None,
            }
            for book in books
        ]

        return Response({'books': books_data}, status=status.HTTP_200_OK)


class GetAllBooksAPIView(APIView):
    def get(self, request, *args, **kwargs):
        books = Books.objects.all()
        books_data = [
            {
                'title': book.title,
                'author': book.author,
                'self_rating': book.self_rating,
                'genre': book.genre,
                'description': book.description,
                'cover_image': request.build_absolute_uri(book.cover_image.url) if book.cover_image else None,
                'user_email': book.user_email,
                'user_name': book.user_name,
            }
            for book in books
        ]

        return Response({'books': books_data}, status=status.HTTP_200_OK)
