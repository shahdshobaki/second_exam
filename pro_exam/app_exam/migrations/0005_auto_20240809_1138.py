# Generated by Django 2.2.4 on 2024-08-09 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_exam', '0004_auto_20240809_1136'),
    ]

    operations = [
        migrations.RenameField(
            model_name='idea',
            old_name='user',
            new_name='uploaded_by',
        ),
        migrations.AlterField(
            model_name='idea',
            name='description',
            field=models.TextField(),
        ),
    ]
