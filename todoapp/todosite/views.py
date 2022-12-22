from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login, logout
import requests


# Create your views here.


@api_view(["GET", "POST"])
def index(request):
    if request.method == "POST":
        todoID = request.data["todoid"]
        res = requests.post("http://localhost:8000/api/todofinish", data={"owner": request.user.id, "todoID": todoID})
        if res.status_code == 200:
            return redirect("index")
        else:
            return redirect("index")
    else:
        if request.user.is_authenticated:
            res = requests.post("http://localhost:8000/api/todos", data={"owner": request.user.id})
            return render(request, "index.html", {"message": res.json()["message"]})
        else:
            return render(request, "index.html", {"message": "Welcome Strangerrr! Login or Signup"})

@api_view(["GET", "POST"])
def loginReq(request):
    if request.method == "POST":
        username = request.data["username"]
        password = request.data["password"]
        res = requests.post("http://localhost:8000/api/login", data={"username": username, "password": password})
        if res.status_code == 200:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("index")
        else:
            return render(request, "login.html", {"message": res.json()["message"]})
    else:
        if request.user.is_authenticated:
            return redirect("index")
        else:
            return render(request, "login.html")

@api_view(["GET", "POST"])
def signupReq(request):
    if request.method == "POST":
        username = request.data["username"]
        email = request.data["email"]
        password = request.data["password"]
        res = requests.post("http://localhost:8000/api/signup", data={"username": username, "email": email, "password": password})
        if res.status_code == 200:
            return render(request, "signup.html", {"message": res.json()["message"]})
        else:
            return render(request, "signup.html", {"message": res.json()["message"]})
    else:
        if request.user.is_authenticated:
            return redirect("index")
        else:
            return render(request, "signup.html")


def logoutReq(request):
    logout(request)
    return redirect("login")


@api_view(["GET", "POST"])
def newTodoReq(request):
    if request.method == "POST":
        name = request.data["name"]
        description = request.data["description"]
        datetime = request.data["datetime"].replace("T", " | ")
        if len(description) <= 100:
            res = requests.post("http://localhost:8000/api/newtodo", data={"name": name, "description": description, "datetime": datetime, "completed": False, "emailSent": False, "owner": request.user.id})
            if res.status_code == 200:
                return redirect("index")
            else:
                return render(request, "newtodo.html", {"message": res.json()["message"]})
        else:
            return render(request, "newtodo.html", {"message": "Description must less than 100!"})
    else:
        if request.user.is_authenticated:
            return render(request, "newtodo.html")
        else:
            return redirect("index")