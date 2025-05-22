# core/serializers.py
from rest_framework import serializers
from .models import (CompletedTraining, User, Formation, Trainer, TrainingRoom, TrainingWish,
                    Session, SessionParticipant, Notification)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                 'rpe_association', 'code_postal', 'city', 'latitude', 'longitude')
        extra_kwargs = {'password': {'write_only': True}}

class FormationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Formation
        fields = '__all__'

class TrainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trainer
        fields = '__all__'

class SessionSerializer(serializers.ModelSerializer):
    trainers = TrainerSerializer(many=True, read_only=True)

    class Meta:
        model = Session
        fields = '__all__'

class TrainingWishSerializer(serializers.ModelSerializer):
    formation = FormationSerializer(read_only=True)
    class Meta:
        model = TrainingWish    
        fields = '__all__'

class CompletedTrainingSerializer(serializers.ModelSerializer):
    formation_name = serializers.CharField(source='formation.name', read_only=True)

    class Meta:
        model = CompletedTraining
        fields = ['id', 'formation_name', 'completion_date']
