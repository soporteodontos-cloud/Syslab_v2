from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
MY_AREAS = [
    ('CAD CAM', 'CAD CAM'),
    ('METAL', 'METAL'),
    ('METALOCERAMICA', 'METALOCERAMICA'),
    ('CEROMERO', 'CEROMERO'),
    ('ACRILICO', 'ACRILICO'),
    ('PLACAS', 'PLACAS'),
    ('MAQUILLAJE', 'MAQUILLAJE'),
]

class CustomUsers(AbstractUser):
    areas = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.username
