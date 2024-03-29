# Generated by Django 4.2 on 2023-06-01 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('educational_division', '0007_alter_contracts_beginning_date_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='acts',
            options={'verbose_name': 'Акт выполненных работ', 'verbose_name_plural': 'Акты выполненных работ'},
        ),
        migrations.AlterModelOptions(
            name='contracts',
            options={'verbose_name': 'Контракт', 'verbose_name_plural': 'Контракты'},
        ),
        migrations.AlterModelOptions(
            name='courses',
            options={'verbose_name': 'Дисциплина', 'verbose_name_plural': 'Дисциплины'},
        ),
        migrations.AlterModelOptions(
            name='group',
            options={'verbose_name': 'Группа', 'verbose_name_plural': 'Группы'},
        ),
        migrations.AlterModelOptions(
            name='professors',
            options={'verbose_name': 'Преподаватель', 'verbose_name_plural': 'Преподаватели'},
        ),
        migrations.AlterModelOptions(
            name='specialities',
            options={'verbose_name': 'Специальность', 'verbose_name_plural': 'Специальности'},
        ),
        migrations.AlterModelOptions(
            name='specialitycourses',
            options={'verbose_name': 'Курс Специальности', 'verbose_name_plural': 'Курсы специальностей'},
        ),
        migrations.AddField(
            model_name='professors',
            name='academic_degree',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Нет'), (2, 'Кандидат наук'), (3, 'Доктор наук')], null=True),
        ),
        migrations.AddField(
            model_name='professors',
            name='academic_title',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Ассистент'), (2, 'Преподаватель'), (3, 'Старший преподаватель'), (4, 'Доцент'), (5, 'Профессор')], null=True),
        ),
    ]
