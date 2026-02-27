from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404 , redirect
from django.db.models import Avg
from .models import Book, Review
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from .models import Book   # adjust model name if different
from .forms import ReviewForm

def all_books(request):
    books = Book.objects.all()
    return render(request, 'library_app/books/all_books.html', {'books': books})

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()

    return render(request, "library_app/register.html", {"form": form})

def book_detail(request, id):
    book = get_object_or_404(Book, id=id)
    reviews = book.reviews.all().order_by('-created_at')
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    form = ReviewForm()

    return render(request, 'library_app/book_details.html', {
        'book': book,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'form': form
    })

def book_list(request):
    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()

    books = Book.objects.none() if query or category else Book.objects.all()

    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query)
        )

    if category:
        books = books.filter(category=category)

    return render(request, "library_app/book_list.html", {
        "books": books,
        "query": query,
        "category": category,
    })

@login_required
def add_review(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()

    return redirect("book_detail", id=book.id)