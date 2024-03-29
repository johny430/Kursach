# Generated by Django 4.2 on 2023-05-21 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('educational_division', '0006_alter_contracts_beginning_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contracts',
            name='beginning_date',
            field=models.DateField(default='2023-02-08', verbose_name='Дата начала контракта'),
        ),
        migrations.AlterField(
            model_name='contracts',
            name='end_date',
            field=models.DateField(default='2023-06-08', verbose_name='Дата окончания контракта'),
        ),
    ]
