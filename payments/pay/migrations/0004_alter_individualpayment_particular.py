# Generated by Django 4.0 on 2022-02-01 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pay', '0003_remove_profile_is_preschool'),
    ]

    operations = [
        migrations.AlterField(
            model_name='individualpayment',
            name='particular',
            field=models.CharField(choices=[('Tuition', 'Tuition'), ('Groceries', 'Groceries'), ('Development', 'Development'), ('Online Learning', 'Online Learning'), ('Bus Levy', 'Bus Levy'), ('Registration Fee', 'Registration Fee')], max_length=100),
        ),
    ]
