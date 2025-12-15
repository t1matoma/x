from rest_framework import serializers

from src.apps.posts.models.post import Post


class PostSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = ['id', 'author', 'title', 'content', 'created_at', 'updated_at']
		read_only_fields = ['id', 'created_at', 'updated_at']


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'content')