from typing import Any

from ..models.chat import Chat
from src.apps.users.models.user import User


class ChatRepository:
    @staticmethod
    def list(filters: dict[str, Any] = None, user=None):
        qs = Chat.objects.all()
        if user:
            qs = qs.filter(members=user)
        if filters:
            qs = qs.filter(**filters)
        return qs

    @staticmethod
    def get(user1: User, user2: User) -> Chat|None:
        chat = Chat.objects.filter(members=user1).filter(members=user2).first()
        if not chat:
            return None
        return chat

    @staticmethod
    def create(*, data: dict[str, Any], members) -> Chat:
        chat = Chat.objects.create(**data)
        chat.members.set(members)
        return chat

    @staticmethod
    def delete(user, instance: Chat) -> None:
        instance.delete()

    @staticmethod
    def get_by_id(pk):
        return Chat.objects.filter(id=pk).first()
