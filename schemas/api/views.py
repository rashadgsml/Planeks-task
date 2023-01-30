import json
from faker import Faker
import pandas as pd
from django.core.files.base import ContentFile

from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.response import Response

from .serializers import SchemaSerializer, SchemaColumnSerializer, DatasetSerializer
from ..models import Schema, SchemaColumn, Dataset
from .utils import fill_list
from .permissions import IsAuthor


class SchemaList(ListAPIView):
    serializer_class = SchemaSerializer
    queryset = Schema.objects.all()

    def get_queryset(self, *args, **kwargs):
        return Schema.objects.filter(user=self.request.user)


class SchemaDetailAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = SchemaSerializer
    queryset = Schema.objects.all()
    lookup_field = "id"

    def get_serializer_context(self):
        context = super().get_serializer_context()
        try:
            context.update({"columns": self.column_id_list})
        except:
            pass
        return context
    
    def get_object(self):
        obj = super().get_object()
        return obj

    def put(self, request, *args, **kwargs):
        serializer = SchemaColumnSerializer(data=json.loads(request.data["columns"]), many=True)
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

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"columns": self.column_id_list})
        return context

    def post(self, request, *args, **kwargs):
        serializer = SchemaColumnSerializer(data=json.loads(request.data["columns"]), many=True)
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


class GenerateCsvAPI(RetrieveAPIView):
    queryset = Schema.objects.all()
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        fake = Faker()
        schema = self.get_object()
        rows = request.GET.get("rows")

        columns = schema.columns.all().order_by("-order")
        column_name_list = columns.values_list("name", flat=True)

        row_list = fill_list(columns, int(rows), fake)

        dataset = pd.DataFrame(row_list, columns=column_name_list)
        temp_file = ContentFile(dataset.to_csv(index=None, header=True, 
                                            sep=schema.column_sep, lineterminator='\n',
                                            quotechar='"', quoting=1))
        obj = Dataset.objects.create(
            schema=schema
        )
        obj.file.save('output.csv', temp_file)
        return Response()


class DatasetListAPI(RetrieveAPIView):
    queryset = Schema.objects.all()
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        datasets = Dataset.objects.filter(schema=self.get_object()).order_by("-id")
        serializer = DatasetSerializer(datasets, many=True)
        return Response(serializer.data)
