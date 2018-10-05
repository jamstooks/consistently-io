# Generated by Django 2.1.1 on 2018-10-05 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('integrations', '0008_auto_20181003_1657'),
    ]

    operations = [
        migrations.AddField(
            model_name='travis',
            name='build_time',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='integrationstatus',
            name='status',
            field=models.CharField(choices=[('waiting', 'Waiting...'), ('passed', 'Passed'), ('failed', 'Failed')], default='waiting', max_length=20),
        ),
    ]
