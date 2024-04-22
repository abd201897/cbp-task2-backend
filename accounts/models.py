from django.contrib.auth.models import AbstractUser
from django.db import models
from utils.models import Roles


# Create your models here.


class User(AbstractUser):
    role = models.ForeignKey(Roles, default=None, null=True, on_delete=models.SET_NULL)
    date_of_birth = models.BigIntegerField(default=None, null=True, verbose_name='Date Of Birth')
    address = models.TextField(default='', null=True, verbose_name='Address')
    city = models.CharField(max_length=100, default='', null=True, verbose_name='City')
    country = models.CharField(max_length=100, default='', null=True, verbose_name='Country')
    image = models.TextField(default='', verbose_name='Profile Picture URL')

    def __str__(self):
        return f"{self.get_full_name()} [Username: {self.username}] | [Role: {self.role}]"

    class Meta:
        db_table = "User"

