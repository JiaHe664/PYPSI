# Generated by Django 4.1.2 on 2022-10-19 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("intersect", "00010_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Statsh",
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
                ("statsh_data", models.CharField(max_length=128)),
            ],
        ),
        migrations.RemoveField(model_name="cucoo", name="statsh_data",),
    ]