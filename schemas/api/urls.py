from django.urls import path
from .views import SchemaList, SchemaCreateAPI, SchemaColumnCreateAPI, SchemaDetailAPI, GenerateCsvAPI, DatasetListAPI

app_name = "schemas-api"

urlpatterns = [
    path("list/", SchemaList.as_view(), name="list"),
    path("dataset-list/<id>/", DatasetListAPI.as_view(), name="dataset-list"),
    path("create/", SchemaCreateAPI.as_view(), name="create"),
    path("detail/<id>/", SchemaDetailAPI.as_view(), name="detail"),
    path("create-column/", SchemaColumnCreateAPI.as_view(), name="create-column"),
    path("generate-csv/<id>/", GenerateCsvAPI.as_view(), name="generate-csv"),
]
