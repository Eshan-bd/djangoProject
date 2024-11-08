from django.contrib.auth.models import User
from rest_framework import serializers

from .models import BlogPost, BlogComment


class UserListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'url', 'username']

class UserDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class BlogCommentSerializer(serializers.ModelSerializer):
    post_id = serializers.PrimaryKeyRelatedField(queryset=BlogPost.objects.all(), source='post')

    class Meta:
        model = BlogComment
        fields = ['id', 'post_id', 'author', 'content', 'created_at']

class BlogPostSerializer(serializers.ModelSerializer):
    comments = BlogCommentSerializer(many=True, read_only=True)  # Nested comments for BlogPost
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'comments', 'like_count']

    def get_like_count(self, obj):
        return obj.likes.count()