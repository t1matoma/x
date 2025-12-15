from typing import Any

from src.apps.posts.models.post import Post


class PostRepository:
	@staticmethod
	def list(filters: dict[str, Any] = None):
		qs = Post.objects.all()
		if filters:
			qs = qs.filter(**filters)
		return qs

	@staticmethod
	def get(pk: int) -> Post|None:
		try:
			return Post.objects.get(pk=pk)
		except Post.DoesNotExist:
			return None

	@staticmethod
	def create(*, data: dict[str, Any], author) -> Post:
		return Post.objects.create(author=author,**data)

	@staticmethod
	def update(instance: Post, data: dict[str, Any]) -> Post:
		for k, v in data.items():
			setattr(instance, k, v)
		instance.save()
		return instance

	@staticmethod
	def delete(instance: Post) -> None:
		instance.delete()
