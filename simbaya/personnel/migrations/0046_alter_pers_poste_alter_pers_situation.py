# Generated by Django 5.0.1 on 2024-04-30 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personnel', '0045_alter_pers_poste_alter_pers_situation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pers',
            name='poste',
            field=models.CharField(choices=[('Ouvrier', 'Ouvrier'), ('Chauffeur', 'chauffeur'), ('Vendeur', 'vendeur')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='pers',
            name='situation',
            field=models.CharField(choices=[('Marié', 'Marié'), ('Celibataire', 'celibataire')], max_length=500, null=True),
        ),
    ]
