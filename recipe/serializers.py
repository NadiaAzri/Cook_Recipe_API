from rest_framework import serializers
from .models import Recipe, Comment, Like, DisLike
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from accounts.models import ProfileUser
from django.conf import settings

user = settings.AUTH_USER_MODEL


# TODO: add the user profile (all his recipes)
class LikeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Like
        fields = ('id','recipe', 'comment', 'users','created','updated',)
        depth = 1


class DisLikeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DisLike
        fields = ('id','recipe', 'comment', 'users','created','updated',)
        depth = 1


class CommentSerializer(serializers.ModelSerializer):
    # author = serializers.ReadOnlyField(source='author.user_name')
    # recipe = serializers.ReadOnlyField(source='recipe.title')
    likes = LikeSerializer(many=True, required=False)
    dislikes = DisLikeSerializer(many=True, required=False)
    class Meta:
        model = Comment
        fields = ('id','body', 'parent', 'author', 'recipe','created','updated', 'total_replies','total_likes','total_dislikes','likes', 'dislikes')
        depth = 1
        

class RecipeSerializer(serializers.ModelSerializer):
    # author = serializers.ReadOnlyField(source='author.user_name')
    # comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    comments = CommentSerializer(many=True, required=False)
    likes = LikeSerializer(many=True, required=False)
    dislikes = DisLikeSerializer(many=True, required=False)
    

    class Meta:
        model = Recipe
        fields = ('id', 'title', 'author','thumbnail', 'style', 'ingredients', 'description','created','updated','total_comments','total_likes','total_dislikes', 'comments', 'likes', 'dislikes')
        depth = 1
    
 