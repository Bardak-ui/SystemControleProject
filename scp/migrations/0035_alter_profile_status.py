# Generated by Django 5.1.4 on 2025-01-02 01:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scp', '0034_alter_profile_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='status',
            field=models.CharField(choices=[('Заблокирован', 'Banned'), ('Не заблокирован', 'Not banned')], default='Not banned', max_length=50),
        ),
    ]
