from django.urls import path
from . import views
from .views import list_books
from django.contrib.auth.views import LoginView
from .views import LibraryDetailView, profile, admin_dashboard, librarian_dashboard, member_dashboard

urlpatterns = [
    path('books/', views.list_books, name='list_books'),
    path('register/', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    # path(LogoutView.as_view(template_name="logout") ),
    # path(LoginView.as_view(template_name='login')),
    path('profile/', profile, name='users-profile'),
    path('admin/', admin_dashboard, name='admin_dashboard'),
    path('librarian/', librarian_dashboard, name='librarian_dashboard'),
    path('member/', member_dashboard, name='member_dashboard'),
]
