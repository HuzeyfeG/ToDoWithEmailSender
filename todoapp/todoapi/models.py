from django.db import models

# Create your models here.


class ToDo(models.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=100)
    datetime = models.CharField(max_length=32)
    completed = models.BooleanField()
    emailSent = models.BooleanField()
    owner = models.IntegerField()

class SignUpModel(models.Model):
    username = models.CharField(max_length=32)
    email = models.CharField(max_length=32)
    password = models.CharField(max_length=32)

class LogInModel(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)