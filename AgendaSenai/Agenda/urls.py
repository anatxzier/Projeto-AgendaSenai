from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name="home" ),
    path('login', views.login, name="login"),
    path('teste', views.teste, name="teste"),
    path('cadastro', views.cadastro, name="cadastro"),
    path('cadastrosala', views.cadastro, name="cadastrosala"),
    path('logout', views.logout, name="logout"),
    path('agenda', views.agenda, name="agenda"),
    path('usuarios', views.usuarios, name="usuarios"),
    path('perfil/<int:id>/', views.perfil, name='perfil')

]