from ..repositories.message_repository import MessageRepository

class MessageService:
    @staticmethod
    def get_message(message_id: int):
        return MessageRepository.get_message_by_id(message_id)
    
    @staticmethod
    def send_message(user, content: str, chat_id: int):
        return MessageRepository.create_message(content, user.id, chat_id)
    
    @staticmethod
    def remove_message(message_id: int):
        MessageRepository.delete_message(message_id)
        
    @staticmethod
    def edit_message(user, message_id: int, new_content: str):
        message = MessageRepository.get_message_by_id(message_id)
        if message.sender_id != user.id:
            raise PermissionError("You do not have permission to edit this message.")
        return MessageRepository.update_message(message_id, new_content)
    
    @staticmethod
    def get_messages_for_chat(chat_id: int):
        return MessageRepository.list_messages_by_chat(chat_id)