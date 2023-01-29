from rest_framework import serializers
from ..models import Schema, SchemaColumn, Dataset
from .utils import format_date


class SchemaColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchemaColumn
        fields = "__all__"
        extra_kwargs = {
            "int_from": {"required": False},
            "int_to": {"required": False},
        }


class SchemaSerializer(serializers.ModelSerializer):
    columns = SchemaColumnSerializer(many=True, required=False)

    class Meta:
        model = Schema
        fields = "__all__"
        extra_kwargs = {
            "columns": {"required": False}
        }

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.columns.set(self.context['columns'])
        instance.user = self.context['request'].user
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.columns.set(self.context['columns'])
        return instance


class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = "__all__"

    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        repr_['created_at'] = format_date(instance.created_at)

        return repr_

