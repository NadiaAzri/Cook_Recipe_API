from re import T
from django.db import models
import uuid
from django.conf import settings
from django.utils import timezone

user = settings.AUTH_USER_MODEL

class Recipe(models.Model):
    options = (
        ('algerian', 'Algerian Food'),
        ('arabic', 'Arabic Food'),
        ('asian', 'Asian Food'),
        ('american', 'American Food'),
        ('chinese', 'Chinese Food'),
        ('french', 'French Food'),
        ('japanese', 'Japanese Food'),
        ('italian', 'Italian Food'),
        ('greek', 'Greek Food'),
        ('spanish', 'Spanish Food'),
        ('mediterranean', 'Mediterranean Food'),
        ('lebanese', 'Lebanese Food'),
        ('moroccan', 'Moroccan Food'),
        ('turkish', 'Turkish Food'),
        ('thai', 'Thai Food'),
        ('indian', 'Indian Food'),
        ('cajun', 'Cajun Food'),
        ('mexican', 'Mexican Food'),
        ('caribbean', 'Caribbean Food'),
        ('german', 'German Food'),
        ('russian', 'Russian Food'),
        ('hungarian', 'Hungarian Food'),
    )

    author = models.ForeignKey(user,models.CASCADE, related_name='recipes')
    style = models.CharField( max_length=50, choices=options, default='Arabic Food')
    title = models.CharField(max_length=200)
    thumbnail = models.ImageField(default="images/1.jpg", null=True, blank=True)
    ingredients = models.TextField(max_length=4000)
    description = models.TextField(max_length=4000) 
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4,  unique=True,primary_key=True, editable=False)

    def __str__(self):
        return self.title
    
    @property
    def get_total_likes(self):
          return Like.objects.filter(recipe=self).count()
    
    @property
    def get_total_dislikes(self):
         return DisLike.objects.filter(recipe=self).count()


class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField(null=True, blank=True)
    author = models.ForeignKey(user, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True,null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    id = models.UUIDField(default=uuid.uuid4,  unique=True,primary_key=True, editable=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
 	
    def __str__(self):
        return self.body[0:50]
    
    @property
    def children(self):
        return Comment.objects.filter(parent=self).order_by('-created').all()
    
    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False
  
    @property
    def get_total_likes(self):
          return Like.objects.filter(comment=self).count()
    
    @property
    def get_total_dislikes(self):
         return DisLike.objects.filter(comment=self).count()


class Like(models.Model):
    ''' like  comment '''
    
    recipe = models.ForeignKey(Recipe, related_name="likes", on_delete=models.CASCADE, null=True,blank=True)
    comment = models.ForeignKey(Comment, related_name="likes", on_delete=models.CASCADE, null=True, blank=True)
    users = models.ForeignKey(user, on_delete=models.CASCADE,related_name='requirement_comment_likes', null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    id = models.UUIDField(default=uuid.uuid4,  unique=True,primary_key=True, editable=False)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.comment is not None:
         return str(self.comment.body)[:30]
        return str(self.recipe.title)

class DisLike(models.Model):
    ''' Dislike  comment '''

    recipe = models.ForeignKey(Recipe, related_name="dislikes", on_delete=models.CASCADE, null=True,blank=True)
    comment = models.ForeignKey(Comment, related_name="dislikes", on_delete=models.CASCADE, null=True,blank=True)
    users = models.ForeignKey(user,on_delete=models.CASCADE, related_name='requirement_comment_dislikes', null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    id = models.UUIDField(default=uuid.uuid4,  unique=True,primary_key=True, editable=False)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.comment is not None:
         return str(self.comment.body)[:30]
        return str(self.recipe.title)