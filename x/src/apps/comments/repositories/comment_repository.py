from typing import Any

from src.apps.comments.models.comment import Comment
from src.apps.posts.models import post


class CommentRepository:
	@staticmethod
	def list(filters: dict[str, Any] = None):
		qs = Comment.objects.all()
		if filters:
			qs = qs.filter(**filters)
		return qs

	@staticmethod
	def get(pk: int) -> Comment|None:
		try:
			return Comment.objects.get(pk=pk)
		except Comment.DoesNotExist:
			return None

	@staticmethod
	def create(*, data: dict[str, Any], author) -> Comment:
		return Comment.objects.create(author=author,**data)

	@staticmethod
	def update(instance: Comment, data: dict[str, Any]) -> Comment:
		for k, v in data.items():
			setattr(instance, k, v)
		instance.save()
		return instance

	@staticmethod
	def delete(instance: Comment) -> None:
		instance.delete()

	@staticmethod
	def get_by_post():
		return Comment.objects.filter(post=post)
