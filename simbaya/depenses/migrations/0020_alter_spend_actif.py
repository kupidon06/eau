# Generated by Django 5.0 on 2024-01-03 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('depenses', '0019_alter_spend_actif_alter_spend_type_depense'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spend',
            name='actif',
            field=models.CharField(choices=[('Toyota', 'Toyota'), ('Citroen Jumper', 'CITROEN JUMPER'), ('autres', 'autres'), ('usine', 'usine'), ('Ford', 'FORD')], max_length=200, null=True),
        ),
    ]
