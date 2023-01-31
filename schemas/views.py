from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView


class MyLoginView(LoginView):
    redirect_authenticated_user = True


@login_required
def index(request):
    return redirect("schemas:list")


@login_required
def schema_list(request):
    return render(request, "schema_list.html")


@login_required
def create_schema(request):
    return render(request, "create_schema.html")


@login_required
def schema_detail(request, id):
    return render(request, "detail.html", {"obj_id": id})


@login_required
def edit_schema(request, id):
    return render(request, "create_schema.html", {"obj_id": id})
