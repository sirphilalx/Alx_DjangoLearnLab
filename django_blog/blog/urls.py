from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from .views import post_list
from .views import PostDetailView, PostCreateView, PostUpdateView, PostDeleteView
from .views import (
    PostDetailView, CommentCreateView, CommentUpdateView, CommentDeleteView
)

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('', views.home, name='home'),
    # path('post/', PostListView.as_view(), name='post_list'),
    path('post/', post_list, name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/comment/', CommentCreateView.as_view(), name='comment-create'),
    # path('post/<int:pk>/comment/new', CommentCreateView.as_view(), name='comment-create'),
    path('comment/<int:pk>/edit/', CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    # path('comment/<int:pk>/update/', CommentDeleteView.as_view(), name='comment-update'),
]
