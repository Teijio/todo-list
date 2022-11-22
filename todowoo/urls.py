"""todowoo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from todo import views

urlpatterns = [
    path("admin/", admin.site.urls),

    # auth
    path("signup/", views.signup_user, name="signup_user"),
    path("login/", views.login_user, name="login_user"),
    path("logout/", views.logout_user, name="logout_user"),

    # Todo
    path("", views.home, name="home"),
    path("create/", views.create_todo, name="create_todo"),
    path("current/", views.current_todo, name="current_todo"),
    path("completed/", views.completed_todo, name="completed_todo"),
    path("todo/<int:todo_pk>/", views.view_todo, name="view_todo"),
    path("todo/<int:todo_pk>/complete/", views.complete_todo, name="complete_todo"),
    path("todo/<int:todo_pk>/delete/", views.delete_todo, name="delete_todo"),

]
