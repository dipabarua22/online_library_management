from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Review
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q, Avg

# ---------------- BOOK VIEWS (UNCHANGED) ----------------

def book_list(request):
    query = request.GET.get('q')
    category = request.GET.get('category')

    books = Book.objects.all()

    if query:
        books = books.filter(Q(title__icontains=query) | Q(author__icontains=query))

    if category:
        books = books.filter(category=category)

    return render(request, 'library_app/book_list.html', {'books': books})


def book_detail(request, id):
    book = get_object_or_404(Book, id=id)
    avg_rating = book.reviews.aggregate(Avg('rating'))['rating__avg']
    return render(request, 'library_app/book_detail.html', {
        'book': book,
        'avg_rating': avg_rating
    })


@login_required
def add_review(request, book_id):
    if request.method == 'POST':
        Review.objects.create(
            book_id=book_id,
            user=request.user,
            comment=request.POST['comment'],
            rating=request.POST['rating']
        )
    return redirect('book_detail', id=book_id)

# ---------------- AUTH VIEW (SEPARATE) ----------------

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'library_app/register.html', {'form': form})
