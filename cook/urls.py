
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('accounts.urls')),
    path('', include('recipe.urls')),
    path('cook/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('cook/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]