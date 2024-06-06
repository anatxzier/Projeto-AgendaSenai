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
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)
    cpf = forms.CharField(label="CPF", max_length=11)
    foto = forms.ImageField(label="Foto de Perfil", required=False)

class FormCadastroSala(forms.Form):
    nome_sala = forms.CharField(label="Nome da Sala:", max_length=30)
    corredor = forms.CharField(label='Corredor:', max_length= 20)
    descricao = forms.CharField(label="Descrição:", max_length=40)
    capacidade = forms.IntegerField(label='Capacidade:', min_value=0)
    foto = forms.ImageField(label="Foto da Sala:", required=False)

class FormsAgendarData(forms.Form):
    data = forms.DateTimeField(label='Data e Hora do Agendamento',
                               widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
                               input_formats=['%Y-%m-%d %H:%M:%S'])
    