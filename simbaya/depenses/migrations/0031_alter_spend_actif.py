# Generated by Django 5.0.1 on 2024-01-28 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('depenses', '0030_alter_spend_actif_alter_spend_type_depense'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spend',
            name='actif',
            field=models.CharField(choices=[('Citroen Jumper', 'CITROEN JUMPER'), ('Ford', 'FORD'), ('autres', 'autres'), ('Toyota', 'Toyota'), ('usine', 'usine')], max_length=200, null=True),
        ),
    ]