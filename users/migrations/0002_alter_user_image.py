# Generated by Django 4.2.1 on 2023-06-08 12:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="image_user"),
        ),
    ]
