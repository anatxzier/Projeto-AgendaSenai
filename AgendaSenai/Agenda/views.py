from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login as auth_login,logout as auth_logout
from .forms import FormLogin, FormCadastro
from .models import Agendamento, Sala, Agenda, Homepage
from django.contrib.auth.models import User, Group

def homepage(request):
    context = {}
    dados_home = Homepage.objects.all()
    context["dados_home"] = dados_home
    dados_agenda = Agenda.objects.all()
    context["dados_agenda"] = dados_agenda
    return render(request, 'homepage.html',context)


def teste(request):
    context = {}
    dados_home = Homepage.objects.all()
    context["dados_home"] = dados_home
    return render(request, 'teste.html')

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
                return render(request, "login.html", context)

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
            
            # Cria o usuário
            user = User.objects.create_user(username=var_user, email=var_email, password=var_password)
            user.first_name = var_first_name
            user.last_name = var_last_name
            user.save()
            
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
