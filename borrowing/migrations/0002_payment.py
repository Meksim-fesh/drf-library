# Generated by Django 5.1.2 on 2024-11-05 14:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("borrowing", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("Pending", "Pending"), ("Paid", "Paid")], max_length=7
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[("Payment", "Payment"), ("Fine", "Fine")], max_length=7
                    ),
                ),
                ("session_url", models.URLField()),
                ("session_id", models.PositiveIntegerField()),
                ("money_to_pay", models.DecimalField(decimal_places=2, max_digits=6)),
                (
                    "borrowing",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="borrowing.borrowing",
                    ),
                ),
            ],
        ),
    ]
