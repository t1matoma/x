from typing import Any

from src.apps.comments.repositories.comment_repository import CommentRepository
from src.apps.comments.models.comment import Comment


class CommentService:
	@staticmethod
	def list_comments(filters: dict[str, Any]|None = None):
		return CommentRepository.list(filters=filters)

	@staticmethod
	def get_comment(pk: int) -> Comment|None:
		return CommentRepository.get(pk=pk)

	@staticmethod
	def create_comment(*, data: dict[str, Any], author) -> Comment:
		return CommentRepository.create(data=data, author=author)

	@staticmethod
	def update_comment(pk: int, data: dict[str, Any], user) -> Comment|None:
		instance = CommentRepository.get(pk=pk)
		if not instance or instance.author != user:
			return None
		return CommentRepository.update(instance, data)

	@staticmethod
	def delete_comment(pk: int, user) -> bool:
		instance = CommentRepository.get(pk=pk)
		if not instance or instance.author != user:
			return False
		CommentRepository.delete(instance)
		return True
