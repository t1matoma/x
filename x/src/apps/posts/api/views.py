from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


from src.apps.posts.schemas.post import PostSerializer, PostCreateSerializer
from src.apps.posts.services.post_service import PostService

@method_decorator(csrf_exempt, name='dispatch')
class PostViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PostService.list_posts()

    def create(self, request, *args, **kwargs):
        serializer = PostCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = PostService.create_post(data=serializer.validated_data, author=request.user)
        out = self.get_serializer(post)
        return Response(out.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        serializer = PostCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = PostService.update_post(
            pk=kwargs.get('pk'),
            data=serializer.validated_data,
            user=request.user
        )
        if not post:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(PostSerializer(post).data)

    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        deleted = PostService.delete_post(pk, user=request.user)
        if not deleted:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
