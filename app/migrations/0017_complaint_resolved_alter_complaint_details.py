# Generated by Django 4.2 on 2023-05-21 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_alter_complaint_details'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint',
            name='Resolved',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='complaint',
            name='details',
            field=models.CharField(max_length=250),
        ),
    ]