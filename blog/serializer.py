from rest_framework import serializers
from .models import BlogModel,Comments

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model=BlogModel
        fields='__all__'

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comments 
        fields='__all__'