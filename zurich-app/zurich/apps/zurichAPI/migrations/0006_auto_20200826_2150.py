# Generated by Django 3.1 on 2020-08-27 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zurichAPI', '0005_auto_20200826_1534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelconstraints',
            name='area',
            field=models.DecimalField(decimal_places=2, max_digits=12),
        ),
        migrations.AlterField(
            model_name='modelconstraints',
            name='budget',
            field=models.DecimalField(decimal_places=2, max_digits=12),
        ),
        migrations.AlterField(
            model_name='modelconstraints',
            name='endangerment',
            field=models.DecimalField(decimal_places=2, max_digits=12),
        ),
        migrations.AlterField(
            model_name='modelconstraints',
            name='proximity',
            field=models.DecimalField(decimal_places=2, max_digits=12),
        ),
        migrations.AlterField(
            model_name='modelconstraints',
            name='trees',
            field=models.DecimalField(decimal_places=2, max_digits=12),
        ),
        migrations.AlterField(
            model_name='modelconstraints',
            name='water',
            field=models.DecimalField(decimal_places=2, max_digits=12),
        ),
    ]