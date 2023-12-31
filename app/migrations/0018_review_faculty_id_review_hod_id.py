# Generated by Django 4.2 on 2023-05-21 23:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_complaint_resolved_alter_complaint_details'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='faculty_id',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.facultysignup'),
        ),
        migrations.AddField(
            model_name='review',
            name='hod_id',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.hodsignup'),
        ),
    ]
