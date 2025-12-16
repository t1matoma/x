from typing import Any

from ..models.like import Like


class LikeRepository:
    @staticmethod
    def get(post, user) -> Like|None:
        like = Like.objects.filter(post=post, user=user).first()
        if not like:
            return None
        return like
    
    @staticmethod
    def create(post, user) -> Like:
        return Like.objects.create(post=post, user=user)

    @staticmethod
    def delete(like):
        return like.delete()
    
    @staticmethod
    def list_likes(post):
        return Like.objects.filter(post=post)
