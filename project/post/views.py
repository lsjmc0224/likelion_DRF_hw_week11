from rest_framework import viewsets, mixins
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Post
from .serializers import PostSerializer

# Create your views here.
class PostViewSet(viewsets.GenericViewSet, 
                  mixins.ListModelMixin, 
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin, 
                  mixins.DestroyModelMixin):
    queryset = Post.objects.all()
    serializer_class = PostSerializer