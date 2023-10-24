from rest_framework import status
from rest_framework.test import APITestCase

from api.serializers import TeamSerializer
from teams.models import Person, Team


class TeamAPITests(APITestCase):
    base_url = '/api/v1/teams/'

    def setUp(self):
        self.team = Team.objects.create(name='Test Team', description='This is a test team')
        self.person = Person.objects.create(first_name="Viktoria", last_name="Kit", email="viki.kit@example.com")

    def test_list_teams(self):
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_team(self):
        data = {'name': 'New Team', 'description': 'This is a new test team'}
        response = self.client.post(self.base_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Team.objects.count(), 2)

    def test_retrieve_team(self):
        response = self.client.get(f'{self.base_url}{self.team.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, TeamSerializer(self.team).data)

    def test_update_team(self):
        data = {'name': 'Updated Team Name'}
        response = self.client.put(f'{self.base_url}{self.team.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.team.refresh_from_db()
        self.assertEqual(self.team.name, 'Updated Team Name')

    def test_partial_update_team(self):
        data = {'description': 'Updated Description'}
        response = self.client.patch(f'{self.base_url}{self.team.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.team.refresh_from_db()
        self.assertEqual(self.team.description, 'Updated Description')

    def test_delete_team(self):
        response = self.client.delete(f'{self.base_url}{self.team.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Team.objects.count(), 0)

    def test_add_member_to_team(self):
        data = {'person_id': self.person.id}
        response = self.client.post(f'{self.base_url}{self.team.id}/add_member/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.person in self.team.members.all())

    def test_remove_member_from_team(self):
        self.team.members.add(self.person)
        data = {'person_id': self.person.id}
        response = self.client.post(f'{self.base_url}{self.team.id}/remove_member/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.person in self.team.members.all())

    def test_create_team_invalid_data(self):
        data = {'name': ''}
        response = self.client.post(f'{self.base_url}', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_team_not_found(self):
        response = self.client.get(f'{self.base_url}1000/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_existing_member_to_team(self):
        self.team.members.add(self.person)
        data = {'person_id': self.person.id}
        response = self.client.post(f'{self.base_url}{self.team.id}/add_member/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
