# Generated by Django 4.0.2 on 2022-04-03 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0006_alter_key_pair1_private_key_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='balance_data',
            name='total_amount',
            field=models.FloatField(default=0, max_length=15),
        ),
    ]
