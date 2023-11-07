# Generated by Django 4.2.4 on 2023-11-01 15:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gestion", "0042_player_injured_player_suspended"),
    ]

    operations = [
        migrations.AddField(
            model_name="player",
            name="forme",
            field=models.PositiveSmallIntegerField(
                blank=True,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(99),
                ],
            ),
        ),
    ]
