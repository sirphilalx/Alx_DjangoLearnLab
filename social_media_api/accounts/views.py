from rest_framework import generics, status, permissions, viewsets
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer
from .permissions import IsSelf

# generics.GenericAPIView
# CustomUser.objects.all()


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Ensure a token is only created if one does not exist for the user
        token, created = Token.objects.get_or_create(user=user)

        return Response({'token': token.key}, status=status.HTTP_201_CREATED)

class UserLoginView(ObtainAuthToken):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = authenticate(username=serializer.validated_data['username'], password=serializer.validated_data['password'])
        
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
    
User = get_user_model()

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsSelf]

    @action(detail=False, methods=['post'], url_path='follow/(?P<user_id>\d+)')
    def follow_user(self, request, user_id=None):
        user_to_follow = get_object_or_404(User, pk=user_id)
        user = request.user
        if user != user_to_follow:
            user.following.add(user_to_follow)
            user.save()
            return Response({"status": "user followed"}, status=status.HTTP_200_OK)
        return Response({"status": "cannot follow yourself"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='unfollow/(?P<user_id>\d+)')
    def unfollow_user(self, request, user_id=None):
        user_to_unfollow = get_object_or_404(User, pk=user_id)
        user = request.user
        if user != user_to_unfollow:
            user.following.remove(user_to_unfollow)
            user.save()
            return Response({"status": "user unfollowed"}, status=status.HTTP_200_OK)
        return Response({"status": "cannot unfollow yourself"}, status=status.HTTP_400_BAD_REQUEST)