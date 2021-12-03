from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register('recipe', views.ViewsetsRecipe, basename='recipes')
router2 = DefaultRouter()
router2.register('comment', views.ViewsetsComment, basename='comments')
router3 = DefaultRouter()
router3.register('reply', views.ViewsetsReply, basename='replies')

urlpatterns = [
    # Viewsets
    path('cook/recipes/<str:recipe_pk>/comments/<str:parent_pk>/', include(router3.urls)),
    path('cook/recipes/<str:recipe_pk>/', include(router2.urls)),
    path('cook/', include(router.urls)),
]