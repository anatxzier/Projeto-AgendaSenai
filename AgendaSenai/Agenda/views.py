from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login,logout as auth_logout
from .forms import FormLogin, FormCadastro, FormCadastroSala, FormsEdição, FormsAgendamento
from .models import Sala, Agenda, Homepage, Usuario, Agendamento
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse 
from django.core.cache import cache
from django.db.models.functions import Lower
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from datetime import datetime
from django.contrib.auth.decorators import user_passes_test

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


def group_required(group_name):
    def in_group(user):
        if user.is_authenticated:
            return user.groups.filter(name=group_name).exists()
        return False
    return user_passes_test(in_group)



@login_required
def agenda(request):
    context = {}
    dados_sala = Sala.objects.annotate(nome_lower=Lower('nome')).order_by('nome_lower')
    corredores = Sala.objects.values_list('corredor', flat=True).distinct().order_by('corredor')
    corredores = sorted(set(corredor.upper() for corredor in corredores))
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

@login_required
@group_required('Coordenador')
def usuarios(request):
    context = {}
    usuarios_professores = User.objects.filter(groups__name="Professor")
    dados_usuarios = Usuario.objects.filter(nome__in=usuarios_professores)
    context['dados_usuarios'] = dados_usuarios
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

    return render(request,'usuarios.html', context)


@login_required
@group_required('Coordenador')
def atualizar(request):
    if request.method == 'POST':
        form = FormsEdição(request.POST, request.FILES)
        if form.is_valid():
            try:
                user = get_object_or_404(User, username=form.cleaned_data['username'])
                user.first_name = form.cleaned_data['nome']
                user.last_name = form.cleaned_data['sobrenome']
                user.email = form.cleaned_data['email']
                user.save() 
                
                
                if 'foto' in request.FILES:
                    usuario = get_object_or_404(Usuario, nome=user) 
                    usuario.foto_user = form.cleaned_data['foto']
                    usuario.save()
                

                return redirect("usuarios")
            except User.DoesNotExist:
                print("deu errado user não existe")
                return redirect("usuarios")
        else:
            print(form.errors)  # Imprimir os erros de validação
    else:
        print("deu errado, método não é POST")

    return redirect("usuarios")

@login_required
@group_required('Coordenador')
def deletar(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        print(username)
        try:
            usuario = User.objects.get(username=username) 
            usuario.delete()
        except User.DoesNotExist:
            return redirect("usuarios")

    return redirect("usuarios")



@login_required
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

    Form_Inicial = {
        "nome": user_link.first_name,
        "sobrenome": user_link.last_name,
        "foto": usuario_link.foto_user,
        "email": user_link.email,
        "username": user_link.username
    }
    form = FormsEdição(initial=Form_Inicial)
    context['form'] = form
    return render(request, 'perfil.html', context)


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


from django.contrib import messages


@login_required
@group_required('Coordenador')
def cadastro(request):
    cache.clear()
    context = {}
    context["dados_agenda"] = Agenda.objects.all()
    context["dados_sala"] = Sala.objects.all()
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


    if request.method == "POST":
        form = FormCadastro(request.POST, request.FILES)
        if form.is_valid():
            try:
                var_first_name = form.cleaned_data['first_name']
                var_last_name = form.cleaned_data['last_name']
                var_user = form.cleaned_data['user']
                var_email = form.cleaned_data['email']
                var_password = form.cleaned_data['password']
                var_cpf = form.cleaned_data['cpf']

                # Verifica se o usuário enviou uma foto; caso contrário, usa a imagem padrão
                foto_user = form.cleaned_data['foto'] if 'foto' in request.FILES else 'imgUser/default.jpg'

                if User.objects.filter(username=var_user).exists() or not var_cpf.isdigit():
                    context['error_message'] = 'Nome de usuario ou cpf inválido, por favor tente novamente'
                    form = FormCadastro()
                    context['form'] = form
                    return render(request, "cadastro.html", context)
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
                    
                    return redirect('usuarios')
            except Exception as e:
                context['error_message'] = 'Ocorreu um erro durante o processamento do formulário.'
                # Adiciona o cabeçalho Cache-Control: no-cache na resposta HTTP
                form = FormCadastro()
                context['form'] = form
                
                return redirect("cadastro")
        else:
            form = FormCadastro()
            context['form'] = form
            return render(request, "cadastro.html", context)
    else:
        form = FormCadastro()
        context['form'] = form
        return render(request, "cadastro.html", context)
    
@login_required
@group_required('Coordenador')
def cadastroSala(request):
    context = {}
    context["dados_agenda"] = Agenda.objects.all()
    context["dados_sala"] = Sala.objects.all()

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

    if request.method == "POST":
        form = FormCadastroSala(request.POST, request.FILES)
        if form.is_valid():
            var_nome_sala = form.cleaned_data['nome_sala']
            var_corredor = form.cleaned_data['corredor']
            var_descricao = form.cleaned_data['descricao']
            var_capacidade = form.cleaned_data['capacidade']

            # Verifica se o usuário enviou uma foto; caso contrário, usa a cor padrão
            foto_sala = form.cleaned_data['foto'] if 'foto' in request.FILES else 'imgSala/saladefault.png'

            # Verifica se já existe uma sala com o mesmo nome
            if Sala.objects.filter(nome__iexact=var_nome_sala).exists():
                context['error_message'] = f"Já existe uma sala com o nome '{var_nome_sala}'. Por favor, escolha outro nome."
                context['form'] = form
                return render(request, "cadastroSala.html", context)
            else:
                sala = Sala(nome=var_nome_sala, corredor=var_corredor, descricao=var_descricao, capacidade=var_capacidade, foto_sala=foto_sala)
                sala.save()

                messages.success(request, 'Sala cadastrada com sucesso!')
                return redirect('cadastrosala')
        else:
            context['form'] = form
            return render(request, "cadastroSala.html", context)
    else:
        form = FormCadastroSala()
        context['form'] = form
        return render(request, "cadastroSala.html", context)
    
# @login_required
# @group_required('Coordenador')
# def atualizarsala(request):
#     if request.method == 'POST':
#         form = FormCadastroSala(request.POST, request.FILES)
#         if form.is_valid():
#             try:
#                 sala = get_object_or_404(Sala, nome=form.cleaned_data['nome'])
#                 sala.nome = form.cleaned_data['nome']
#                 sala.corredor = form.cleaned_data['corredor']
#                 sala.descricao = form.cleaned_data['descricao']
#                 sala.capacidade = form.cleaned_data['capacidade']
                
#                 # Atualiza a foto da sala, se fornecida
#                 if 'foto' in request.FILES:
#                     sala.foto_sala = form.cleaned_data['foto']
                
#                 # Salva a sala atualizada
#                 sala.save() 
                
#                 return redirect("agenda")
#             except Sala.DoesNotExist:
#                 print("A sala não existe")
#                 return redirect("agenda")
#         else:
#             print(form.errors)  # Imprime os erros de validação
#     else:
#         print("Algum erro foi encontrado, método não é POST")

#     return redirect("agenda")

@login_required
@group_required('Coordenador')
def atualizarsala(request):
    if request.method == 'POST':
        form = FormCadastroSala(request.POST, request.FILES)
        if form.is_valid():
            try:
                sala_id = form.cleaned_data['sala_id']
                sala = get_object_or_404(Sala, id=sala_id)

                sala.corredor = form.cleaned_data['corredor']
                sala.descricao = form.cleaned_data['descricao']
                sala.capacidade = form.cleaned_data['capacidade']

                if 'foto' in request.FILES:
                    sala.foto_sala = request.FILES['foto']

                sala.save()

                return redirect("agenda")
            except Sala.DoesNotExist:
                print("A sala não existe")
                return redirect("agenda")
        else:
            print(form.errors)  # Imprime os erros de validação
    else:
        print("Método não é POST")

    return redirect("agenda")

@login_required
@group_required('Coordenador')
def deletarsala(request):
    if request.method == 'POST':
        nome_sala = request.POST.get('nome_sala')
        print(nome_sala)
        try:
            sala = Sala.objects.get(nome=nome_sala) 
            sala.delete()
        except Sala.DoesNotExist:
            pass

    return redirect("agenda")

@login_required
def logout(request):
    auth_logout(request)
    return redirect("home")
    #return render(request, "teste.html")

@login_required
def agendarsala(request):
    context = {}
    dados_agenda = Agenda.objects.all()
    context["dados_agenda"] = dados_agenda
    dados_usuario = Usuario.objects.all()
    context["dados_usuario"] = dados_usuario
    dados_agendamento = Agendamento.objects.all()
    context["dados_agendamento"] = dados_agendamento

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

    if request.method == 'POST':

        if request.POST.get('sala_id'):
            sala_id = request.POST.get('sala_id')
            form_inicial = {
                'sala': sala_id
            }
            form = FormsAgendamento(initial=form_inicial)
        else:
            form = FormsAgendamento(request.POST)
        
        if form.is_valid():
            var_salaid = form.cleaned_data['sala']
            var_data = form.cleaned_data['data']
            var_assunto = form.cleaned_data['assunto']
            var_hora_entrada = form.cleaned_data['hora_entrada']
            var_hora_saida = form.cleaned_data['hora_saida']
            var_turma = form.cleaned_data['turma']
            
            sala = get_object_or_404(Sala, id=var_salaid)

            agendamento = Agendamento(nome=user, data=var_data, hora_inicio=var_hora_entrada, hora_fim=var_hora_saida, sala=sala, turma=var_turma, assunto=var_assunto)
            agendamento.save()
            
            return redirect(f'calendario/{var_salaid}')
        else:
            print("caiu para cá")
            context["form"] = form
            return render(request, 'agendarsala.html', context)
    else:
        # Método GET, inicializa um formulário vazio
        form = FormsAgendamento()
        context["form"] = form
        return render(request, 'agendarsala.html', context)

   



@login_required
##calendario
def calendario(request, id):
    context = {}
    context["dados_agenda"] = Agenda.objects.all()
    
    if request.user.is_authenticated:
        user = request.user
        context["userr"] = user
        print(type(user.username))
        # Buscar o perfil do usuário autenticado
        perfil_usuario = get_object_or_404(Usuario, nome=user)
        context['perfil_usuario'] = perfil_usuario

        user_is_coordenador = user.groups.filter(name='Coordenador').exists()
        context['user_is_coordenador'] = user_is_coordenador
        
    else:
        context["userr"] = None
        context['perfil_usuario'] = None
        context['user_is_coordenador'] = False

        
    
    sala = get_object_or_404(Sala, id=id)
    context['sala']= sala
    agendamentos = Agendamento.objects.filter(sala=sala)
    context['agendamentos'] = agendamentos
    form = FormsAgendamento()
    context['form'] = form
    return render(request,'calendar.html',context)

@login_required
def deletaragendamento(request):
    if request.method == 'POST':
        id_evento = request.POST.get('evento_id')
        id_sala = request.POST.get('sala_id')
        print(f'id evento--->{id_evento}')
        print(type(id_evento))
        print(f'id sala----> {id_sala}')
        try:
            agendamento = get_object_or_404(Agendamento, id = id_evento)
            agendamento.delete()
            
        except Agendamento.DoesNotExist:
            print("agendamento não existe")

    return redirect(f"calendario/{id_sala}")

@login_required
def atualizaragendamento(request):
    if request.method == 'POST':

        agendamento_id = request.POST.get('agendamento_id')
        sala_id = request.POST.get('sala')
        form = FormsAgendamento(request.POST)
        if form.is_valid():
            try:
                var_salaid = form.cleaned_data['sala']
                var_data = form.cleaned_data['data']
                var_assunto = form.cleaned_data['assunto']
                var_hora_entrada = form.cleaned_data['hora_entrada']
                var_hora_saida = form.cleaned_data['hora_saida']
                var_turma = form.cleaned_data['turma']
                sala = get_object_or_404(Sala, id=var_salaid)
                
                agendamento = get_object_or_404(Agendamento, id=agendamento_id)
                
                agendamento.data = var_data
                agendamento.hora_inicio = var_hora_entrada
                agendamento.hora_fim = var_hora_saida
                agendamento.assunto = var_assunto
                agendamento.turma = var_turma
                agendamento.save()

                messages.success(request, 'Agendamento atualizado com sucesso!')
                return redirect(f"calendario/{var_salaid}")
            except Sala.DoesNotExist:
                messages.error(request, 'A sala não existe.')
                return redirect("agenda")
        else:
            # Se o formulário não for válido, exibir erros específicos do formulário
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')

    return redirect(f'calendario/{sala_id}')

@login_required
@require_GET  # Certifica-se de que essa view só aceita requisições GET
def eventos(request, sala_id):
    if request.user.is_authenticated:
        user = request.user
        user_is_coordenador = user.groups.filter(name='Coordenador').exists()
    data = request.GET.get('data')  # Obtém a data dos parâmetros da URL
    if data:
        try:
            data = datetime.strptime(data, '%Y-%m-%d').date()  # Converte a string da data para um objeto datetime
        except ValueError:
            return JsonResponse({'error': 'Invalid date format'}, status=400)  # Retorna um erro se o formato da data for inválido
        
        agendamentos = Agendamento.objects.filter(sala__id=sala_id, data=data)  # Filtra os agendamentos pela sala e data
        eventos = [
            {   
                'id': agendamento.id,    
                'nome': agendamento.nome.username,
                'hora_inicio': agendamento.hora_inicio.strftime('%H:%M'),
                'hora_fim': agendamento.hora_fim.strftime('%H:%M'),
                'assunto': agendamento.assunto,
                'turma': agendamento.turma,
                'username': (agendamento.nome.username == user.username),
                'user_is_coordenador': user_is_coordenador
            }
            for agendamento in agendamentos
        ]  # Constrói uma lista de eventos para retornar como JSON
        return JsonResponse({'eventos': eventos})  # Retorna os eventos como JSON
    return JsonResponse({'error': 'No date provided'}, status=400)  # Retorna um erro se a data não for fornecida

##calendario

@login_required
def detalhes_evento(request, evento_id):
    evento = get_object_or_404(Agendamento, id=evento_id)

    detalhes = {
        'assunto': evento.assunto,
        'data': evento.data.strftime('%Y-%m-%d'),  # Formato da data como string
        'hora_inicio': evento.hora_inicio.strftime('%H:%M'),  # Formato da hora de início como string
        'hora_fim': evento.hora_fim.strftime('%H:%M'),  # Formato da hora de fim como string
        'turma': evento.turma,
        'sala': evento.sala.id,
        # Adicione outros campos conforme necessário
    }

    return JsonResponse(detalhes)