from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AuthCustomConfig(AppConfig):
    name = 'auth_custom'
    verbose_name = _('Доступ')
