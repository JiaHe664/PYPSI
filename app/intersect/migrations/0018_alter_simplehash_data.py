# Generated by Django 4.1.2 on 2022-10-21 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("intersect", "0017_alter_simplehash_h1_alter_simplehash_h2_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="simplehash",
            name="data",
            field=models.CharField(max_length=255),
        ),
    ]