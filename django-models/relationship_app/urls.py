from django.urls import path
from .views import list_books, register, login, logout
from .views import LibraryDetailView

urlpatterns = [
    path('books/', list_books, name='list_books'),
    path('register', register, name='register'),
    path('login', login, name='login'),
    path('logout', logout, name='logout'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]
