# Generated by Django 3.1 on 2020-08-27 19:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('zurichAPI', '0012_modelconstraints_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelconstraints',
            name='request_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zurichAPI.requests'),
        ),
    ]