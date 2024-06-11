from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Agenda (models.Model):
    titulo = models.CharField(max_length=50)
    logo = models.ImageField(upload_to="Logo/")

    def __str__(self):
        return self.titulo

class Homepage (models.Model):
    titulo = models.TextField(max_length=20)
    texto = models.TextField(max_length=500)
    imagem = models.ImageField(upload_to="imgHome/")

    def __str__(self):
        return self.titulo


class Login(models.Model):
    texto = models.TextField(max_length=500)

    def __str__(self):
        return self.texto



class Sala(models.Model):
    nome = models.CharField(max_length=20)
    corredor = models.TextField(max_length=50)
    descricao = models.TextField(max_length=500)
    capacidade = models.IntegerField()
    foto_sala = models.ImageField(upload_to="imgSala/" , default="imgSala/saladefault.png")

    def __str__(self):
        return self.nome

class Agendamento(models.Model):
    nome = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.DateField(default=timezone.now)
    # hora_inicio = models.TimeField(default=timezone.localtime().time)
    # hora_fim = models.TimeField(default=timezone.localtime().time)
    sala = models.ForeignKey(Sala,on_delete=models.CASCADE)
    turma = models.TextField(max_length= 30)
    assunto = models.TextField(max_length=200)

    def __str__(self):
        return self.nome

class Usuario(models.Model):
    cpf = models.CharField(max_length=11,unique=True)
    nome = models.ForeignKey(User, on_delete=models.CASCADE)
    foto_user = models.ImageField(upload_to="imgUser/", default= "imgUser/default.jpg")
        
    def __str__(self):
        return str(self.nome) 

