# Generated by Django 5.0.1 on 2024-01-28 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personnel', '0040_alter_pers_poste_alter_pers_regime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pers',
            name='poste',
            field=models.CharField(choices=[('Vendeur', 'vendeur'), ('Ouvrier', 'Ouvrier'), ('Chauffeur', 'chauffeur')], max_length=200, null=True),
        ),
    ]
