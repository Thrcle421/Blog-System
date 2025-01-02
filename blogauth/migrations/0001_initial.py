# Generated by Django 5.1.4 on 2024-12-31 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ValidationModel",
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
                ("email", models.EmailField(max_length=254)),
                ("validation", models.CharField(max_length=4)),
                ("create_time", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]