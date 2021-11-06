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
        fields = ('id', 'title', 'author', 'style', 'ingredients', 'description','created','updated', 'comments', 'likes', 'dislikes')
    
    def get_author(self, obj):
        return obj.author.user_name
    
    def get_comment_count(obj):
            return obj.comments.all().count()
        
    def get_likes(obj):
        return Like.objects.filter(recipe=obj).count()
    
    def get_dislikes(obj):
        return DisLike.objects.filter(recipe=obj).count()

 


# class CommentChildSerializer(serializers.ModelSerializer):
#     parent_id = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(),source='parent.id')
#     author = serializers.SerializerMethodField()
#     class Meta:
#         model = Comment
#         fields = ('author', 'content', 'id','parent_id')

#     def get_author(self, obj):
#         return obj.author.username

#     def create(self, validated_data):
#         subject = parent.objects.create(parent=validated_data['parent']['id'], content=validated_data['content'])

class CommentSerializer(serializers.ModelSerializer):
    # reply_count = serializers.SerializerMethodField()
    # author = serializers.SerializerMethodField()
    # replies = serializers.SerializerMethodField()
    author = serializers.ReadOnlyField(source='author.user_name')
    recipe = serializers.ReadOnlyField(source='recipe.title')
    likes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    dislikes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Comment
        fields = ('id','body', 'parent', 'author', 'recipe','created','updated', 'likes', 'dislikes')
        # depth = 1

    def get_reply_count(obj):
        if obj.is_parent:
            return Comment.objects.filter(parent=obj).order_by('-created').all().count()
        return 0

    def get_author(self, obj):
        return obj.author.user_name
    
    def get_likes(obj):
        return Like.objects.filter(comment=obj).count()
    
    def get_dislikes(obj):
        return DisLike.objects.filter(comment=obj).count()
    # def get_replies(self, obj):
    #     if obj.is_parent:
    #         return CommentChildSerializer(obj.children(), many=True).data
    #     return None