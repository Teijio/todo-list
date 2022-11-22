from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import ToDoForm
from .models import ToDo
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, "todo/home.html")


def signup_user(request):
    if request.method == "GET":
        return render(
            request, "todo/signup_user.html", {"form": UserCreationForm()}
        )
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    request.POST["username"],
                    password=request.POST["password1"],
                )
                user.save()
                login(request, user)
                return redirect("current_todo")
            except IntegrityError:
                return render(
                    request,
                    "todo/signup_user.html",
                    {
                        "form": UserCreationForm(),
                        "error": "That username has already been taken",
                    },
                )
        else:
            return render(
                request,
                "todo/signup_user.html",
                {
                    "form": UserCreationForm(),
                    "error": "Passwords did not match",
                },
            )


def login_user(request):
    if request.method == "GET":
        return render(
            request, "todo/login_user.html", {"form": AuthenticationForm()}
        )
    else:
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is None:
            return render(
                request,
                "todo/login_user.html",
                {
                    "form": AuthenticationForm(),
                    "error": "Username name or password did not match",
                },
            )
        else:
            login(request, user)
            return redirect("current_todo")


@login_required
def logout_user(request):
    if request.method == "POST":
        logout(request)
        return redirect("home")


@login_required
def create_todo(request):
    if request.method == "GET":
        return render(request, "todo/create_todo.html", {"form": ToDoForm()})
    else:
        try:
            form = ToDoForm(request.POST)
            new_todo = form.save(commit=False)
            new_todo.user = request.user
            new_todo.save()
            return redirect("current_todo")
        except ValueError:
            return render(
                request,
                "todo/create_todo.html",
                {"form": ToDoForm(), "error": "Bad data input, try again"},
            )


@login_required
def current_todo(request):
    todo_list = ToDo.objects.filter(
        user=request.user,
        date_complete__isnull=True,
    )
    return render(request, "todo/current_todo.html", {"todo_list": todo_list})


@login_required
def completed_todo(request):
    todo_list = ToDo.objects.filter(
        user=request.user,
        date_complete__isnull=False,
    ).order_by("-date_complete")
    return render(
        request, "todo/completed_todo.html", {"todo_list": todo_list}
    )


@login_required
def view_todo(request, todo_pk):
    todo = get_object_or_404(ToDo, pk=todo_pk, user=request.user)
    if request.method == "GET":
        form = ToDoForm(instance=todo)
        return render(
            request, "todo/view_todo.html", {"todo": todo, "form": form}
        )
    else:
        try:
            form = ToDoForm(request.POST, instance=todo)
            form.save()
            return redirect("current_todo")
        except ValueError:
            return render(
                request,
                "todo/view_todo.html",
                {"todo": todo, "form": form, "error": "Bad info"},
            )


@login_required
def complete_todo(request, todo_pk):
    todo = get_object_or_404(ToDo, pk=todo_pk, user=request.user)
    if request.method == "POST":
        todo.date_complete = timezone.now()
        todo.save()
        return redirect("current_todo")


@login_required
def delete_todo(request, todo_pk):
    todo = get_object_or_404(ToDo, pk=todo_pk, user=request.user)
    if request.method == "POST":
        todo.delete()
        return redirect("current_todo")
