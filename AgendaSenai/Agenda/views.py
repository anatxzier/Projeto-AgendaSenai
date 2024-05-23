from django.shortcuts import render, HttpResponse

def homepage(request):
    return HttpResponse ("<h1>Olá mundo</h1>")


# Create your views here.
