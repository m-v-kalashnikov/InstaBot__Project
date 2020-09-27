from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    instagram_login = models.CharField(verbose_name=_('Instagram login'),
                                       max_length=30,
                                       blank=True,
                                       null=True,
                                       )
    instagram_password = models.CharField(verbose_name=_('Instagram password'),
                                          max_length=256,
                                          blank=True,
                                          null=True,
                                          )
