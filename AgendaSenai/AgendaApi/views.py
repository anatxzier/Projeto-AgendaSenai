from rest_framework import viewsets
from Agenda.models import Sala 
from .serializers import SalaSerializer

class SalaViewSet(viewsets.ModelViewSet):
    queryset = Sala.objects.all()
    serializer_class = SalaSerializer

# Create your views here.
