import random
import string
from datetime import datetime

from auth_custom.models import User
from django.test import override_settings
from django.urls import reverse
from insta_bot_api.settings import EMAIL_FILE_PATH
from rest_framework import status
from rest_framework.test import APITestCase


def get_random_digit(ex):
    letters_and_digits = string.ascii_letters + string.digits
    letters_and_digits = letters_and_digits.replace(ex, '')
    result_str = random.choice(letters_and_digits)
    return result_str


def get_random_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str


class CustomAuth(APITestCase):

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.filebased.EmailBackend')
    def test_registration_success(self):
        """
        Success registration
        :return:
        """
        url = reverse('rest_register')
        data = {
            'email': 'test@test.com',
            'password1': 'Password_super321',
            'password2': 'Password_super321'
        }
        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_registration_fail_password(self):
        """
        Fail registration because not matching passwords
        :return:
        """
        url = reverse('rest_register')
        data = {
            'email': 'test@test.com',
            'password1': get_random_string(16),
            'password2': get_random_string(17)
        }
        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_fail_user_exists(self):
        """
        Fail registration because user exists
        :return:
        """
        u = User.objects.create_user(username='test', email='test@test.com', password='Password_super321')
        u.save()
        url = reverse('rest_register')
        data = {
            'email': 'test@test.com',
            'password1': 'Password_super321',
            'password2': 'Password_super321'
        }
        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.filebased.EmailBackend')
    def test_verification_success(self):
        """
        Success verification
        :return:
        """
        url = reverse('rest_register')
        data = {
            'email': 'test@test.com',
            'password1': 'Password_super321',
            'password2': 'Password_super321'
        }
        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        r = '{}{}{}-{}{}{}*.log'.format(datetime.now().year,
                                        '{:02d}'.format(datetime.now().month),
                                        '{:02d}'.format(datetime.now().day),
                                        '{:02d}'.format(datetime.now().hour),
                                        '{:02d}'.format(datetime.now().minute),
                                        '{:02d}'.format(datetime.now().second))
        file = ''
        for name in EMAIL_FILE_PATH.glob(r):
            file = name

        f = open(file=file, encoding='utf-8', mode='r')
        key = f.readlines()[15].split()[-1].split('/')[-1]
        url = reverse('rest_verify_email')
        data = {
            'key': key
        }
        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.filebased.EmailBackend')
    def test_verification_fail(self):
        """
        Fail verification
        :return:
        """
        url = reverse('rest_register')
        data = {
            'email': 'test@test.com',
            'password1': 'Password_super321',
            'password2': 'Password_super321'
        }
        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        r = '{}{}{}-{}{}{}*.log'.format(datetime.now().year,
                                        '{:02d}'.format(datetime.now().month),
                                        '{:02d}'.format(datetime.now().day),
                                        '{:02d}'.format(datetime.now().hour),
                                        '{:02d}'.format(datetime.now().minute),
                                        '{:02d}'.format(datetime.now().second))
        file = ''
        for name in EMAIL_FILE_PATH.glob(r):
            file = name

        f = open(file=file, encoding='utf-8', mode='r')
        token = f.readlines()[15].split()[-1].split('/')[-1]
        digit = token[-1]
        new_digit = get_random_digit(digit)
        pre_key = token
        key = pre_key.replace(digit, new_digit)
        url = reverse('rest_verify_email')
        data = {
            'key': key
        }
        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
