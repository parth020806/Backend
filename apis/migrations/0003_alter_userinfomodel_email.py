# Generated by Django 4.1 on 2023-07-22 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0002_alter_userinfomodel_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfomodel',
            name='email',
            field=models.CharField(max_length=100),
        ),
    ]
