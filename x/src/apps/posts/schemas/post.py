from rest_framework import serializers

from src.apps.posts.models.post import Post


class PostSerializer(serializers.ModelSerializer):
	liked_count = serializers.IntegerField(source='likes.count', read_only=True)
	liked_by = serializers.SerializerMethodField()
	comment_count = serializers.IntegerField(source='comments.count', read_only=True)
	commented_by = serializers.SerializerMethodField()
	author_username = serializers.CharField(source='author.username', read_only=True)
	is_liked = serializers.SerializerMethodField()
	class Meta:
		model = Post
		fields = ['id', 'author', 'author_username', 'title', 'content', 'created_at', 'updated_at', 'liked_count', 'liked_by','comment_count','commented_by', 'is_liked']
		read_only_fields = ['id', 'created_at', 'updated_at']
  
	def get_liked_by(self, obj):
		return [like.user.username for like in obj.likes.all()]
	def get_commented_by(self, obj):
		return [comment.author.username for comment in obj.comments.all()]
	def get_is_liked(self, obj):
		request = self.context.get('request')
		if request and request.user.is_authenticated:
			return obj.likes.filter(user=request.user).exists()
		return False


class PostCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = ('title', 'content')