from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Aihealue, Ketju, Vastaus, Notes, Tags

User = get_user_model()


# Tests for the Forum models
class ForumModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='valter',
            email='valter@example.com',
            password='test1234'
        )
        self.aihealue = Aihealue.objects.create(header="Django stuff")
        self.ketju = Ketju.objects.create(
            header="How to use Django?",
            content="Can someone help me?",
            author=self.user,
            aihealue=self.aihealue
        )
        self.vastaus = Vastaus.objects.create(
            content="Sure! Here's how...",
            replier=self.user,
            ketju=self.ketju
        )

    def test_ketju_creation(self):
        self.assertEqual(self.ketju.header, "How to use Django?")
        self.assertEqual(self.ketju.author.username, "valter")
        self.assertEqual(self.ketju.aihealue.header, "Django stuff")

    def test_vastaus_related_to_ketju(self):
        self.assertEqual(self.vastaus.ketju, self.ketju)
        self.assertEqual(self.vastaus.replier, self.user)


# Tests for Notes model
class NotesModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='valter',
            email='valter@example.com',
            password='test1234'
        )
        self.note = Notes.objects.create(
            owner=self.user,
            header="React tips",
            content="Use components wisely.",
            tags=Tags.REACT
        )

    def test_note_creation_and_str(self):
        self.assertEqual(str(self.note), "React tips")
        self.assertEqual(self.note.tags, Tags.REACT)
        self.assertEqual(self.note.owner.username, "valter")


from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse


# API Tests for Ketju (Thread)
class KetjuAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="valter_api",
            email="valter_api@example.com",
            password="testpass"
        )
        self.aihealue = Aihealue.objects.create(header="Testing area")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_ketju(self):
        url = reverse('ketju-list')
        data = {
            'header': 'Test from API',
            'content': 'Creating a Ketju via API test.',
            'author': self.user.id,
            'aihealue': self.aihealue.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['header'], 'Test from API')

    def test_list_ketjut(self):
        Ketju.objects.create(
            header='Listable Thread',
            content='Testing GET',
            author=self.user,
            aihealue=self.aihealue
        )
        url = reverse('ketju-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(k['header'] == 'Listable Thread' for k in response.data))


# API Tests for Vastaus (Reply)
class VastausAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="replyuser",
            email="reply@example.com",
            password="testpass"
        )
        self.aihealue = Aihealue.objects.create(header="Replies Area")
        self.ketju = Ketju.objects.create(
            header="Thread for reply",
            content="Let's reply here",
            author=self.user,
            aihealue=self.aihealue
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_vastaus(self):
        url = reverse('vastaus-list')
        data = {
            'content': "Here's my reply via API",
            'replier': self.user.id,
            'ketju': self.ketju.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['content'], "Here's my reply via API")


# Unauthenticated access test
class UnauthenticatedAccessTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="unauth_user",
            email="unauth@example.com",
            password="testpass"
        )
        self.aihealue = Aihealue.objects.create(header="Restricted")
        self.ketju = Ketju.objects.create(
            header="Auth test thread",
            content="Content",
            author=self.user,
            aihealue=self.aihealue
        )

    def test_unauthenticated_vastaus_post(self):
        url = reverse('vastaus-list')
        data = {
            'content': "Trying to reply without login",
            'replier': self.user.id,
            'ketju': self.ketju.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 401)


# Notes API test: user-specific notes
class NotesAPITests(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1",
            email="user1@example.com",
            password="pass1"
        )
        self.user2 = User.objects.create_user(
            username="user2",
            email="user2@example.com",
            password="pass2"
        )

        Notes.objects.create(
            owner=self.user1,
            header="Note from user1",
            content="Private",
            tags=Tags.PYTHON
        )
        Notes.objects.create(
            owner=self.user2,
            header="Note from user2",
            content="Hidden",
            tags=Tags.REACT
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user1)

    def test_notes_are_user_specific(self):
        url = reverse('notes-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(all(note['owner'] == self.user1.id for note in response.data))
        self.assertFalse(any(note['owner'] == self.user2.id for note in response.data))
