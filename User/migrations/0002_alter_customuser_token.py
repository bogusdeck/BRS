# Generated by Django 5.1 on 2024-08-08 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='token',
            field=models.CharField(blank=True, max_length=36, null=True),
        ),
    ]
