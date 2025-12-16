from rest_framework import serializers

from src.apps.comments.models.comment import Comment


class CommentSerializer(serializers.ModelSerializer):
	author_username = serializers.CharField(source='author.username', read_only=True)

	class Meta:
		model = Comment
		fields = ['id', 'author', 'author_username', 'post', 'content', 'created_at', 'updated_at']
		read_only_fields = ['id', 'author', 'created_at', 'updated_at']


class CommentCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		fields = ['post', 'content']
