from django.shortcuts import render


def schema_list(request):
    return render(request, "schema_list.html")


def create_schema(request):
    return render(request, "create_schema.html")


def schema_detail(request, id):
    return render(request, "detail.html", {"obj_id": id})


def edit_schema(request, id):
    return render(request, "create_schema.html", {"obj_id": id})
