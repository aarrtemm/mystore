# Generated by Django 4.2.1 on 2023-06-19 14:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0004_alter_order_basket_history"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="basket_history",
            field=models.JSONField(default=dict),
        ),
    ]
