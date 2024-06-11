from django.urls import path
from . import views


urlpatterns = [
    path('', views.homepage, name="home" ),
    path('login', views.login, name="login"),
    # path('teste', views.teste, name="teste"),
    path('cadastro', views.cadastro, name="cadastro"),
    path('cadastrosala', views.cadastroSala, name="cadastrosala"),
    path('logout', views.logout, name="logout"),
    path('agenda', views.agenda, name="agenda"),
    path('usuarios', views.usuarios, name="usuarios"),
    path('perfil/<int:id>/', views.perfil, name='perfil'),
    path('deletar', views.deletar, name="deletar"),
    path('atualizar', views.atualizar, name="atualizar"),
    path('agendarsala', views.agendarsala, name='agendarsala'),
    path('deletarsala', views.deletarsala, name="deletarsala"),
    path('atualizarsala', views.atualizarsala, name="atualizarsala"),
    ## calendário
    path('calendario', views.calendario, name='calendario'),
    # path('agendamento', views.agendamento, name='agendamento')
    path('agendar', views.agendar, name='agendar')

    ## calendario

]