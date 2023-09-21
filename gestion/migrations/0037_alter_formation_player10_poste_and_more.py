# Generated by Django 4.2.4 on 2023-09-20 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gestion", "0036_alter_formation_player10_poste_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="formation",
            name="player10_poste",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Remplacent", "Rp"),
                    ("Buteur", "BU"),
                    ("Ailier_droit", "AD"),
                    ("Aillier_gauche", "AG"),
                    ("Milieu_Offensif", "MO"),
                    ("Milieu_Centrale", "MC"),
                    ("Milieu_defensif", "MDC"),
                    ("Defenseur_Gauche", "DG"),
                    ("Defenseur_Droit", "DD"),
                    ("Defenseur_Centrale", "DC"),
                    ("Goalkipper", "GK"),
                ],
                default="Rp",
                max_length=20,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="formation",
            name="player11_poste",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Remplacent", "Rp"),
                    ("Buteur", "BU"),
                    ("Ailier_droit", "AD"),
                    ("Aillier_gauche", "AG"),
                    ("Milieu_Offensif", "MO"),
                    ("Milieu_Centrale", "MC"),
                    ("Milieu_defensif", "MDC"),
                    ("Defenseur_Gauche", "DG"),
                    ("Defenseur_Droit", "DD"),
                    ("Defenseur_Centrale", "DC"),
                    ("Goalkipper", "GK"),
                ],
                default="Rp",
                max_length=20,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="formation",
            name="player1_poste",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Remplacent", "Rp"),
                    ("Buteur", "BU"),
                    ("Ailier_droit", "AD"),
                    ("Aillier_gauche", "AG"),
                    ("Milieu_Offensif", "MO"),
                    ("Milieu_Centrale", "MC"),
                    ("Milieu_defensif", "MDC"),
                    ("Defenseur_Gauche", "DG"),
                    ("Defenseur_Droit", "DD"),
                    ("Defenseur_Centrale", "DC"),
                    ("Goalkipper", "GK"),
                ],
                default="Rp",
                max_length=20,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="formation",
            name="player2_poste",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Remplacent", "Rp"),
                    ("Buteur", "BU"),
                    ("Ailier_droit", "AD"),
                    ("Aillier_gauche", "AG"),
                    ("Milieu_Offensif", "MO"),
                    ("Milieu_Centrale", "MC"),
                    ("Milieu_defensif", "MDC"),
                    ("Defenseur_Gauche", "DG"),
                    ("Defenseur_Droit", "DD"),
                    ("Defenseur_Centrale", "DC"),
                    ("Goalkipper", "GK"),
                ],
                default="Rp",
                max_length=20,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="formation",
            name="player3_poste",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Remplacent", "Rp"),
                    ("Buteur", "BU"),
                    ("Ailier_droit", "AD"),
                    ("Aillier_gauche", "AG"),
                    ("Milieu_Offensif", "MO"),
                    ("Milieu_Centrale", "MC"),
                    ("Milieu_defensif", "MDC"),
                    ("Defenseur_Gauche", "DG"),
                    ("Defenseur_Droit", "DD"),
                    ("Defenseur_Centrale", "DC"),
                    ("Goalkipper", "GK"),
                ],
                default="Rp",
                max_length=20,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="formation",
            name="player4_poste",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Remplacent", "Rp"),
                    ("Buteur", "BU"),
                    ("Ailier_droit", "AD"),
                    ("Aillier_gauche", "AG"),
                    ("Milieu_Offensif", "MO"),
                    ("Milieu_Centrale", "MC"),
                    ("Milieu_defensif", "MDC"),
                    ("Defenseur_Gauche", "DG"),
                    ("Defenseur_Droit", "DD"),
                    ("Defenseur_Centrale", "DC"),
                    ("Goalkipper", "GK"),
                ],
                default="Rp",
                max_length=20,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="formation",
            name="player5_poste",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Remplacent", "Rp"),
                    ("Buteur", "BU"),
                    ("Ailier_droit", "AD"),
                    ("Aillier_gauche", "AG"),
                    ("Milieu_Offensif", "MO"),
                    ("Milieu_Centrale", "MC"),
                    ("Milieu_defensif", "MDC"),
                    ("Defenseur_Gauche", "DG"),
                    ("Defenseur_Droit", "DD"),
                    ("Defenseur_Centrale", "DC"),
                    ("Goalkipper", "GK"),
                ],
                default="Rp",
                max_length=20,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="formation",
            name="player6_poste",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Remplacent", "Rp"),
                    ("Buteur", "BU"),
                    ("Ailier_droit", "AD"),
                    ("Aillier_gauche", "AG"),
                    ("Milieu_Offensif", "MO"),
                    ("Milieu_Centrale", "MC"),
                    ("Milieu_defensif", "MDC"),
                    ("Defenseur_Gauche", "DG"),
                    ("Defenseur_Droit", "DD"),
                    ("Defenseur_Centrale", "DC"),
                    ("Goalkipper", "GK"),
                ],
                default="Rp",
                max_length=20,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="formation",
            name="player7_poste",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Remplacent", "Rp"),
                    ("Buteur", "BU"),
                    ("Ailier_droit", "AD"),
                    ("Aillier_gauche", "AG"),
                    ("Milieu_Offensif", "MO"),
                    ("Milieu_Centrale", "MC"),
                    ("Milieu_defensif", "MDC"),
                    ("Defenseur_Gauche", "DG"),
                    ("Defenseur_Droit", "DD"),
                    ("Defenseur_Centrale", "DC"),
                    ("Goalkipper", "GK"),
                ],
                default="Rp",
                max_length=20,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="formation",
            name="player8_poste",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Remplacent", "Rp"),
                    ("Buteur", "BU"),
                    ("Ailier_droit", "AD"),
                    ("Aillier_gauche", "AG"),
                    ("Milieu_Offensif", "MO"),
                    ("Milieu_Centrale", "MC"),
                    ("Milieu_defensif", "MDC"),
                    ("Defenseur_Gauche", "DG"),
                    ("Defenseur_Droit", "DD"),
                    ("Defenseur_Centrale", "DC"),
                    ("Goalkipper", "GK"),
                ],
                default="Rp",
                max_length=20,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="formation",
            name="player9_poste",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Remplacent", "Rp"),
                    ("Buteur", "BU"),
                    ("Ailier_droit", "AD"),
                    ("Aillier_gauche", "AG"),
                    ("Milieu_Offensif", "MO"),
                    ("Milieu_Centrale", "MC"),
                    ("Milieu_defensif", "MDC"),
                    ("Defenseur_Gauche", "DG"),
                    ("Defenseur_Droit", "DD"),
                    ("Defenseur_Centrale", "DC"),
                    ("Goalkipper", "GK"),
                ],
                default="Rp",
                max_length=20,
                null=True,
            ),
        ),
    ]
