# Generated by Django 4.1.5 on 2023-01-28 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schemas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schema',
            name='columns',
            field=models.ManyToManyField(blank=True, related_name='columns', to='schemas.schemacolumn'),
        ),
    ]
