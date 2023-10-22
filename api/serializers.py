from rest_framework import serializers
from teams.models import Person, Team


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'


class TeamSerializer(serializers.ModelSerializer):
    members = PersonSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = '__all__'


class TeamMember(serializers.Serializer):
    person_id = serializers.IntegerField()
