# Generated by Django 4.0.2 on 2022-04-06 06:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0007_alter_balance_data_total_amount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trans_data',
            old_name='owner',
            new_name='user',
        ),
    ]
