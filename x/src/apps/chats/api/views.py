from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from ..schemas.chat import ChatSerializer, ChatCreateSerializer
from ..services.chat_service import ChatService
from ..schemas.message import MessageSerializer, MessageCreateSerializer, MessageEditSerializer
from ..services.message_service import MessageService

@method_decorator(csrf_exempt, name='dispatch')
class ChatViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ChatService.list_chats_for_user(self.request.user)
    
    def create(self, request, *args, **kwargs):
        serializer = ChatCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        chat = ChatService.get_or_create_chat(
            user1=request.user,
            user2=serializer.validated_data['members'][0]  # Assuming two-member chats
        )
        out = self.get_serializer(chat)
        return Response(out.data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, *args, **kwargs):       
        pk = kwargs.get('pk')
        deleted = ChatService.delete_chat_for_user(pk, user=request.user)
        if not deleted:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@method_decorator(csrf_exempt, name='dispatch')
class MessageViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        chat_id = self.request.query_params.get('chat_id')
        return MessageService.get_messages_for_chat(chat_id)
    
    def create(self, request, *args, **kwargs):
        serializer = MessageCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = MessageService.send_message(
            user=request.user,
            content=serializer.validated_data['content'],
            chat_id=serializer.validated_data['chat'].id
        )
        out = self.get_serializer(message)
        return Response(out.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        serializer = MessageEditSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = MessageService.edit_message(
            user=request.user,
            message_id=kwargs.get('pk'),
            new_content=serializer.validated_data['content']
        )
        if not message:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(MessageSerializer(message).data)
    
    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        deleted = MessageService.remove_message(pk, self.request.user)
        if not deleted:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)