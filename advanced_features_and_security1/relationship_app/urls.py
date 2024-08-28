from django.urls import path
from . import views
from .views import list_books
from django.contrib.auth.views import LoginView
from .views import LibraryDetailView, profile, Admin, Librarian, Member

urlpatterns = [
    path('books/', views.list_books, name='list_books'),
    path('register/', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    # path(LogoutView.as_view(template_name="logout") ),
    # path(LoginView.as_view(template_name='login')),
    path('profile/', profile, name='users-profile'),
    path('admin/', Admin, name='admin'),
    path('librarian/', Librarian, name='librarian'),
    path('member/', Member, name='member'),

    # new path for book management
    # path('add_book/', views.add_book, name='add_book'),
    # path('edit_book/<int:pk>/', views.edit_book, name='edit_book'),
    # path('delete_book/<int:pk>/', views.delete_book, name='delete_book'),
]
