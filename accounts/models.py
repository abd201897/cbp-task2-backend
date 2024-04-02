from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.


class User(AbstractUser):

    def __str__(self):
        return f"{self.get_full_name()} [Username: {self.username}] | [Role: {self.role}]"

    class Meta:
        db_table = "User"
