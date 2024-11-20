from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework import viewsets, filters, permissions
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegisterSerializer
from blog.serializers import UserListSerializer, UserDetailSerializer
from .models import BlogPost, BlogComment
from .pagination import BlogPostPagination, BlogCommentPagination
from .serializers import BlogPostSerializer, BlogCommentSerializer
from .tasks import send_confirmation_email


class UserListView(ListAPIView):
    """
    API endpoint to retrieve a list of all users.
    """
    queryset = User.objects.all()            # Retrieve all users
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserDetailView(RetrieveAPIView):
    """
    API endpoint to retrieve a single user's details.
    """
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    lookup_field = 'pk'
    permission_classes = [permissions.IsAuthenticated]


class RegisterView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Send the confirmation email asynchronously
            send_confirmation_email(user.id, user.email)
            # send_confirmation_email.delay(user.id, user.email)
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmailConfirmationView(APIView):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(id=uid)
        except (TypeError, ValueError, User.DoesNotExist):
            return Response({"error": "Invalid confirmation link."}, status=400)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"message": "Email confirmed successfully!"}, status=200)
        return Response({"error": "Invalid or expired token."}, status=400)

class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    pagination_class = BlogPostPagination
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically set the logged-in user as the author of the blog post
        serializer.save(author=self.request.user)

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
    permission_classes = [permissions.IsAuthenticated]
