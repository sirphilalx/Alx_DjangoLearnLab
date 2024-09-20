from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, permission_classes
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly
from notifications.models import Notification

# Post.objects.filter(author__in=following_users).order_by
# generics.get_object_or_404(Post, pk=pk)
# Like.objects.get_or_create(user=request.user, post=post)

User = get_user_model()

class PostViewSet(viewsets.ModelViewSet):
    # Post.objects.filter(author__in=following_users).order_by
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['title', 'content']
    search_fields = ['title', 'content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Get the current user
        user = self.request.user
        # Get the users the current user follows
        followed_users = user.following.all()
        # Filter posts based on followed users
        queryset = Post.objects.filter(author__in=followed_users).order_by('-created_at')
        return queryset
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_post(request, pk):
    user = request.user
    post = get_object_or_404(Post, id=pk)
    
    if Like.objects.filter(post=post, user=user).exists():
        return Response({"detail": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

    Like.objects.create(post=post, user=user)

    # Create notification
    verb = "liked your post"
    Notification.objects.create(
        recipient=post.author,
        actor=user,
        verb=verb,
        target_content_type=ContentType.objects.get_for_model(post),
        target_object_id=post.id
    )
    
    return Response({"detail": "Post liked."}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unlike_post(request, pk):
    user = request.user
    post = get_object_or_404(Post, id=pk)
    
    like = Like.objects.filter(post=post, user=user).first()
    if not like:
        return Response({"detail": "You haven't liked this post."}, status=status.HTTP_400_BAD_REQUEST)

    like.delete()

    # Create notification
    verb = "unliked your post"
    Notification.objects.create(
        recipient=post.author,
        actor=user,
        verb=verb,
        target_content_type=ContentType.objects.get_for_model(post),
        target_object_id=post.id
    )
    
    return Response({"detail": "Post unliked."}, status=status.HTTP_200_OK)