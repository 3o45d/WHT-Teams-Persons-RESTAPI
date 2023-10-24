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

    """ Endpoint to retrieve all persons """

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Successfully retrieved list.", schema=PersonSerializer()
            ),
        }
    )
    def list(self, request, **kwargs):
        """ Handle GET /persons/ """
        queryset = self.queryset
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    """ Endpoint to create a new person """

    @swagger_auto_schema(
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description="Successfully created person.",
                schema=PersonSerializer()
            ),
            status.HTTP_400_BAD_REQUEST: "Error in the provided data."
        }
    )
    def create(self, request, *args, **kwargs):
        """ Handle POST /persons/ """
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """ Endpoint to retrieve a specific person by ID """

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Successfully retrieved person's information.",
                schema=PersonSerializer()
            ),
            status.HTTP_404_NOT_FOUND: "Person with the specified ID not found."
        }
    )
    def retrieve(self, request, pk=None, *args, **kwargs):
        """ Handle GET /persons/{id}/ """
        try:
            instance = self.get_object()
            serializer = self.serializer_class(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Person.DoesNotExist:
            return Response(
                data={"detail": "Person with the specified ID not found."},
                status=status.HTTP_404_NOT_FOUND
            )

    """ Endpoint to update a person's details """

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Successfully updated person's data.",
                schema=PersonSerializer()
            ),
            status.HTTP_400_BAD_REQUEST: "Error in the provided data.",
            status.HTTP_404_NOT_FOUND: "Person with the specified ID not found."
        }
    )
    def update(self, request, pk=None, *args, **kwargs):
        """ Handle PUT /persons/{id}/ """
        try:
            instance = self.get_object()
            serializer = self.serializer_class(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Person.DoesNotExist:
            return Response(
                data={"detail": "Person with the specified ID not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    """ Endpoint to partially update a person's details """

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Successfully partially updated person's data.",
                schema=PersonSerializer()
            ),
            status.HTTP_400_BAD_REQUEST: "Error in the provided data.",
            status.HTTP_404_NOT_FOUND: "Person with the specified ID not found."
        }
    )
    def partial_update(self, request, pk=None, *args, **kwargs):
        """ Handle PATCH /persons/{id}/ """
        try:
            instance = self.get_object()
            serializer = self.serializer_class(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Person.DoesNotExist:
            return Response(data={"detail": "Person with the specified ID not found"}, status=status.HTTP_404_NOT_FOUND)

    """ Endpoint to delete a specific person by ID """

    @swagger_auto_schema(
        responses={
            status.HTTP_204_NO_CONTENT: "Successfully deleted person.",
            status.HTTP_404_NOT_FOUND: "Person with the specified ID not found."
        }
    )
    def destroy(self, request, pk=None, *args, **kwargs):
        """ Handle DELETE /persons/{id}/ """
        try:
            instance = self.get_object()
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Person.DoesNotExist:
            return Response(
                data={"detail": "Person with the specified ID not found"},
                status=status.HTTP_404_NOT_FOUND
            )


class TeamViewSet(viewsets.ModelViewSet):
    serializer_class = TeamSerializer
    queryset = Team.objects.all()

    """ Endpoint to retrieve all teams """

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Successfully retrieved list of teams.",
                schema=TeamSerializer(many=True)
            ),
        }
    )
    def list(self, request, **kwargs):
        """ Handle GET /teams/ """
        queryset = self.queryset
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    """ Endpoint to create a new team """

    @swagger_auto_schema(
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description="Successfully created team.",
                schema=TeamSerializer()
            ),
            status.HTTP_400_BAD_REQUEST: "Error in the provided data."
        }
    )
    def create(self, request, *args, **kwargs):
        """ Handle POST /teams/ """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """ Endpoint to retrieve team details by ID """

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Successfully retrieved team details.",
                schema=TeamSerializer()
            ),
            status.HTTP_404_NOT_FOUND: "Team with the given ID not found."
        }
    )
    def retrieve(self, request, pk=None, *args, **kwargs):
        """ Handle GET /teams/{id}/ """
        try:
            instance = self.get_object()
            serializer = self.serializer_class(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Team.DoesNotExist:
            return Response(
                data={"detail": "Team with the given ID not found."},
                status=status.HTTP_404_NOT_FOUND
            )

    """ Endpoint to update team details by ID """

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Successfully updated team details.",
                schema=TeamSerializer()
            ),
            status.HTTP_400_BAD_REQUEST: "Error in the provided data.",
            status.HTTP_404_NOT_FOUND: "Team with the given ID not found."
        }
    )
    def update(self, request, pk=None, *args, **kwargs):
        """ Handle PUT /teams/{id}/ """
        try:
            instance = self.get_object()
            serializer = self.serializer_class(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Team.DoesNotExist:
            return Response(
                data={"detail": "Team with the given ID not found."},
                status=status.HTTP_404_NOT_FOUND
            )

    """ Endpoint to partially update team details by ID """

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Successfully partially updated team details.",
                schema=TeamSerializer()
            ),
            status.HTTP_400_BAD_REQUEST: "Error in the provided data.",
            status.HTTP_404_NOT_FOUND: "Team with the given ID not found."
        }
    )
    def partial_update(self, request, pk=None, *args, **kwargs):
        """ Handle PATCH /teams/{id}/ """
        try:
            instance = self.get_object()
            serializer = self.serializer_class(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Team.DoesNotExist:
            return Response(
                data={"detail": "Team with the given ID not found."},
                status=status.HTTP_404_NOT_FOUND
            )

    """ Endpoint to delete a team by ID """

    @swagger_auto_schema(
        responses={
            status.HTTP_204_NO_CONTENT: "Successfully deleted the team.",
            status.HTTP_404_NOT_FOUND: "Team with the given ID not found."
        }
    )
    def destroy(self, request, pk=None, *args, **kwargs):
        """ Handle DELETE /teams/{id}/ """
        try:
            instance = self.get_object()
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Team.DoesNotExist:
            return Response(
                data={"detail": "Team with the given ID not found."},
                status=status.HTTP_404_NOT_FOUND
            )

    """ Endpoint to add a member to the team by ID """

    @swagger_auto_schema(
        method='post',
        responses={
            status.HTTP_200_OK: openapi.Response(description="Successfully added member to the team."),
            status.HTTP_400_BAD_REQUEST: "Error in the provided data or user is already a team member.",
            status.HTTP_404_NOT_FOUND: "Team or person with the given ID not found."
        }
    )
    @action(detail=True, methods=['post'], url_path='add_member', serializer_class=TeamMember)
    def add_member(self, request, pk=None):
        """ Handle POST /teams/{id}/add_member/ """
        try:
            team = self.get_object()
        except Team.DoesNotExist:
            return Response(
                data={'status': 'Team with the given ID not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        person_id = request.data.get('person_id')
        try:
            person = Person.objects.get(id=person_id)
        except Person.DoesNotExist:
            return Response(
                data={'status': 'Person with the given ID not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        team.members.add(person)
        return Response(
            data={'status': 'Successfully added member to the team.'},
            status=status.HTTP_200_OK
        )

    """ Endpoint to remove a member from the team by ID """

    @swagger_auto_schema(
        method='post',
        responses={
            status.HTTP_200_OK: openapi.Response(description="Successfully removed member from the team."),
            status.HTTP_400_BAD_REQUEST: "Error in the provided data or user is not a team member.",
            status.HTTP_404_NOT_FOUND: "Team or person with the given ID not found."
        }
    )
    @action(detail=True, methods=['post'], url_path='remove_member', serializer_class=TeamMember)
    def remove_member(self, request, pk=None):
        """ Handle POST /teams/{id}/remove_member/ """
        try:
            team = self.get_object()
            person_id = request.data.get('person_id')
        except Team.DoesNotExist:
            return Response(
                data={'status': 'Team with the given ID not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            person = Person.objects.get(id=person_id)
        except Person.DoesNotExist:
            return Response(
                data={'status': 'Person with the given ID not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        if person not in team.members:
            return Response(
                data={'status': 'Error in the provided data or user is not a team member'},
                status=status.HTTP_400_BAD_REQUEST
            )

        team.members.remove(person)
        return Response(
            data={'status': 'Successfully removed member from the team'},
            status=status.HTTP_200_OK
        )
