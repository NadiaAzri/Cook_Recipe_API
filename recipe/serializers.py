from rest_framework import serializers
from .models import Recipe, Comment, Like, DisLike
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from accounts.models import ProfileUser
from django.conf import settings

user = settings.AUTH_USER_MODEL


class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.user_name')
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    likes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    dislikes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    

    class Meta:
        model = Recipe
        fields = ('id', 'title', 'author','thumbnail', 'style', 'ingredients', 'description','created','updated','total_comments','total_likes','total_dislikes', 'comments', 'likes', 'dislikes')
    
 
class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.user_name')
    recipe = serializers.ReadOnlyField(source='recipe.title')
    likes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    dislikes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Comment
        fields = ('id','body', 'parent', 'author', 'recipe','created','updated', 'total_replies','total_likes','total_dislikes','likes', 'dislikes')