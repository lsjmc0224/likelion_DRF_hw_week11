from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Count, Q

from .models import *
from .serializers import *
# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.annotate(
        like_cnt=Count(
            "reactions", filter=Q(reactions__reaction="like"), distinct=True
        ),
    )
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["title"]
    search_fields = ["title", "^title"]
    ordering_fields = ["title", "created_at"]
    def get_serializer_class(self):
        if self.action == 'list': 
            return PostListSerializer
        return PostSerializer
    
    def get_permissions(self):
        if self.action in ['likes', 'create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return []
    
    @action(methods=["POST"], detail=True, permission_classes=[IsAuthenticated])
    def likes(self, request, pk=None):
        post = self.get_object()
        PostReaction.objects.create(post=post, user=request.user, reaction="like")
        return Response()
    
    @action(methods=["GET"], detail=False)
    def top5(self, request):
        queryset = self.get_queryset().order_by("-like_cnt")[:5]
        serializer = PostListSerializer(queryset, many=True)
        return Response(serializer.data)

class CommentViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin, 
    mixins.DestroyModelMixin
    ):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return []

class PostCommentViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin
    ):
    serializer_class = CommentSerializer

    #url에서 추출된 post아이디를 가져오는 것
    def get_queryset(self):
        post = self.kwargs.get("post_id")
        queryset = Comment.objects.filter(post_id=post)
        return queryset
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return []
    
    def create(self, request, post_id=None):
        post = get_object_or_404(Post, id=post_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(post=post)
        return Response(serializer.data)