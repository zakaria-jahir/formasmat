from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny

from .serializers import *
from .models import *

# 🔐 Authentification personnalisée : retourne un token + infos utilisateur
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


# 👤 API Utilisateurs
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['GET'])
    def profile(self, request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)


# 🎓 API Formations (publique)
class FormationViewSet(viewsets.ModelViewSet):
    queryset = Formation.objects.all()
    serializer_class = FormationSerializer
    permission_classes = [AllowAny]


# 🗓️ API Sessions de formation (publique)
class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes = [AllowAny]

    # ✅ Ajout d’un participant à une session
    @action(detail=True, methods=['POST'])
    def add_participant(self, request, pk=None):
        session = self.get_object()
        user_id = request.data.get('user_id')

        if not user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Vérifier si le participant existe déjà
        if SessionParticipant.objects.filter(session=session, user=user).exists():
            return Response({'error': 'Participant already exists in session'}, status=status.HTTP_409_CONFLICT)

        # Ajouter le participant
        SessionParticipant.objects.create(
            session=session,
            user=user,
            status='CONTACTED'
        )
        return Response({'status': 'Participant added successfully'}, status=status.HTTP_201_CREATED)
