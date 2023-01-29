from django.urls import path
from .views import schema_list, create_schema, schema_detail, edit_schema

app_name = "schemas"

urlpatterns = [
    path("list/", schema_list, name="list"),
    path("create/", create_schema, name="create"),
    path("detail/<id>/", schema_detail, name="detail"),
    path("edit/<id>/", edit_schema, name="edit"),
]
