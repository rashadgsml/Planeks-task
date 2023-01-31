from django.db import models
from django.conf import settings


COLUMN_TYPES = (
    ("Full name", "Full name"),
    ("Job", "Job"),
    ("Email", "Email"),
    ("Domain name", "Domain name"),
    ("Phone number", "Phone number"),
    ("Text", "Text"),
    ("Integer", "Integer"),
    ("Address", "Address"),
    ("Date", "Date"),
)


class Schema(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True
    )
    title = models.CharField(max_length=100)
    column_sep = models.CharField(max_length=1)
    string_char = models.CharField(max_length=1)

    columns = models.ManyToManyField("SchemaColumn", blank=True, related_name="columns")

    modified_at = models.DateField(auto_now=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Schema"
        verbose_name_plural = "Schemas"


class SchemaColumn(models.Model):
    name = models.CharField(max_length=100)
    column_type = models.CharField(choices=COLUMN_TYPES, max_length=100)
    order = models.IntegerField(blank=True, null=True)

    # if clumn_type is integer
    int_from = models.IntegerField(blank=True, null=True)
    int_to = models.IntegerField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Schema Column"
        verbose_name_plural = "Schema Columns"
        ordering = ("order",)


class Dataset(models.Model):
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE)
    file = models.FileField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.schema.title

    class Meta:
        verbose_name = "Dataset"
        verbose_name_plural = "Datasets"
