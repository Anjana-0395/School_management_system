# Generated by Django 5.1.4 on 2024-12-19 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school_app', '0003_alter_student_division'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='staff_name',
            field=models.CharField(default='anna', max_length=100),
            preserve_default=False,
        ),
    ]
