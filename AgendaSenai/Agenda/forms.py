from django import forms
from django.utils import timezone
from datetime import timedelta


class FormLogin(forms.Form):
    user = forms.CharField(label='Usuário', max_length=20)
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)

class FormCadastro(forms.Form):
    user = forms.CharField(label="Nome de Usuário", max_length=30)
    first_name = forms.CharField(label='Nome', max_length= 20)
    last_name = forms.CharField(label="Sobrenome", max_length=40)
    email = forms.EmailField(label="Email", max_length=60)
    password = forms.CharField(label='Senha', widget=forms.PasswordInput, min_length=8)
    cpf = forms.CharField(label="CPF", min_length=11,max_length=11)
    foto = forms.ImageField(label="Foto de Perfil", required=False)

class FormCadastroSala(forms.Form):
    nome_sala = forms.CharField(label="Nome da Sala", max_length=30)
    corredor = forms.CharField(label='Corredor', max_length= 20)
    descricao = forms.CharField(label="Descrição", max_length=40)
    capacidade = forms.IntegerField(label='Capacidade', min_value=0)
    foto = forms.ImageField(label="Foto da Sala", required=False)

class FormsEdição(forms.Form):
    nome = forms.CharField(label="Nome:",max_length=15)
    sobrenome = forms.CharField(label="Sobrenome:", max_length=50)
    foto = forms.ImageField(label="Foto de usuário:", required=False)
    email = forms.EmailField(label="Email:", max_length=60)
    username = forms.CharField(widget=forms.HiddenInput())

class FormsAgendamento(forms.Form):
    assunto = forms.CharField(label="Assunto:", max_length=200)
    data = forms.DateField(label='Data', widget=forms.DateTimeInput(attrs={'type': 'date'}))
    hora_entrada = forms.TimeField(label="Hora de entrada", widget=forms.DateTimeInput(attrs={'type': 'time'}))
    hora_saida = forms.TimeField(label="Hora de saída", widget=forms.DateTimeInput(attrs={'type': 'time'}))
    turma = forms.CharField(label="Turma:", max_length=100)

