import json
import contextlib
import pandas as pd
from django.core.files.base import ContentFile

from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveAPIView,
)
from rest_framework.response import Response

from .serializers import SchemaSerializer, SchemaColumnSerializer, DatasetSerializer
from ..models import Schema, SchemaColumn, Dataset
from .utils import fill_list
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthor


class SchemaList(ListAPIView):
    serializer_class = SchemaSerializer
    queryset = Schema.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(user=self.request.user)


class SchemaDetailAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = SchemaSerializer
    queryset = Schema.objects.all()
    lookup_field = "id"
    permission_classes = (IsAuthenticated, IsAuthor)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        with contextlib.suppress(Exception):
            context.update({"columns": self.column_id_list})
        return context

    def put(self, request, *args, **kwargs):
        serializer = SchemaColumnSerializer(
            data=json.loads(request.data["columns"]), many=True
        )
        serializer.is_valid(raise_exception=True)
        columns = serializer.save()
        column_id_list = []
        for column in columns:
            column_id_list.append(column.id)
        self.column_id_list = column_id_list
        return super().put(request, *args, **kwargs)


class SchemaCreateAPI(CreateAPIView):
    serializer_class = SchemaSerializer
    queryset = Schema.objects.all()
    permission_classes = (IsAuthenticated, IsAuthor)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"columns": self.column_id_list})
        return context

    def post(self, request, *args, **kwargs):
        serializer = SchemaColumnSerializer(
            data=json.loads(request.data["columns"]), many=True
        )
        serializer.is_valid(raise_exception=True)
        columns = serializer.save()
        column_id_list = []
        for column in columns:
            column_id_list.append(column.id)
        self.column_id_list = column_id_list
        return super().post(request, *args, **kwargs)


class SchemaColumnCreateAPI(CreateAPIView):
    serializer_class = SchemaColumnSerializer
    queryset = SchemaColumn.objects.all()
    permission_classes = (IsAuthenticated,)


class GenerateCsvAPI(RetrieveAPIView):
    queryset = Schema.objects.all()
    lookup_field = "id"
    permission_classes = (IsAuthenticated, IsAuthor)

    def get(self, request, *args, **kwargs):
        schema = self.get_object()
        rows = request.GET.get("rows")

        columns = schema.columns.all().order_by("-order")
        column_name_list = columns.values_list("name", flat=True)

        row_list = fill_list(columns, int(rows))

        dataset = pd.DataFrame(row_list, columns=column_name_list)
        temp_file = ContentFile(
            dataset.to_csv(
                index=None,
                header=True,
                sep=schema.column_sep,
                lineterminator="\n",
                quotechar=schema.string_char,
                quoting=1,
            )
        )
        obj = Dataset.objects.create(schema=schema)
        obj.file.save("output.csv", temp_file)
        return Response()


class DatasetListAPI(RetrieveAPIView):
    queryset = Schema.objects.all()
    lookup_field = "id"
    permission_classes = (IsAuthenticated, IsAuthor)

    def get(self, request, *args, **kwargs):
        datasets = Dataset.objects.filter(schema=self.get_object()).order_by("-id")
        serializer = DatasetSerializer(datasets, many=True)
        return Response(serializer.data)
