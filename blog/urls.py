from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from blog import urls
from blog.views import UserDetailView, UserListView
from .views import BlogPostViewSet, BlogCommentViewSet

router = DefaultRouter()
router.register(r'posts', BlogPostViewSet)  # Register BlogPost viewset
router.register(r'comments', BlogCommentViewSet)  # Register BlogComment viewset

urlpatterns = [
    path('', include(router.urls)),  # Include the router URLs
    path('users/', UserListView.as_view(), name='user-list'),         # List of all users
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]