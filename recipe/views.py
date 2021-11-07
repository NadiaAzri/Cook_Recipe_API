from django.shortcuts import render
from django.http.response import JsonResponse
from .models import Recipe, Comment, Like, DisLike
from rest_framework.decorators import api_view
from .serializers import  RecipeSerializer, CommentSerializer
from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import generics, mixins, viewsets
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from .permissions import IsAuthorOrReadOnly
from django.conf import settings
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from accounts.models import ProfileUser
# viewsets
class ViewsetsRecipe(viewsets.ModelViewSet):
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticated]
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# List POST comment
class ListPostComment(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    #Get comments
    def get(self, request, recipe_pk):
      try:
        comment = Comment.objects.filter(recipe=recipe_pk).all()
        serializer = CommentSerializer(comment, many=True)
        return Response(serializer.data)
      except Comment.DoesNotExists:
        return Response(status=status.HTTP_404_NOT_FOUND)
        
    # Post
    def post(self, request, recipe_pk):
        serializer = CommentSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save(recipe = Recipe.objects.get(pk=recipe_pk), author=self.request.user)
            return Response(
                serializer.data,
                status = status.HTTP_201_CREATED
            )
        return Response(
            serializer.data,
            status= status.HTTP_400_BAD_REQUEST
        )

# GET PUT DELETE comment
class CommentCRUD(APIView):
    permission_classes = [IsAuthorOrReadOnly]
    def get(self, request, pk, recipe_pk):
      try:
        comment = Comment.objects.filter(recipe=recipe_pk).get(pk=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
      except Comment.DoesNotExists:
        return Response(status=status.HTTP_404_NOT_FOUND)
        
    # PUT
    def put(self, request, pk, recipe_pk):
        try:
          comment = Comment.objects.get(pk=pk)
        except Comment.DoesNotExists:
          return Response(status=status.HTTP_404_NOT_FOUND)
       
        serializer = CommentSerializer(comment, data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    # DELETE
    def delete(self, request, pk, recipe_pk):
        try:
         comment = Comment.objects.filter(recipe=recipe_pk).get(pk=pk)
        except Comment.DoesNotExists:
         return Response(status=status.HTTP_404_NOT_FOUND)
       
        comment.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)


# List POST reply
class ListPostReply(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    #Get comments
    def get(self, request,parent_pk, recipe_pk):
      try:
        comment = Comment.objects.filter(parent=parent_pk).all()
        serializer = CommentSerializer(comment, many=True)
        return Response(serializer.data)
      except Comment.DoesNotExists:
        return Response(status=status.HTTP_404_NOT_FOUND)
        
    # Post
    def post(self, request,parent_pk, recipe_pk):
        serializer = CommentSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save(recipe = Recipe.objects.get(pk=recipe_pk),parent=Comment.objects.get(pk=parent_pk), author=self.request.user)
            return Response(
                serializer.data,
                status = status.HTTP_201_CREATED
            )
        return Response(
            serializer.data,
            status= status.HTTP_400_BAD_REQUEST
        )

# GET PUT DELETE reply
class ReplyCRUD(APIView):
    permission_classes = [IsAuthorOrReadOnly]
    def get(self, request,pk, parent_pk, recipe_pk):
      try:
        comment = Comment.objects.filter(recipe=recipe_pk).get(pk=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
      except Comment.DoesNotExists:
        return Response(status=status.HTTP_404_NOT_FOUND)
        
    # PUT
    def put(self, request, pk, parent_pk,recipe_pk):
        try:
          comment = Comment.objects.filter(recipe=recipe_pk).get(pk=pk)
        except Comment.DoesNotExists:
          return Response(status=status.HTTP_404_NOT_FOUND)
       
        serializer = CommentSerializer(comment, data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    # DELETE
    def delete(self, request, pk, recipe_pk):
        try:
         comment = Comment.objects.filter(recipe=recipe_pk).get(pk=pk)
        except Comment.DoesNotExists:
         return Response(status=status.HTTP_404_NOT_FOUND)
       
        comment.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)


@api_view(('GET',))
def recipe_informations(request,pk):

    try:
        recipe = Recipe.objects.get(pk=pk)
    except Recipe.DoesNotExists:
        return Response(status=status.HTTP_404_NOT_FOUND)

    comments = RecipeSerializer.get_comment_count(recipe)
    likes = RecipeSerializer.get_likes(recipe)
    dislikes = RecipeSerializer.get_dislikes(recipe)
    votes = [
        {
            "likes": likes,
            "dislikes": dislikes,
            "comments": comments,
        }
    ]
    return Response(votes)

@api_view(('GET',))
def comment_informations(request,comment_pk,recipe_pk):

    try:
        comment = Comment.objects.get(pk=comment_pk)
    except Comment.DoesNotExists:
        return Response(status=status.HTTP_404_NOT_FOUND)

    comments = CommentSerializer.get_reply_count(comment)
    likes = CommentSerializer.get_likes(comment)
    dislikes = CommentSerializer.get_dislikes(comment)
    votes = [
        {
            "likes": likes,
            "dislikes": dislikes,
            "replies": comments,
        }
    ]
    return Response(votes)

@api_view(('GET',))
def like_recipe(request,pk):

    like = Like.objects.filter(users=request.user, recipe=Recipe.objects.get(pk=pk)).exists()
    dislike = DisLike.objects.filter(users=request.user, recipe=Recipe.objects.get(pk=pk)).exists()

    if not like  and not dislike:
        Like.objects.create(users=request.user, recipe=Recipe.objects.get(pk=pk))
        return Response(status = status.HTTP_201_CREATED)

    elif like and not dislike:
        like = Like.objects.get(users=request.user, recipe=pk)
        like.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)

    else:
         Like.objects.create(users=request.user, recipe=Recipe.objects.get(pk=pk))
         dislike = DisLike.objects.get(users=request.user, recipe=Recipe.objects.get(pk=pk))
         dislike.delete()
         return Response(status = status.HTTP_201_CREATED)

@api_view(('GET',))
def dislike_recipe(request,pk):

    like = Like.objects.filter(users=request.user, recipe=Recipe.objects.get(pk=pk)).exists()
    dislike = DisLike.objects.filter(users=request.user, recipe=Recipe.objects.get(pk=pk)).exists()

    if not like  and not dislike:
        DisLike.objects.create(users=request.user, recipe=Recipe.objects.get(pk=pk))
        return Response(status = status.HTTP_201_CREATED)

    elif not like and dislike:
        like = DisLike.objects.get(users=request.user, recipe=pk)
        like.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)

    else:
         DisLike.objects.create(users=request.user, recipe=Recipe.objects.get(pk=pk))
         dislike = Like.objects.get(users=request.user, recipe=Recipe.objects.get(pk=pk))
         dislike.delete()
         return Response(status = status.HTTP_201_CREATED)


@api_view(('GET',))
def like_comment(request,recipe_pk, pk):

    like = Like.objects.filter(users=request.user, comment=Comment.objects.get(pk=pk)).exists()
    dislike = DisLike.objects.filter(users=request.user, comment=Comment.objects.get(pk=pk)).exists()

    if not like  and not dislike:
        Like.objects.create(users=request.user, comment=Comment.objects.get(pk=pk))
        return Response(status = status.HTTP_201_CREATED)

    elif like and not dislike:
        like = Like.objects.get(users=request.user, comment=pk)
        like.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)

    else:
         Like.objects.create(users=request.user, comment=Comment.objects.get(pk=pk))
         dislike = DisLike.objects.get(users=request.user, comment=Comment.objects.get(pk=pk))
         dislike.delete()
         return Response(status = status.HTTP_201_CREATED)

@api_view(('GET',))
def dislike_comment(request,recipe_pk, pk):

    like = Like.objects.filter(users=request.user, comment=Comment.objects.get(pk=pk)).exists()
    dislike = DisLike.objects.filter(users=request.user, comment=Comment.objects.get(pk=pk)).exists()

    if not like  and not dislike:
        DisLike.objects.create(users=request.user, comment=Comment.objects.get(pk=pk))
        return Response(status = status.HTTP_201_CREATED)

    elif not like and dislike:
        like = DisLike.objects.get(users=request.user, comment=pk)
        like.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)

    else:
         DisLike.objects.create(users=request.user, comment=Comment.objects.get(pk=pk))
         dislike = Like.objects.get(users=request.user, comment=Comment.objects.get(pk=pk))
         dislike.delete()
         return Response(status = status.HTTP_201_CREATED)

