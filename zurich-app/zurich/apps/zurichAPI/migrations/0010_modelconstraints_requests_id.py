# Generated by Django 3.1 on 2020-08-27 19:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('zurichAPI', '0009_auto_20200827_1304'),
    ]

    operations = [
        migrations.AddField(
            model_name='modelconstraints',
            name='requests_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='zurichAPI.algorithms'),
            preserve_default=False,
        ),
    ]
