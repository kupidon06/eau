# Generated by Django 5.0 on 2024-01-01 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personnel', '0026_alter_pers_poste_alter_pers_situation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pers',
            name='poste',
            field=models.CharField(choices=[('Vendeur', 'vendeur'), ('Ouvrier', 'Ouvrier'), ('Chauffeur', 'chauffeur')], max_length=200, null=True),
        ),
    ]