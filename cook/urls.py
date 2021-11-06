
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('accounts.urls')),
    path('', include('recipe.urls')),
    path('api-auth/', include('rest_framework.urls'))
]