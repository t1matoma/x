from ..models.message import Message

class MessageRepository:
    @staticmethod
    def get_message_by_id(message_id: int) -> Message:
        return Message.objects.get(id=message_id)
    
    @staticmethod
    def create_message(content: str, sender_id: int, chat_id: int, file_url: str|None = None) -> Message:
        message = Message(content=content, file_url=file_url, sender_id=sender_id, chat_id=chat_id)
        message.save()
        return message
    
    @staticmethod
    def delete_message(message_id: int) -> None:
        message = MessageRepository.get_message_by_id(message_id)
        message.delete()
      
    @staticmethod
    def update_message(message_id: int, new_content: str) -> Message:
        message = MessageRepository.get_message_by_id(message_id)
        message.content = new_content
        message.save()
        return message
    
    @staticmethod
    def list_messages_by_chat(chat_id: int) -> list[Message]:
        return Message.objects.filter(chat_id=chat_id).order_by('timestamp').all()