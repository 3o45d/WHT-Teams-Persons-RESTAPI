from rest_framework.test import APIClient, APITestCase

from api.serializers import PersonSerializer
from teams.models import Person


class PersonAPITest(APITestCase):
    base_url = '/api/v1/persons/'

    def setUp(self):
        self.client = APIClient()
        self.person1 = Person.objects.create(first_name="Viktoria", last_name="Kit", email="viki.kit@example.com")
        self.person2 = Person.objects.create(first_name="Matviy", last_name="Luxe", email="matviy.luxe@example.com")

        self.valid_payload = {
            'first_name': 'Andrii',
            'last_name': 'Shevchenko',
            'email': 'a.shevchenko@example.com'
        }

        self.invalid_payload = {
            'first_name': '',
            'last_name': '',
            'email': 'a.shevchenko@example.com'
        }

    def test_get_all_persons(self):
        response = self.client.get(self.base_url)
        persons = Person.objects.all()
        serializer = PersonSerializer(persons, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, 200)

    def test_get_valid_single_person(self):
        response = self.client.get(f'{self.base_url}{self.person1.pk}/')
        person = Person.objects.get(pk=self.person1.pk)
        serializer = PersonSerializer(person)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, 200)

    def test_get_invalid_single_person(self):
        response = self.client.get(f'{self.base_url}1000/')
        self.assertEqual(response.status_code, 404)

    def test_create_valid_person(self):
        response = self.client.post(self.base_url, data=self.valid_payload)
        self.assertEqual(response.status_code, 201)

    def test_max_length_first_name(self):
        long_first_name = 'A' * 51
        payload = {
            'first_name': long_first_name,
            'last_name': 'Smith',
            'email': 'test.email@example.com'
        }
        response = self.client.post(self.base_url, data=payload)
        self.assertEqual(response.status_code, 400)

    def test_create_duplicate_email(self):
        response = self.client.post(self.base_url, data=self.valid_payload)
        response_duplicate = self.client.post(self.base_url, data=self.valid_payload)
        self.assertEqual(response_duplicate.status_code, 400)

    def test_fields_in_response(self):
        response = self.client.get(f'{self.base_url}{self.person1.pk}/')
        self.assertIn('first_name', response.data)
        self.assertIn('last_name', response.data)
        self.assertIn('email', response.data)

    def test_create_invalid_person(self):
        response = self.client.post(self.base_url, data=self.invalid_payload)
        self.assertEqual(response.status_code, 400)

    def test_valid_update_person(self):
        response = self.client.put(f'{self.base_url}{self.person1.pk}/', data=self.valid_payload)
        self.assertEqual(response.status_code, 200)

    def test_invalid_update_person(self):
        response = self.client.put(f'{self.base_url}{self.person1.pk}/', data=self.invalid_payload)
        self.assertEqual(response.status_code, 400)

    def test_delete_valid_person(self):
        response = self.client.delete(f'{self.base_url}{self.person1.pk}/')
        self.assertEqual(response.status_code, 204)

    def test_delete_invalid_person(self):
        response = self.client.delete(f'{self.base_url}1000/')
        self.assertEqual(response.status_code, 404)
