from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Agenda (models.Model):
    titulo = models.CharField(max_length=50)
    logo = models.ImageField(upload_to="Logo")

    def __str__(self):
        return self.titulo

class Homepage (models.Model):
    titulo = models.TextField(max_length=20)
    texto = models.TextField(max_length=500)
    imagem = models.ImageField(upload_to="imgHome")

class Login(models.Model):
    texto = models.TextField(max_length=500)

class Sala(models.Model):
    nome = models.CharField(max_length=20)
    descricao = models.TextField(max_length=500)
    equipamento = models.TextField(max_length=500)
    capacidade = models.IntegerField(max_length=3)
    foto = models.ImageField(upload_to="imgSala")

    def __str__(self):
        return self.nome

class Agendamento(models.Model):
    nome = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.DateTimeField(default=timezone.now)
    sala = models.ForeignKey(Sala,on_delete=models.CASCADE)
    turma = models.TextField(max_length= 30)
    assunto = models.TextField(max_length=200)

class Usuario(models.Model):
    cpf = models.IntegerField(max_length=11)
    nome = models.ForeignKey(User, on_delete=models.CASCADE)
    foto_user = models.ImageField(upload_to="imgUser")
        


