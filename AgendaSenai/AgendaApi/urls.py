from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SalaViewSet, AgendamentoViewSet, UsuarioViewSet

router = DefaultRouter()
router.register(r'salas', SalaViewSet)
router.register(r'agendamento', AgendamentoViewSet)
router.register(r'usuario', UsuarioViewSet)

urlpatterns = [
    path('', include(router.urls)),
]