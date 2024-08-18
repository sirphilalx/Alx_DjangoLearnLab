from django.urls import path
from . import views
from .views import list_books
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from .views import LibraryDetailView

urlpatterns = [
    path('books/', views.list_books, name='list_books'),
    # path('register', views.register, name='register'),
    # path('login', views.login, name='login'),
    # path('logout', views.logout, name='logout'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]
