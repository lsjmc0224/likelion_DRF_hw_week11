from rest_framework import serializers
from .models import *



class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField(read_only=True)
    def get_comments(self, instance):
        serializer = CommentSerializer(instance.comments, many=True)
        return serializer.data
    class Meta:
        model = Post
        fields = '__all__'