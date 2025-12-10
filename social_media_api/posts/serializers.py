# posts/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment

User = get_user_model()

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        source='author', queryset=User.objects.all(), write_only=True, required=False
    )

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'author_id', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

    def create(self, validated_data):
        # If author provided via view (request.user), prefer that
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            validated_data['author'] = request.user
        return super().create(validated_data)


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        source='author', queryset=User.objects.all(), write_only=True, required=False
    )

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'author_id', 'comments', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'comments', 'created_at', 'updated_at']

    def create(self, validated_data):
        # prefer request.user as author when available
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            validated_data['author'] = request.user
        return super().create(validated_data)
