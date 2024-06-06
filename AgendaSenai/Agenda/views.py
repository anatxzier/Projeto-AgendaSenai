from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login,logout as auth_logout
from .forms import FormLogin, FormCadastro, FormsAgendarData, FormCadastroSala
from .models import Sala, Agenda, Homepage, Usuario
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page


from .forms import FormCadastro


def homepage(request):
    context = {}
    dados_home = Homepage.objects.all()
    context["dados_home"] = dados_home
    dados_agenda = Agenda.objects.all()
    context["dados_agenda"] = dados_agenda
    dados_usuario = Usuario.objects.all()
    context["dados_usuario"] = dados_usuario
    if request.user.is_authenticated:
        user = request.user
        context["userr"] = user
        print(user.username)
        
        # Buscar o perfil do usuário autenticado
        perfil_usuario = get_object_or_404(Usuario, nome=user)
        context['perfil_usuario'] = perfil_usuario

        user_is_coordenador = user.groups.filter(name='Coordenador').exists()
        context['user_is_coordenador'] = user_is_coordenador
    else:
        context["userr"] = None
        context['perfil_usuario'] = None
        context['user_is_coordenador'] = False
    
    return render(request, 'homepage.html',context)


def agenda(request):
    context = {}
    dados_sala = Sala.objects.all().order_by('nome')
    corredores = Sala.objects.values_list('corredor', flat=True).distinct().order_by('corredor')
    context['dados_sala'] = dados_sala
    context['corredores'] = corredores
    dados_agenda = Agenda.objects.all()
    context["dados_agenda"] = dados_agenda  
    if request.user.is_authenticated:
        user = request.user
        context["userr"] = user
        
        # Buscar o perfil do usuário autenticado
        perfil_usuario = get_object_or_404(Usuario, nome=user)
        context['perfil_usuario'] = perfil_usuario

        user_is_coordenador = user.groups.filter(name='Coordenador').exists()
        context['user_is_coordenador'] = user_is_coordenador
        
    else:
        context["userr"] = None
        context['perfil_usuario'] = None
        context['user_is_coordenador'] = False

    return render(request, 'agendacoor.html', context)

def usuarios(request):
    context = {}
    dados_usuarios = Usuario.objects.all()
    context['dados_usuarios'] = dados_usuarios
    dados_agenda = Agenda.objects.all()
    context["dados_agenda"] = dados_agenda
    if request.user.is_authenticated:
        user = request.user
        context["userr"] = user
        print(user.username)
        
        # Buscar o perfil do usuário autenticado
        perfil_usuario = get_object_or_404(Usuario, nome=user)
        context['perfil_usuario'] = perfil_usuario

        user_is_coordenador = user.groups.filter(name='Coordenador').exists()
        context['user_is_coordenador'] = user_is_coordenador
    else:
        context["userr"] = None
        context['perfil_usuario'] = None
        context['user_is_coordenador'] = False

    return render(request,'usuarios.html', context)

def perfil(request, id):
    context = {}
    dados_usuarios = Usuario.objects.all()
    context['dados_usuarios'] = dados_usuarios
    dados_agenda = Agenda.objects.all()
    context['dados_agenda'] = dados_agenda
    
    if request.user.is_authenticated:
        user = request.user
        context["userr"] = user
        
        # Buscar o perfil do usuário autenticado
        perfil_usuario = get_object_or_404(Usuario, nome=user)
        context['perfil_usuario'] = perfil_usuario

        user_is_coordenador = user.groups.filter(name='Coordenador').exists()
        context['user_is_coordenador'] = user_is_coordenador
    else:
        context["userr"] = None
        context['perfil_usuario'] = None
        context['user_is_coordenador'] = False

    

    usuario_link = get_object_or_404(Usuario, id=id)
    context['usuario'] = usuario_link
    
    user_link = get_object_or_404(User, username=usuario_link.nome)
    context['user_link'] = user_link
    return render(request, 'perfil.html', context)



# def teste(request):
#     context = {}
#     if request.method == 'POST':
#         form = FormsAgendarData(request.POST)
#         if form.is_valid():
#             data = form.cleaned_data['data']
#             now = timezone.localtime(timezone.now()) 
#             # Verifica se a data está dentro do intervalo de agora até dois meses no futuro
#             if data <= now or data > now + timedelta(days=60):
#                 return HttpResponse("O agendamento deve ser entre agora e daqui a dois meses.")
#             # Verifica se a hora está entre 7 e 18 horas
#             if data.hour < 7 or data.hour >= 18:
#                 return HttpResponse("O agendamento deve ser entre as 7h e as 18h.")
#             # Se tudo estiver correto, você pode prosseguir com o processamento do formulário
#             return render(request, 'teste.html', {'form': form})
#     else:
#         form = FormsAgendarData()
#         context['form'] = form
#         return render(request, 'teste.html', context)

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
                
                return redirect('home')
            else:
                form = FormLogin()
                context['form'] = form
                context['error'] = "Usuário ou senha incorretas"
                return render(request, "login.html", context)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = FormLogin()
        context['form'] = form
        # Vou redenrizar o que foi criado no arquivo forms
        return render(request, "login.html", context)

@cache_page(30)
def cadastro(request):
    context = {}
    dados_agenda = Agenda.objects.all()
    context["dados_agenda"] = dados_agenda  
    dados_sala = Sala.objects.all()
    context["dados_sala"] = dados_sala

    if request.method == "POST":
        form = FormCadastro(request.POST, request.FILES)
        if form.is_valid():
            var_first_name = form.cleaned_data['first_name']
            var_last_name = form.cleaned_data['last_name']
            var_user = form.cleaned_data['user']
            var_email = form.cleaned_data['email']
            var_password = form.cleaned_data['password']
            var_cpf = form.cleaned_data['cpf']

            # Verifica se o usuário enviou uma foto; caso contrário, usa a imagem padrão
            foto_user = form.cleaned_data['foto'] if 'foto' in request.FILES else 'imgUser/default.jpg'

            if User.objects.filter(username=var_user).exists():
                context['error_message'] = 'Este nome de usuário já existe! Por favor, escolha outro.'
                form = FormCadastro()
                context['form'] = form
                render(request, "cadastro.html", context)

            else:
            # Cria o usuário
                user = User.objects.create_user(username=var_user, email=var_email, password=var_password)
                user.first_name = var_first_name
                user.last_name = var_last_name
                user.save()

                # Cria o perfil do usuário
                usuario = Usuario(cpf=var_cpf, nome=user, foto_user=foto_user)
                usuario.save()

                # Adiciona o usuário ao grupo
                group = Group.objects.get(name='Professor')
                user.groups.add(group)

                return redirect('home')
        else:
            form = FormCadastro()
            context['form'] = form
            render(request, "cadastro.html", context)
    else:
        form = FormCadastro()
        context['form'] = form
    
    print(context)
    return render(request, "cadastro.html", context)

def cadastroSala(request):
    context = {}
    dados_agenda = Agenda.objects.all()
    context["dados_agenda"] = dados_agenda  
    dados_sala = Sala.objects.all()
    context["dados_sala"] = dados_sala

    if request.method == "POST":
        form = FormCadastroSala(request.POST, request.FILES)
        if form.is_valid():
            var_nome_sala = form.cleaned_data['nome_sala']
            var_corredor = form.cleaned_data['corredor']
            var_descricao = form.cleaned_data['descricao']
            var_capacidade = form.cleaned_data['capacidade']

            # Verifica se o usuário enviou uma foto; caso contrário, usa a cor padrão
            foto_sala = form.cleaned_data['foto'] if 'foto' in request.FILES else 'imgSala/saladefault.png'

            sala = Sala(nome=var_nome_sala, corredor=var_corredor, descricao=var_descricao, capacidade=var_capacidade, foto_sala=foto_sala)
            sala.save()

            return render(request, "agenda.html", context)
        else:
            context['form'] = form
    else:
        form = FormCadastroSala()
        context['form'] = form
    
    return render(request, "cadastroSala.html", context)


def logout(request):
    auth_logout(request)
    return redirect("home")
    #return render(request, "teste.html")

