from appengine_django.models import BaseModel
from django.db import models

class User(BaseModel):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)

class Repository(BaseModel):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User)
