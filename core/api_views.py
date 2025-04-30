from rest_framework import viewsets
from .models import Formation
from .serializers import FormationSerializer

class FormationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows formations to be viewed or edited.
    """
    queryset = Formation.objects.all()
    serializer_class = FormationSerializer

    