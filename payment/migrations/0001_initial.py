# Generated by Django 5.1.6 on 2025-02-24 19:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ShippingAddress",
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
                ("full_name", models.CharField(max_length=250)),
                ("email", models.CharField(max_length=250)),
                ("address1", models.CharField(max_length=250)),
                ("address2", models.CharField(max_length=250)),
                ("city", models.CharField(max_length=250)),
                ("state", models.CharField(blank=True, max_length=250, null=True)),
                ("zipcode", models.CharField(max_length=250)),
                ("country", models.CharField(blank=True, max_length=250, null=True)),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
