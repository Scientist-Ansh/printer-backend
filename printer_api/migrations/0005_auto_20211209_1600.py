# Generated by Django 3.2.9 on 2021-12-09 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('printer_api', '0004_user_pages_printed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='department',
            name='pages_remaining',
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]