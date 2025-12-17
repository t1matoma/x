from ..repositories.chat_repository import ChatRepository

class ChatService:
    @staticmethod
    def get_or_create(user1, user2):
        chat = ChatRepository.get(user1=user1, user2=user2)
        if chat:
            return chat
        return ChatRepository.create(members=[user1, user2])
    
    @staticmethod
    def list_chats(user):
        ChatRepository.list(user=user)
    
    @staticmethod
    def delete_chat(user1, user2):
        instance = ChatRepository.get(user1=user1, user2=user2)
        if not instance:
            return False
        
        ChatRepository.delete(instance)
        return True 