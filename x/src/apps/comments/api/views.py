from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from src.apps.comments.schemas.comment import CommentSerializer, CommentCreateSerializer
from src.apps.comments.services.comment_service import CommentService

@method_decorator(csrf_exempt, name='dispatch')
class CommentViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CommentService.list_comments()

    def create(self, request, *args, **kwargs):
        serializer = CommentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = CommentService.create_comment(data=serializer.validated_data, author=request.user)
        out = self.get_serializer(comment)
        return Response(out.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        serializer = CommentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = CommentService.update_comment(
            pk=kwargs.get('pk'),
            data=serializer.validated_data,
            user=request.user
        )
        if not comment:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(CommentSerializer(comment).data)

    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        deleted = CommentService.delete_comment(pk, user=request.user)
        if not deleted:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    
