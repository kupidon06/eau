# Generated by Django 5.0.1 on 2024-04-27 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personnel', '0043_alter_pers_situation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pers',
            name='poste',
            field=models.CharField(choices=[('Vendeur', 'vendeur'), ('Chauffeur', 'chauffeur'), ('Ouvrier', 'Ouvrier')], max_length=200, null=True),
        ),
    ]
