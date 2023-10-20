from django.shortcuts import render
from rest_framework import viewsets
from api.serializers import PersonSerializer, TeamSerializer
from teams.models import Person, Team


class PersonViewSet(viewsets.ModelViewSet):
    serializer_class = PersonSerializer
    queryset = Person.objects.all()


class TeamViewSet(viewsets.ModelViewSet):
    serializer_class = TeamSerializer
    queryset = Team.objects.all()
