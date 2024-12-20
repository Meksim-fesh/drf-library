# Generated by Django 5.1.2 on 2024-11-06 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("borrowing", "0002_payment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payment",
            name="session_id",
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name="payment",
            name="session_url",
            field=models.URLField(max_length=516),
        ),
    ]
