# Generated by Django 5.1.4 on 2024-12-30 14:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scp', '0021_rename_user_profile_puser_alter_project_status_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(choices=[('Выполнено', 'Complited'), ('В разработке', 'In Development'), ('Ожидает', 'Waiting')], default='Waiting', max_length=50),
        ),
        migrations.AlterField(
            model_name='task',
            name='assignee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='t_assignee', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('Выполнено', 'Complited'), ('В разработке', 'In Development'), ('Ожидает', 'Waiting')], default='Waiting', max_length=50),
        ),
    ]
