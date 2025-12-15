from typing import Any

from src.apps.posts.repositories.post_repository import PostRepository
from src.apps.posts.models.post import Post


class PostService:
	@staticmethod
	def list_posts(filters: dict[str, Any]|None = None):
		return PostRepository.list(filters=filters)

	@staticmethod
	def get_post(pk: int) -> Post|None:
		return PostRepository.get(pk=pk)

	@staticmethod
	def create_post(*, data: dict[str, Any], author) -> Post:
		return PostRepository.create(data=data, author=author)

	@staticmethod
	def update_post(pk: int, data: dict[str, Any], user) -> Post|None:
		instance = PostRepository.get(pk=pk)
		if not instance or instance.author != user:
			return None
		return PostRepository.update(instance, data)

	@staticmethod
	def delete_post(pk: int, user) -> bool:
		instance = PostRepository.get(pk=pk)
		if not instance or instance.author != user:
			return False
		PostRepository.delete(instance)
		return True
