from rest_framework.routers import DefaultRouter
from django.urls import path, include

from ..api.views import MessageViewSet
from ..api.views import ChatViewSet

router = DefaultRouter()
router.register(r'chats', ChatViewSet, basename='chat')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
    path('chats/<int:chat_pk>/messages/', MessageViewSet.as_view({'get': 'list', 'post': 'create'}), name='chat-messages'),
]
