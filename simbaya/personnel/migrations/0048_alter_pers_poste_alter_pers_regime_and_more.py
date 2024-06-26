# Generated by Django 5.0.1 on 2024-04-30 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personnel', '0047_alter_pers_poste_alter_pers_regime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pers',
            name='poste',
            field=models.CharField(choices=[('Vendeur', 'vendeur'), ('Ouvrier', 'Ouvrier'), ('Chauffeur', 'chauffeur')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='pers',
            name='regime',
            field=models.CharField(choices=[('Salarié', 'salarié'), ('Pourcentage', 'Pourcentage')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='pers',
            name='situation',
            field=models.CharField(choices=[('Celibataire', 'celibataire'), ('Marié', 'Marié')], max_length=500, null=True),
        ),
    ]
