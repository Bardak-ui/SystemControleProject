# Generated by Django 5.1.4 on 2024-12-29 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scp', '0008_alter_project_status_alter_task_priority_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(choices=[('Complited', 'Выполнено'), ('In Development', 'В разработке'), ('Waiting', 'Ожидает')], default='Waiting', max_length=50),
        ),
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.CharField(choices=[('Low', 'Низкий'), ('Cредний', 'Average'), ('Высокий', 'High'), ('Не указан', 'Not specified')], default='Not specified', max_length=50),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('Complited', 'Выполнено'), ('In Development', 'В разработке'), ('Waiting', 'Ожидает')], default='Waiting', max_length=50),
        ),
    ]
