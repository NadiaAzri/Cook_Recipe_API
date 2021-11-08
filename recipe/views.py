
from .models import Recipe, Comment, Like, DisLike
from .serializers import  RecipeSerializer, CommentSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsAuthorOrReadOnly
from django.conf import settings
from rest_framework.decorators import action


# viewsets
class ViewsetsRecipe(viewsets.ModelViewSet):
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly]
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['get'])
    def like(self,request,pk=None):
  
        like = Like.objects.filter(users=request.user, recipe=Recipe.objects.get(pk=pk)).exists()
        dislike = DisLike.objects.filter(users=request.user, recipe=Recipe.objects.get(pk=pk)).exists()

        if not like  and not dislike:
           Like.objects.create(users=request.user, recipe=Recipe.objects.get(pk=pk))
           res = {
               "message": "you liked this recipe"
           }
           return Response(res, status = status.HTTP_201_CREATED)

        elif like and not dislike:
             like = Like.objects.get(users=request.user, recipe=pk)
             like.delete()
             res = {
               "message": "you unliked this recipe"
           }
             return Response(res, status= status.HTTP_204_NO_CONTENT)

        else:
             Like.objects.create(users=request.user, recipe=Recipe.objects.get(pk=pk))
             dislike = DisLike.objects.get(users=request.user, recipe=Recipe.objects.get(pk=pk))
             dislike.delete()
             res = {
               "message": "you liked this recipe"
           }
             return Response(res, status = status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get'])
    def dislike(self,request,pk=None):

        like = Like.objects.filter(users=request.user, recipe=Recipe.objects.get(pk=pk)).exists()
        dislike = DisLike.objects.filter(users=request.user, recipe=Recipe.objects.get(pk=pk)).exists()

        if not like  and not dislike:
           DisLike.objects.create(users=request.user, recipe=Recipe.objects.get(pk=pk))
           res = {
               "message": "you disliked this recipe"
           }
           return Response(res, status = status.HTTP_201_CREATED)

        elif not like and dislike:
            dislike = DisLike.objects.get(users=request.user, recipe=pk)
            dislike.delete()
            res = {
               "message": "you undisliked this recipe"
           }
            return Response(res, status= status.HTTP_204_NO_CONTENT)
          
        else:
           DisLike.objects.create(users=request.user, recipe=Recipe.objects.get(pk=pk))
           dislike = Like.objects.get(users=request.user, recipe=Recipe.objects.get(pk=pk))
           dislike.delete()
           res = {
               "message": "you disliked this recipe"
           }
           return Response( res, status = status.HTTP_201_CREATED)



class ViewsetsComment(viewsets.ModelViewSet):
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializer
    def get_queryset(self):
        
            return Comment.objects.filter(recipe=self.kwargs["recipe_pk"])
 
    def perform_create(self, serializer):
        serializer.save(recipe = Recipe.objects.get(pk=self.kwargs["recipe_pk"]), author=self.request.user)
    
    @action(detail=True, methods=['get'])
    def like(self,request,recipe_pk,pk=None):

        like = Like.objects.filter(users=request.user, comment=Comment.objects.get(pk=pk)).exists()
        dislike = DisLike.objects.filter(users=request.user, comment=Comment.objects.get(pk=pk)).exists()

        if not like  and not dislike:
           Like.objects.create(users=request.user, comment=Comment.objects.get(pk=pk))
           res = {
               "message": "you liked this comment"
           }
           return Response(res, status = status.HTTP_201_CREATED)

        elif like and not dislike:
             like = Like.objects.get(users=request.user, comment=pk)
             like.delete()
             res = {
               "message": "you unliked this comment"
           }
             return Response(res, status= status.HTTP_204_NO_CONTENT)

        else:
             Like.objects.create(users=request.user, comment=Comment.objects.get(pk=pk))
             dislike = DisLike.objects.get(users=request.user, comment=Comment.objects.get(pk=pk))
             dislike.delete()
             res = {
               "message": "you liked this comment"
           }
             return Response(res, status = status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get'])
    def dislike(self,request,recipe_pk, pk=None):

        like = Like.objects.filter(users=request.user, comment=Comment.objects.get(pk=pk)).exists()
        dislike = DisLike.objects.filter(users=request.user, comment=Comment.objects.get(pk=pk)).exists()

        if not like  and not dislike:
           DisLike.objects.create(users=request.user, comment=Comment.objects.get(pk=pk))
           res = {
               "message": "you disliked this comment"
           }
           return Response(res, status = status.HTTP_201_CREATED)

        elif not like and dislike:
             like = DisLike.objects.get(users=request.user, comment=pk)
             like.delete()
             res = {
               "message": "you undisliked this comment"
           }
             return Response(res, status= status.HTTP_204_NO_CONTENT)

        else:
            DisLike.objects.create(users=request.user, comment=Comment.objects.get(pk=pk))
            dislike = Like.objects.get(users=request.user, comment=Comment.objects.get(pk=pk))
            dislike.delete()
            res = {
               "message": "you disliked this comment"
           }
            return Response(res, status = status.HTTP_201_CREATED)

    


class ViewsetsReply(viewsets.ModelViewSet):
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializer
    def get_queryset(self):
        
            return Comment.objects.filter(parent=self.kwargs["parent_pk"])
 
    def perform_create(self, serializer):
        serializer.save(recipe = Recipe.objects.get(pk=self.kwargs["recipe_pk"]),parent=Comment.objects.get(pk=self.kwargs["parent_pk"]), author=self.request.user)
           
    @action(detail=True, methods=['get'])
    def like(self,request,recipe_pk, parent_pk,pk=None):

        like = Like.objects.filter(users=request.user, comment=Comment.objects.get(pk=pk)).exists()
        dislike = DisLike.objects.filter(users=request.user, comment=Comment.objects.get(pk=pk)).exists()

        if not like  and not dislike:
           Like.objects.create(users=request.user, comment=Comment.objects.get(pk=pk))
           res = {
               "message": "you liked this comment"
           }
           return Response(res, status = status.HTTP_201_CREATED)

        elif like and not dislike:
             like = Like.objects.get(users=request.user, comment=pk)
             like.delete()
             res = {
               "message": "you unliked this comment"
           }
             return Response(res, status= status.HTTP_204_NO_CONTENT)

        else:
             Like.objects.create(users=request.user, comment=Comment.objects.get(pk=pk))
             dislike = DisLike.objects.get(users=request.user, comment=Comment.objects.get(pk=pk))
             dislike.delete()
             res = {
               "message": "you liked this comment"
           }
             return Response(res, status = status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get'])
    def dislike(self,request,recipe_pk, parent_pk, pk=None):

        like = Like.objects.filter(users=request.user, comment=Comment.objects.get(pk=pk)).exists()
        dislike = DisLike.objects.filter(users=request.user, comment=Comment.objects.get(pk=pk)).exists()

        if not like  and not dislike:
           DisLike.objects.create(users=request.user, comment=Comment.objects.get(pk=pk))
           res = {
               "message": "you disliked this comment"
           }
           return Response(res, status = status.HTTP_201_CREATED)

        elif not like and dislike:
             like = DisLike.objects.get(users=request.user, comment=pk)
             like.delete()
             res = {
               "message": "you undisliked this comment"
           }
             return Response(res, status= status.HTTP_204_NO_CONTENT)

        else:
            DisLike.objects.create(users=request.user, comment=Comment.objects.get(pk=pk))
            dislike = Like.objects.get(users=request.user, comment=Comment.objects.get(pk=pk))
            dislike.delete()
            res = {
               "message": "you disliked this comment"
           }
            return Response(res, status = status.HTTP_201_CREATED)

