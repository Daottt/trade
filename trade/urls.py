
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ads.urls')),
    path('auth/', include('rest_framework.urls')),
]
