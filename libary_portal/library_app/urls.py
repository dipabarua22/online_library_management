from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('book/<int:id>/', views.book_detail, name='book_detail'),
    path('book/<int:book_id>/review/', views.add_review, name='add_review'),

    path('register/', views.register, name='register'),
]
