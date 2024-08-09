from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from User.models import Category

from BRS.services import fetch_books, fetch_book_for_preference
from django.conf import settings


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


def process_books(response_json):
    return response_json.get("items", [])


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
            recommended_book_response = fetch_book_for_preference(
                user_preference, api_key
            )
            user_recommendations = process_books({"items": recommended_book_response})

        trending_books = process_books(trending_books_response)
        all_time_favorites = process_books(all_time_favorites_response)

        context = {
            "trending_books": trending_books,
            "all_time_favorites": all_time_favorites,
            "user_recommendations": user_recommendations,
        }

    except Exception as e:
        messages.error(request, f"An error occured: {e}")
        context = {}

    return render(request, "home.html", context)


def preference(request):
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
def clear_preference(request):
    user = request.user
    user.preference = []
    user.save()
    messages.success(request, "All preferences have been cleared!")
    return redirect("preference")


def addBook(request):
    if not request.user.is_authenticated:
        messages.info(request, "You need to log in first.")
        return redirect("signin")
    return render(request, "addBook.html")



def showcase(request):
    query = request.GET.get('query', '')
    genre = request.GET.get('genre', '')
    author = request.GET.get('author', '')
    rating = request.GET.get('rating', '')
    sort = request.GET.get('sort', 'relevance')
    page_number = request.GET.get('page', 1)

    if author: 
        query = author

    filters = {
        'q': query,
        'genre': genre,
        'author': author,
        'rating': rating,
        'sort': sort,
    }
    
    api_key = settings.GOOGLE_BOOKS_API_KEY
    default_image = "/static/default_for_cover.jpg"
    
    # Construct search parameters
    search_params = []
    if query:
        search_params.append(f"intitle:{query}")
    if genre:
        search_params.append(f"subject:{genre}")
    if author:
        search_params.append(f"inauthor:{author}")
    if rating:
        search_params.append(f"averageRating:{rating}")

    search_query = '+'.join(search_params)
    
    books = []
    total_items = 0
    
    if search_query:
        try:
            # Fetch books in chunks and manage pagination
            start_index = 0
            max_results = 10
            fetched_books = []
            while True:
                response = fetch_books(search_query, api_key, max_results, start_index)
                items = response.get('items', [])
                total_items = response.get('totalItems', 0)
                fetched_books.extend(items)
                if len(items) < max_results:
                    break
                start_index += max_results

            # Sort books
            if sort == 'title_asc':
                fetched_books.sort(key=lambda x: x.get('volumeInfo', {}).get('title', '').lower())
            elif sort == 'title_desc':
                fetched_books.sort(key=lambda x: x.get('volumeInfo', {}).get('title', '').lower(), reverse=True)
            
            # Paginate the results
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
        'books': books,
        'query': query,
        'default_image': default_image,
        'selected_genre': genre,
        'selected_author': author,
        'selected_rating': rating,
        'selected_sort': sort,
        'total_items': total_items
    }
    
    return render(request, 'showcase.html', context)
