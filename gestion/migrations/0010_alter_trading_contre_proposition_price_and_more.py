# Generated by Django 4.1.7 on 2023-08-15 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gestion", "0009_alter_trading_contre_proposition_price_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="trading",
            name="contre_proposition_price",
            field=models.DecimalField(
                decimal_places=2, default=None, max_digits=10, null=True
            ),
        ),
        migrations.AlterField(
            model_name="trading",
            name="sell_price",
            field=models.DecimalField(
                decimal_places=2, default=None, max_digits=10, null=True
            ),
        ),
    ]
