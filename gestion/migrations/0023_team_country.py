# Generated by Django 4.2.4 on 2023-08-18 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gestion", "0022_alter_messagerie_trading_number"),
    ]

    operations = [
        migrations.AddField(
            model_name="team",
            name="country",
            field=models.CharField(default=None, max_length=100, null=True),
        ),
    ]
