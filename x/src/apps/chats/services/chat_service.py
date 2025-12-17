from ..repositories.chat_repository import ChatRepository

class ChatService:
    @staticmethod
    def get_or_create_chat(user1, user2):
        chat = ChatRepository.get(user1=user1, user2=user2)
        if chat:
            return chat
        return ChatRepository.create(data={}, members=[user1, user2])

    @staticmethod
    def list_chats_for_user(user):
        return ChatRepository.list(user=user)

    @staticmethod
    def delete_chat_for_user(pk, user):
        instance = ChatRepository.get_by_id(pk)
        if not instance or user not in instance.members.all():
            return False
        ChatRepository.delete(user, instance)
        return True
