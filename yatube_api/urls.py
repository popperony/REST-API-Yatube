from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import (
        TokenObtainPairView,
        TokenRefreshView,
    )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api.urls')),
    path('redoc/', TemplateView.as_view(template_name='redoc.html'), name='redoc'),
]
