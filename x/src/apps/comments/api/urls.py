from rest_framework.routers import DefaultRouter

from src.apps.comments.api.views import CommentViewSet

router = DefaultRouter()
router.register(r'', CommentViewSet, basename='comment')
urlpatterns = router.urls
