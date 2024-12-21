# Generated by Django 5.1.4 on 2024-12-19 10:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school_app', '0005_alter_staff_department'),
    ]

    operations = [
        migrations.CreateModel(
            name='Librarian',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('librarian_name', models.CharField(max_length=100)),
                ('joining_date', models.DateField()),
                ('library_section', models.CharField(max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='librarian_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]