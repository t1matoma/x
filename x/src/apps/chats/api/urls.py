from rest_framework.routers import DefaultRouter

from ..api.views import MessageViewSet
from ..api.views import ChatViewSet

router = DefaultRouter()
router.register(r'chats', MessageViewSet, basename='message')
router.register(r'message', ChatViewSet, basename='chat')
urlpatterns = router.urls