# Generated by Django 4.1.2 on 2022-10-19 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("intersect", "0011_statsh_remove_cucoo_statsh_data"),
    ]

    operations = [
        migrations.CreateModel(
            name="Stash",
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
                ("data", models.CharField(max_length=128)),
            ],
        ),
        migrations.DeleteModel(name="Statsh",),
        migrations.RenameField(
            model_name="cucoo", old_name="table_data", new_name="data",
        ),
        migrations.RenameField(
            model_name="cucoo", old_name="hash_idx", new_name="idx",
        ),
    ]
