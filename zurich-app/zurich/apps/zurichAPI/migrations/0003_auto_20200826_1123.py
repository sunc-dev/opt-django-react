# Generated by Django 3.1 on 2020-08-26 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zurichAPI', '0002_modelconstraints_algorithm'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelconstraints',
            name='algorithm',
            field=models.CharField(choices=[('ilp', 'ILP'), ('Other', 'Other')], default='ILP', max_length=9),
        ),
    ]