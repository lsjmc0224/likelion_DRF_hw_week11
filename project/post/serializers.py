from rest_framework import serializers
from .models import *



class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'

#list view (list 메소드로 불렀을 때)
class PostListSerializer(serializers.ModelSerializer):
    #content 말고 content개수만 보이기
    comments_cnt = serializers.SerializerMethodField()
    
    def get_comments_cnt(self, instance):
        return instance.comments.count()
    
    #comments 개수만 보이게 하고싶음.
    class Meta:
        model = Post
        fields = [
            'id',
            'created_at',
            'updated_at',
            'title',
            'writer',
            'content',
            'comments_cnt',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'comments_cnt','likes',]

#detail view (list 이외의 메소드로 불렀을 때)
class PostSerializer(serializers.ModelSerializer):
    # read_only = True가 아닌 필드와 serializer메소드필드 유지
    comments = serializers.SerializerMethodField()
    title = serializers.CharField()
    writer = serializers.CharField()
    content = serializers.CharField()

    def get_comments(self, instance):
        serializer = CommentSerializer(instance.comments, many=True)
        return serializer.data
    
    #여기선 comments를 보이게 하고 싶음.
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
            'comments',
        ]