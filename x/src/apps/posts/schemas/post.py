from rest_framework import serializers

from src.apps.posts.models.post import Post


class PostSerializer(serializers.ModelSerializer):
	liked_count = serializers.IntegerField(source='likes.count', read_only=True)
	liked_by = serializers.SerializerMethodField()
	comment_count = serializers.IntegerField(source='comments.count', read_only=True)
	commented_by = serializers.SerializerMethodField()
	class Meta:
		model = Post
		fields = ['id', 'author', 'title', 'content', 'created_at', 'updated_at', 'liked_count', 'liked_by','comment_count','commented_by']
		read_only_fields = ['id', 'created_at', 'updated_at']
  
	def get_liked_by(self, obj):
		return [like.user.username for like in obj.likes.all()]
	def get_commented_by(self, obj):
		return [comment.author.username for comment in obj.comments.all()]


class PostCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = ('title', 'content')