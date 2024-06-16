from django import forms
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError
from .models import Agendamento
from datetime import datetime, timedelta, time

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
    assunto = forms.CharField(label="Assunto:", max_length=200, error_messages={'required': ''})
    data = forms.DateField(label='Data', widget=forms.DateInput(attrs={'type': 'date'}), error_messages={'required': ''})
    hora_entrada = forms.TimeField(label="Hora de entrada", widget=forms.TimeInput(attrs={'type': 'time'}), error_messages={'required': ''})
    hora_saida = forms.TimeField(label="Hora de saída", widget=forms.TimeInput(attrs={'type': 'time'}), error_messages={'required': ''})
    turma = forms.CharField(label="Turma:", max_length=100, error_messages={'required': ''})
    sala = forms.CharField(widget=forms.HiddenInput())
    agendamento_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    def clean_data(self):
        data = self.cleaned_data['data']
        hoje = datetime.now().date()
        dois_meses_futuro = hoje + timedelta(days=60)

        if data < hoje:
            raise ValidationError("Não é possível agendar para uma data anterior ao dia atual.")
        if data > dois_meses_futuro:
            raise ValidationError("Não é possível agendar para mais de dois meses no futuro.")

        return data

    def clean_hora_entrada(self):
        hora_entrada = self.cleaned_data['hora_entrada']
        if hora_entrada < time(7, 0) or hora_entrada > time(18, 0):
            raise ValidationError("O horário de entrada deve ser entre 07:00 e 18:00.")
        return hora_entrada

    def clean_hora_saida(self):
        hora_saida = self.cleaned_data['hora_saida']
        if hora_saida < time(7, 0) or hora_saida > time(18, 0):
            raise ValidationError("O horário de saída deve ser entre 07:00 e 18:00.")
        return hora_saida

    def clean(self):
        cleaned_data = super().clean()
        data = cleaned_data.get('data')
        hora_entrada = cleaned_data.get('hora_entrada')
        hora_saida = cleaned_data.get('hora_saida')
        sala = cleaned_data.get('sala')

        # Verificar se o horário de entrada é menor que o horário de saída
        if hora_entrada and hora_saida and hora_entrada >= hora_saida:
            raise ValidationError("O horário de entrada deve ser menor que o horário de saída.")
        # Verificar se estamos atualizando um agendamento existente
        agendamento_id = self.data.get('agendamento_id')
        if agendamento_id:
            try:
                agendamento_existente = Agendamento.objects.get(id=agendamento_id)
                if (data == agendamento_existente.data and
                    hora_entrada == agendamento_existente.hora_inicio and
                    hora_saida == agendamento_existente.hora_fim):
                    # Se data, hora de entrada e hora de saída não mudaram, ignoramos a verificação de conflito
                    return cleaned_data
            except Agendamento.DoesNotExist:
                pass

        # Verificar conflitos de horário apenas se houver dados para todos os campos necessários
        if data and hora_entrada and hora_saida and sala:
            agendamentos_conflitantes = Agendamento.objects.filter(
                sala=sala,
                data=data,
                hora_inicio__lt=hora_saida,
                hora_fim__gt=hora_entrada
            ).exclude(id=agendamento_id) 
            if agendamentos_conflitantes.exists():
                raise forms.ValidationError("Já existe um agendamento nesse horário para a sala selecionada.")

        return cleaned_data