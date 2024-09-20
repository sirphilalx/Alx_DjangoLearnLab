from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserRegistrationView, UserLoginView, CustomUserViewSet

# Creating the router and registering the viewsets
router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='user')

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('', include(router.urls)),  
    path('follow/<int:user_id>/', CustomUserViewSet.as_view({'post': 'follow_user'}), name='follow-user'),
    path('unfollow/<int:user_id>/', CustomUserViewSet.as_view({'post': 'unfollow_user'}), name='unfollow-user'),
]
