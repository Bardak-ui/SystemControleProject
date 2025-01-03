# Generated by Django 5.1.4 on 2024-12-30 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scp', '0025_alter_profile_role_alter_project_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='status',
            field=models.CharField(choices=[('Baned', 'Заблокирован'), ('Not baned', 'Не заблокирован')], default='Not baned', max_length=50),
        ),
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(choices=[('Выполнено', 'Complited'), ('In Development', 'В разработке'), ('Ожидает', 'Waiting')], default='Waiting', max_length=50),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('Выполнено', 'Complited'), ('In Development', 'В разработке'), ('Ожидает', 'Waiting')], default='Waiting', max_length=50),
        ),
    ]
