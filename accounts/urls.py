from django.urls import path
from .views import CustomUserCreate, BlacklistTokenUpdateView, UpdateDeleteProfile


urlpatterns = [
    path('create/', CustomUserCreate.as_view(), name="create_user"),
    path('update/<int:pk>/', UpdateDeleteProfile.as_view(), name="update_user"),
    path('logout/', BlacklistTokenUpdateView.as_view(), name='blacklist')
]