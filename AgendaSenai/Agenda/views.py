from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login as auth_login,logout as auth_logout
from .forms import FormLogin, FormCadastro, FormsAgendarData
from .models import Sala, Agenda, Homepage, Usuario
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.utils import timezone


def homepage(request):
    context = {}
    dados_home = Homepage.objects.all()
    context["dados_home"] = dados_home
    dados_agenda = Agenda.objects.all()
    context["dados_agenda"] = dados_agenda
    return render(request, 'homepage.html',context)


def agenda(request):
    context = {}
    dados_sala = Sala.objects.all().order_by('nome')
    context['dados_sala'] = dados_sala
    dados_agenda = Agenda.objects.all()
    context["dados_agenda"] = dados_agenda   
    return render(request, 'agendacoor.html', context)

def usuarios(request):
    context = {}
    dados_usuarios = Usuario.objects.all()
    context['dados_usuarios'] = dados_usuarios
    dados_agenda = Agenda.objects.all()
    context["dados_agenda"] = dados_agenda
    return render(request,'usuarios.html', context)

@login_required
def teste(request):
    context = {}
    if request.method == 'POST':
        form = FormsAgendarData(request.POST)
        if form.is_valid():
            data = form.cleaned_data['data']
            now = timezone.localtime(timezone.now()) 
            # Verifica se a data está dentro do intervalo de agora até dois meses no futuro
            if data <= now or data > now + timedelta(days=60):
                return HttpResponse("O agendamento deve ser entre agora e daqui a dois meses.")
            # Verifica se a hora está entre 7 e 18 horas
            if data.hour < 7 or data.hour >= 18:
                return HttpResponse("O agendamento deve ser entre as 7h e as 18h.")
            # Se tudo estiver correto, você pode prosseguir com o processamento do formulário
            return render(request, 'teste.html', {'form': form})
    else:
        form = FormsAgendarData()
        context['form'] = form
        return render(request, 'teste.html', context)

def login(request):
    context = {}
    #dados do agendamento
    dados_agenda = Agenda.objects.all()
    context["dados_agenda"] = dados_agenda
    #dados da sala
    dados_sala = Sala.objects.all()
    context["dados_sala"] = dados_sala


    if request.method == "POST":
        form = FormLogin(request.POST)
        if form.is_valid():
            var_user = form.cleaned_data['user']
            var_password = form.cleaned_data['password']

            user = authenticate(username=var_user, password=var_password)
            
            if user is not None:
                auth_login(request, user)
                user_is_coordenador = False
                user_is_coordenador = request.user.groups.filter(name='Coordenador').exists()
                return render(request, 'teste.html', {'user_is_coordenador': user_is_coordenador})
            else:
                form = FormLogin()
                context['form'] = form
                context['error'] = 'Nome de usuário ou senha incorretos.'
                form = FormsAgendarData()
                context['form'] = form
                return render(request, "teste.html", context)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = FormLogin()
        context['form'] = form
        # Vou redenrizar o que foi criado no arquivo forms
        return render(request, "login.html", context)

def cadastro(request):
    context = {}
    dados_agenda = Agenda.objects.all()
    context["dados_agenda"] = dados_agenda  
    dados_sala = Sala.objects.all()
    context["dados_sala"] = dados_sala

    if request.method == "POST":
        form = FormCadastro(request.POST)
        if form.is_valid():
            
            var_first_name = form.cleaned_data['first_name']
            var_last_name = form.cleaned_data['last_name']
            var_user = form.cleaned_data['user']
            var_email = form.cleaned_data['email']
            var_password = form.cleaned_data['password']

            var_cpf = form.cleaned_data['CPF']
            
            # Cria o usuário
            user = User.objects.create_user(username=var_user, email=var_email, password=var_password)
            user.first_name = var_first_name
            user.last_name = var_last_name
            user.save()
            # 
            usuario = Usuario(nome = user, )



            # Adiciona o usuário ao grupo
            group = Group.objects.get(name='Professor')
            user.groups.add(group)

            return redirect('home')
        else:
            context['form'] = form
    else:
        form = FormCadastro()
        
        context['form'] = form
        return render(request, "cadastro.html", context)

@login_required
def logout(request):
    auth_logout(request)
    return render(request, "teste.html")