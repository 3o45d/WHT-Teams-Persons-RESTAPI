from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.serializers import PersonSerializer, TeamSerializer, TeamMember
from teams.models import Person, Team


class PersonViewSet(viewsets.ModelViewSet):
    serializer_class = PersonSerializer
    queryset = Person.objects.all()

    class Meta:
        swagger_tags =['Команды']

    """ GET /persons/ """

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: openapi.Response(description="Успешное получение списка", schema=PersonSerializer()),
        }
    )
    def list(self, request, **kwargs):
        # Обработка GET /persons/
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    """ POST /persons/ """

    @swagger_auto_schema(
        responses={
            status.HTTP_201_CREATED: openapi.Response(description="Успешное создание человека",
                                                      schema=PersonSerializer()),
            status.HTTP_400_BAD_REQUEST: "Ошибка в переданных данных"
        }
    )
    def create(self, request, *args, **kwargs):
        # Обработка POST /persons/
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """ GET /persons/{id}/ """

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: openapi.Response(description="Успешное получение информации об человеке.",
                                                 schema=PersonSerializer()),
            status.HTTP_404_NOT_FOUND: "Человек с указанным ID не найден."
        }
    )
    def retrieve(self, request, pk=None, *args, **kwargs):
        # Обработка GET /persons/{id}/
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Person.DoesNotExist:
            return Response(data={"detail": "Человек с указанным ID не найден."}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: openapi.Response(description="Успешное обновление данных о человеке.",
                                                 schema=PersonSerializer()),
            status.HTTP_400_BAD_REQUEST: "Ошибка в переданных данных.",
            status.HTTP_404_NOT_FOUND: "Человек с указанным ID не найден."
        }
    )
    def update(self, request, pk=None, *args, **kwargs):
        # Обработка PUT /persons/{id}/
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Person.DoesNotExist:
            return Response(data={"detail": "Человек с указанным ID не найден"}, status=status.HTTP_404_NOT_FOUND)

    """ PATCH /persons/{id}/ """

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: openapi.Response(description="Успешное частичное обновление данных о человеке.",
                                                 schema=PersonSerializer()),
            status.HTTP_400_BAD_REQUEST: "Ошибка в переданных данных.",
            status.HTTP_404_NOT_FOUND: "Человек с указанным ID не найден."
        }
    )
    def partial_update(self, request, pk=None, *args, **kwargs):
        # Обработка PATCH /persons/{id}/

        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Person.DoesNotExist:
            return Response(data={"detail": "Человек с указанным ID не найден"}, status=status.HTTP_404_NOT_FOUND)

    """ DELETE /persons/{id}/ """

    @swagger_auto_schema(
        responses={
            status.HTTP_204_NO_CONTENT: "Успешное удаление человека.",
            status.HTTP_404_NOT_FOUND: "Человек с указанным ID не найден."
        }
    )
    def destroy(self, request, pk=None, *args, **kwargs):
        # Обработка DELETE /persons/{id}/

        try:
            instance = self.get_object()
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Person.DoesNotExist:
            return Response(data={"detail": "Человек с указанным ID не найден"}, status=status.HTTP_404_NOT_FOUND)


class TeamViewSet(viewsets.ModelViewSet):
    serializer_class = TeamSerializer
    queryset = Team.objects.all()

    """ GET /teams/ """

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: openapi.Response(description="Успешное получение списка команд",
                                                 schema=TeamSerializer(many=True)),
        }
    )
    def list(self, request, **kwargs):
        # Обработка GET /teams/
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    """ POST /teams/ """

    @swagger_auto_schema(
        responses={
            status.HTTP_201_CREATED: openapi.Response(description="Успешное создание команды", schema=TeamSerializer()),
            status.HTTP_400_BAD_REQUEST: "Ошибка в переданных данных"
        }
    )
    def create(self, request, *args, **kwargs):
        # Обработка POST /teams/ (teams_create)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """ GET /teams/{id}/ """

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: openapi.Response(description="Успешное получение деталей команды",
                                                 schema=TeamSerializer()),
            status.HTTP_404_NOT_FOUND: "Команда с указанным ID не найдена"
        }
    )
    def retrieve(self, request, pk=None, *args, **kwargs):
        # Обработка GET /teams/{id}/
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Team.DoesNotExist:
            return Response(data={"detail": "Команда с указанным ID не найдена"}, status=status.HTTP_404_NOT_FOUND)

    """ PUT /teams/{id}/ """

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: openapi.Response(description="Успешное обновление данных о команде",
                                                 schema=TeamSerializer()),
            status.HTTP_400_BAD_REQUEST: "Ошибка в переданных данных",
            status.HTTP_404_NOT_FOUND: "Команда с указанным ID не найдена"
        }
    )
    def update(self, request, pk=None, *args, **kwargs):
        # Обработка PUT /teams/{id}/
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Team.DoesNotExist:
            return Response(data={"detail": "Команда с указанным ID не найдена"}, status=status.HTTP_404_NOT_FOUND)

    """ PATCH /teams/{id}/ """

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: openapi.Response(description="Успешное частичное обновление данных о команде",
                                                 schema=TeamSerializer()),
            status.HTTP_400_BAD_REQUEST: "Ошибка в переданных данных",
            status.HTTP_404_NOT_FOUND: "Команда с указанным ID не найдена"
        }
    )
    def partial_update(self, request, pk=None, *args, **kwargs):
        # Обработка PATCH /teams/{id}/
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Team.DoesNotExist:
            return Response(data={"detail": "Команда с указанным ID не найдена"}, status=status.HTTP_404_NOT_FOUND)

    """ DELETE /teams/{id}/ """

    @swagger_auto_schema(
        responses={
            status.HTTP_204_NO_CONTENT: "Успешное удаление команды",
            status.HTTP_404_NOT_FOUND: "Команда с указанным ID не найдена"
        }
    )
    def destroy(self, request, pk=None, *args, **kwargs):
        # Обработка DELETE /teams/{id}/
        try:
            instance = self.get_object()
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Team.DoesNotExist:
            return Response(data={"detail": "Команда с указанным ID не найдена"}, status=status.HTTP_404_NOT_FOUND)

    """ POST /teams/{id}/add_member/ """

    @swagger_auto_schema(
        method='post',
        responses={
            status.HTTP_200_OK: openapi.Response(description="Успешное добавление члена в команду."),
            status.HTTP_400_BAD_REQUEST: "Ошибка в переданных данных или пользователь уже в команде.",
            status.HTTP_404_NOT_FOUND: "Команда или человек с указанным ID не найдены."
        }
    )
    @action(detail=True, methods=['post'], url_path='add_member', serializer_class=TeamMember)
    # Обработка POST /teams/{id}/add_member/
    def add_member(self, request, pk=None):
        team = self.get_object()
        person_id = request.data.get('person_id')
        try:
            person = Person.objects.get(id=person_id)
        except Person.DoesNotExist:
            return Response({'status': 'person not found'}, status=404)
        team.members.add(person)
        return Response({'status': 'member added'})

    """ POST /teams/{id}/remove_member/ """

    @swagger_auto_schema(
        method='post',
        responses={
            status.HTTP_200_OK: openapi.Response(description="Успешное удаление члена из команды."),
            status.HTTP_400_BAD_REQUEST: "Ошибка в переданных данных или пользователь не является членом команды.",
            status.HTTP_404_NOT_FOUND: "Команда или человек с указанным ID не найдены."
        }
    )
    @action(detail=True, methods=['post'], url_path='remove_member', serializer_class=TeamMember)
    def remove_member(self, request, pk=None):
        # Обработка POST /teams/{id}/remove_member/
        team = self.get_object()
        person_id = request.data.get('person_id')

        try:
            person = Person.objects.get(id=person_id)
        except Person.DoesNotExist:
            return Response({'status': 'person not found'}, status=404)

        if person not in team.members:
            return Response({'status': 'member removed'})

        team.members.remove(person)
