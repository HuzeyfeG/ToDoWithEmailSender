from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignUpSerializer, LogInSerializer, ToDoSerializer
from .models import ToDo
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.


@api_view(["POST"])
def signupRes(request):
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        if User.objects.filter(username=serializer.data["username"]).exists():
            return Response({"message": "Username is taken!"}, status=status.HTTP_401_UNAUTHORIZED)
        elif User.objects.filter(email=serializer.data["email"]).exists():
            return Response({"message": "Email is taken!"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            user = User.objects.create_user(username=serializer.data["username"], email=serializer.data["email"], password=serializer.data["password"])
            user.save()
            return Response({"message": "Succesfully signed up!"}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Validation Error!"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def loginRes(request):
    serializer = LogInSerializer(data=request.data)
    if serializer.is_valid():
        user = authenticate(request, username=serializer.data["username"], password=serializer.data["password"])
        if user is not None:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({"message": "Username or password not correct!"}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({"message": "Validation Error!"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def newtodoRes(request):
    ownerEmail = User.objects.get(id=request.data["owner"]).email
    serializer = ToDoSerializer(data=request.data)
    if serializer.is_valid():
        ToDo.objects.create(name=serializer.data["name"], description=serializer.data["description"], datetime=serializer.data["datetime"], completed=serializer.data["completed"], emailSent=serializer.data["emailSent"], owner=serializer.data["owner"])
        send_mail("ToDo Created", "Name: " + serializer.data["name"] + "\n" + "Description: " + serializer.data["description"] + "\n" + "Dead Line: " + serializer.data["datetime"], settings.EMAIL_HOST_USER,[ownerEmail])
        return Response({"message": "ToDo Created!"}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Validation Error!"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def todosRes(request):
    todos = ToDo.objects.values().filter(owner=request.data["owner"])
    return Response({"message": todos}, status=status.HTTP_200_OK)

@api_view(["POST"])
def todoFinish(request):
    ownerEmail = User.objects.get(id=request.data["owner"]).email
    todo = ToDo.objects.get(owner=request.data["owner"], id=request.data["todoID"])
    todo.completed = True
    todo.save()
    send_mail("ToDo Completed!", todo.name + "\n" + todo.description + "\n\n" + "Congratulations!", settings.EMAIL_HOST_USER,[ownerEmail])
    return Response(status=status.HTTP_200_OK)

