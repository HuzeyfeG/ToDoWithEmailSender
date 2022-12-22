from django.urls import path
from . import views

urlpatterns = [
    path("login", views.loginReq, name="login"),
    path("signup", views.signupReq, name="signup"),
    path("logout", views.logoutReq, name="logout"),
    path("index", views.index, name="index"),
    path("", views.index, name="index"),
    path("newtodo", views.newTodoReq, name="newtodo")
]