from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SalaViewSet

router = DefaultRouter()
router.register(r'salas', SalaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]