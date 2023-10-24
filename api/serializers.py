from rest_framework import serializers
from teams.models import Person, Team
from rest_framework.validators import UniqueValidator
import re

NAME_FORMAT = r"^[a-zA-Zа-яА-ЯЁёіІїЇ]+$"


class PersonSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=Person.objects.all())])

    class Meta:
        model = Person
        fields = '__all__'

    def validate_first_name(self, value: str) -> str:
        if not re.match(NAME_FORMAT, value):
            raise serializers.ValidationError("First name can only contain letters.")
        return value

    def validate_last_name(self, value: str) -> str:
        if not re.match(NAME_FORMAT, value):
            raise serializers.ValidationError("Last name can only contain letters.")
        return value


class TeamSerializer(serializers.ModelSerializer):
    members = PersonSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = '__all__'

    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Team name should be at least 3 characters long.")
        return value


class TeamMember(serializers.Serializer):
    person_id = serializers.IntegerField()
