from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


from src.apps.posts.schemas.post import PostSerializer, PostCreateSerializer
from src.apps.posts.services.post_service import PostService
from ..services.like_service import LikeService
from src.apps.comments.services.comment_service import CommentService
from src.apps.comments.schemas.comment import CommentSerializer

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
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        post = PostService.get_post(pk=int(pk))
        if not post:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        liked = LikeService.toggle_like(post=post, user=request.user)

        return Response({
            'liked': liked,
            'count': post.likes.count()
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def comment(self, request, pk=None):
        post = PostService.get_post(pk=int(pk))
        if not post:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = {'post': post, 'content': request.data.get('content')}
        comment = CommentService.create_comment(data=data, author=request.user)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def comments(self, request, pk=None):
        post = PostService.get_post(pk=int(pk))
        if not post:
            return Response(status=status.HTTP_404_NOT_FOUND)
        comments = CommentService.list_comments_by_post(post_id=post.id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


    def get_queryset(self):
        return PostService.list_posts()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

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
        out = self.get_serializer(post)
        return Response(out.data)

    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        deleted = PostService.delete_post(pk, user=request.user)
        if not deleted:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
