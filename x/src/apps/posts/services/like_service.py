from ..repositories.like_repository import LikeRepository

class LikeService:
    @staticmethod
    def toggle_like(post, user):
        like = LikeRepository.get(post, user)
        if like:
            LikeRepository.delete(like)
            return False
        LikeRepository.create(post, user)
        return True
    @staticmethod
    def list_likes(post):
        return LikeRepository.list_likes(post)
    