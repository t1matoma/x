from ..repositories.message_repository import MessageRepository
import boto3
from django.conf import settings
from botocore.client import Config
from mimetypes import guess_type

s3_client = boto3.client(
    's3',
    aws_access_key_id=settings.R2_ACCESS_KEY_ID,
    aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
    endpoint_url=settings.R2_ENDPOINT_URL,
    region_name='auto',
    config=Config(
        signature_version='s3v4',
        s3={'addressing_style': 'path'}
    )
)

class MessageService:
    @staticmethod
    def get_message(message_id: int):
        return MessageRepository.get_message_by_id(message_id)
    
    @staticmethod
    def send_message(user, content: str, chat_id: int, file=None):
        file_url = None
        if file:
            key = f"{settings.R2_BUCKET_NAME}/{file.name}"
            content_type, _ = guess_type(file.name)
            s3_client.upload_fileobj(
                Fileobj=file, 
                Bucket=settings.R2_BUCKET_NAME, 
                Key=key,
                ExtraArgs={'ContentType': content_type}
            )
            file_url = f"{settings.R2_ENDPOINT_URL}/{key}"

        return MessageRepository.create_message(
        content=content,
        file_url=file_url,
        sender_id=user.id,
        chat_id=chat_id
    )
    
    @staticmethod
    def remove_message(message_id: int, user):
        message = MessageRepository.get_message_by_id(message_id)
        if message.sender_id != user.id:
            raise PermissionError("You do not have permission to delete this message.")
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