from rest_framework import serializers
from .models import *

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        read_only_field = ['id', 'created_at', 'updated_at']