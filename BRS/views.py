from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages

from User.models import Category

from BRS.services import fetch_books, fetch_book_for_preference
from django.conf import settings

# from api.models import User


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


def welcome(request):
    return render(request, "welcome.html")


# Example of processing response
def process_books(response_json):
    return response_json.get("items", [])


# Example view function
def home(request):
    if not request.user.is_authenticated:
        messages.info(request, "You need to log in first.")
        return redirect("signin")

    api_key = settings.GOOGLE_BOOKS_API_KEY
    user_preference = request.user.preference  
    try:
        trending_books_response = fetch_books("trending", api_key, 12)
        all_time_favorites_response = fetch_books("bestsellers", api_key, 12)
        if not user_preference:
            user_recommendations = []
        else:
            recommended_book_response = fetch_book_for_preference(user_preference, api_key)
            user_recommendations = process_books({"items": recommended_book_response})

        trending_books = process_books(trending_books_response)
        all_time_favorites = process_books(all_time_favorites_response)

        context = {
            "trending_books": trending_books,
            "all_time_favorites": all_time_favorites,
            "user_recommendations": user_recommendations,
        }

    except Exception as e:
        messages.error(request,f"An error occured: {e}")
        context = {}

    return render(request, "home.html", context)


def preference(request):
    if not request.user.is_authenticated:
        messages.info(request, "You need to log in first.")
        return redirect("signin")

    if request.method == "POST":
        selected_categories = request.POST.get(
            "categories", ""
        )  
        selected_categories_list = (
            list(set(selected_categories.split(","))) if selected_categories else []
        )
        user = request.user
        user.preference = selected_categories_list
        user.save()
        messages.success(request, "Preferences updated successfully!")
        return redirect("home")

    # List of categories
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
def clear_preference(request):
    user = request.user
    user.preference = []
    user.save()
    messages.success(request, "All preferences have been cleared!")
    return redirect('preference')

def addBook(request):
    if not request.user.is_authenticated:
        messages.info(request, "You need to log in first.")
        return redirect("signin")
    return render(request, "addBook.html")
