from rest_framework import serializers
from django.db import models
from .models import ToDo, LogInModel, SignUpModel


#Serializers

class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignUpModel
        fields = ["username", "email", "password"]

class LogInSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogInModel
        fields = ["username", "password"]

class ToDoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDo
        fields = ["name", "description", "datetime", "completed", "emailSent", "owner"]