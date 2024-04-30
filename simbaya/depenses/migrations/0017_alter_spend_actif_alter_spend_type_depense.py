# Generated by Django 5.0 on 2024-01-02 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('depenses', '0016_alter_spend_actif_alter_spend_detail_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spend',
            name='actif',
            field=models.CharField(choices=[('Ford', 'FORD'), ('Toyota', 'Toyota'), ('autres', 'autres'), ('usine', 'usine'), ('Citroen Jumper', 'CITROEN JUMPER')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='spend',
            name='type_depense',
            field=models.CharField(blank=True, choices=[('charge familliale', 'charge familliale'), ('charge ordinaire', 'charge ordinaire')], max_length=200, null=True),
        ),
    ]
