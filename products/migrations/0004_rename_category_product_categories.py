# Generated by Django 4.2.1 on 2023-06-08 10:24

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0003_remove_product_category_product_category"),
    ]

    operations = [
        migrations.RenameField(
            model_name="product",
            old_name="category",
            new_name="categories",
        ),
    ]