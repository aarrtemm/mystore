# Generated by Django 4.2.1 on 2023-06-19 11:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0007_alter_basket_managers"),
        ("orders", "0003_order_initiator"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="basket_history",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="products.product"
            ),
        ),
    ]
