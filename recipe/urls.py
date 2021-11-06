from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register('recipe', views.ViewsetsRecipe)


urlpatterns = [
    # Viewsets
    path('cook/', include(router.urls)),
    path('cook/recipe/info/<str:pk>/', views.recipe_informations),
    path('cook/recipe/<str:pk>/like/', views.like_recipe),
    path('cook/recipe/<str:pk>/dislike/', views.dislike_recipe),
    path('cook/recipe/<str:recipe_pk>/comments/<str:pk>/like/', views.like_comment),
    path('cook/recipe/<str:recipe_pk>/comments/<str:pk>/dislike/', views.dislike_comment),
    path('cook/recipe/<str:recipe_pk>/comments/info/<str:comment_pk>/', views.comment_informations),
    path('cook/recipe/<str:recipe_pk>/comments/<str:pk>/', views.CommentCRUD.as_view()),
    path('cook/recipe/<str:recipe_pk>/comments/', views.ListPostComment.as_view()),
    path('cook/recipe/<str:recipe_pk>/comments/<str:parent_pk>/replies/<str:pk>/', views.ReplyCRUD.as_view()),
    path('cook/recipe/<str:recipe_pk>/comments/<str:parent_pk>/replies/', views.ListPostReply.as_view()),
    
   
]