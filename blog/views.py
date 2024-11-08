from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, status, permissions
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from blog.serializers import UserListSerializer, UserDetailSerializer
from .models import BlogPost, BlogComment
from .pagination import BlogPostPagination, BlogCommentPagination
from .serializers import BlogPostSerializer, BlogCommentSerializer


class UserListView(ListAPIView):
    """
    API endpoint to retrieve a list of all users.
    """
    queryset = User.objects.all()            # Retrieve all users
    serializer_class = UserListSerializer
    # permission_classes = [permissions.IsAuthenticated]

class UserDetailView(RetrieveAPIView):
    """
    API endpoint to retrieve a single user's details.
    """
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    lookup_field = 'pk'
    # permission_classes = [permissions.IsAuthenticated]

class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    pagination_class = BlogPostPagination
    # permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = self.get_object()
        if request.user in post.likes.all():
            return Response({"message": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        post.likes.add(request.user)
        return Response({"message": "Post liked!"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        post = self.get_object()
        if request.user not in post.likes.all():
            return Response({"message": "You haven't liked this post yet."}, status=status.HTTP_400_BAD_REQUEST)

        post.likes.remove(request.user)
        return Response({"message": "Post unliked!"}, status=status.HTTP_200_OK)


class BlogCommentViewSet(viewsets.ModelViewSet):
    queryset = BlogComment.objects.all()
    serializer_class = BlogCommentSerializer
    pagination_class = BlogCommentPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['post']
    ordering_fields = 'created_at'
    ordering = ['-created_at']
    # permission_classes = [permissions.IsAuthenticated]
