from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from ..schemas.chat import ChatSerializer
from ..services.chat_service import ChatService
from ..schemas.message import MessageSerializer, MessageCreateSerializer, MessageEditSerializer
from ..services.message_service import MessageService
from ..models.message import Message
from rest_framework.parsers import MultiPartParser, FormParser

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
        member_username = request.data.get('member_username')
        if not member_username:
            return Response({'error': 'member_username required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            user2 = User.objects.get(username=member_username)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        chat = ChatService.get_or_create_chat(
            user1=request.user,
            user2=user2
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
    parser_classes = (MultiPartParser, FormParser)
    
    def get_queryset(self):
        chat_id = self.kwargs.get('chat_pk') or self.request.query_params.get('chat_id')
        if not chat_id:
            return Message.objects.none()
        return MessageService.get_messages_for_chat(chat_id)
    def create(self, request, *args, **kwargs):
        print(request.data)
        print(type(request.data.get('content')))
        chat_id = self.kwargs.get('chat_pk')
        if not chat_id:
            return Response({'error': 'chat_id required'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = MessageCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        file = serializer.validated_data.get('file')

        # Отправляем сообщение через сервис
        message = MessageService.send_message(
            user=request.user,
            content=serializer.validated_data['content'],
            chat_id=chat_id,
            file=file 
        )
        
        return Response(
        MessageSerializer(message).data,
        status=status.HTTP_201_CREATED
    )
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
        try:
            deleted = MessageService.remove_message(pk, self.request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except PermissionError:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
