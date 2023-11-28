from datetime import timedelta
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

from users.models import EmailVerification, User


class UserRegistrationViewTestCase(TestCase):

    def setUp(self) -> None:
        self.path = reverse('users:registration')
        self.test_user_data = {
            'first_name': 'Petr', 'last_name': 'Petrov',
            'username': 'PetrPetrov', 'email': 'petrpetrov@yandex.ru',
            'password1': '12345678pP', 'password2': '12345678pP',
        }
        self.username_test_user = self.test_user_data['username']

    def test_user_registration_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], "UPGrade PC - Регистрация")
        self.assertTemplateUsed(response, 'users/registration.html')

    def test_user_registration_post_success(self):
        self.assertFalse(User.objects.filter(username=self.username_test_user).exists())
        response = self.client.post(self.path, self.test_user_data)

        #  check creating of user
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'), fetch_redirect_response=False)
        self.assertTrue(User.objects.filter(username=self.username_test_user).exists())

        #  check creating of email verification
        email_verification = EmailVerification.objects.filter(user__username=self.username_test_user)
        self.assertTrue(email_verification.exists())
        self.assertEqual(
            email_verification.first().expiration.date(),
            (now() + timedelta(hours=48)).date()
        )

    def test_user_registration_post_error(self):
        User.objects.create(username=self.username_test_user)
        response = self.client.post(self.path, self.test_user_data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пользователь с таким именем уже существует.', html=True)
