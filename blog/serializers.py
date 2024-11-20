# serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers

from .models import BlogPost, BlogComment


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class UserListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'url', 'username']

class UserDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class BlogCommentSerializer(serializers.ModelSerializer):
    post_id = serializers.PrimaryKeyRelatedField(queryset=BlogPost.objects.all(), source='post')

    class Meta:
        model = BlogComment
        fields = ['id', 'post_id', 'author', 'content', 'created_at']

class BlogPostSerializer(serializers.ModelSerializer):
    comments = BlogCommentSerializer(many=True, read_only=True)  # Nested comments for BlogPost
    like_count = serializers.SerializerMethodField()
    author = UserSerializer(read_only=True)

    class Meta:
        model = BlogPost
        fields = ['id', 'author', 'title', 'content', 'created_at', 'updated_at', 'comments', 'like_count']

    def get_like_count(self, obj):
        return obj.likes.count()