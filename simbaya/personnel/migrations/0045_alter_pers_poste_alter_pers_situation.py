# Generated by Django 5.0.1 on 2024-04-27 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personnel', '0044_alter_pers_poste'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pers',
            name='poste',
            field=models.CharField(choices=[('Ouvrier', 'Ouvrier'), ('Vendeur', 'vendeur'), ('Chauffeur', 'chauffeur')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='pers',
            name='situation',
            field=models.CharField(choices=[('Celibataire', 'celibataire'), ('Marié', 'Marié')], max_length=500, null=True),
        ),
    ]
