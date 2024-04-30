import uuid
from decimal import Decimal

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserAccountManager(BaseUserManager):

    def create_user(self, phone, password, **extra_fields):
        if not phone:
            raise ValueError('Le numero de telephone doit être fourni')
        phone = phone
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password, **extra_fields):
        return self.create_user(phone, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(('nom'), max_length=255,null=True)
    phone = models.CharField(('téléphone'), max_length=15, unique=True)
    objects = UserAccountManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name']


    class Meta:
        verbose_name = ('compte utilisateur')
        verbose_name_plural = ('comptes utilisateurs')

    def __str__(self):
        return self.phone