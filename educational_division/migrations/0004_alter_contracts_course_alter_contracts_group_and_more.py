# Generated by Django 4.2 on 2023-05-21 10:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('educational_division', '0003_alter_user_professor_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contracts',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='educational_division.courses', verbose_name='Предмет'),
        ),
        migrations.AlterField(
            model_name='contracts',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='educational_division.group', verbose_name='Группа'),
        ),
        migrations.AlterField(
            model_name='contracts',
            name='professor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='educational_division.professors', verbose_name='Профессор'),
        ),
        migrations.AlterField(
            model_name='specialitycourses',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='educational_division.courses', verbose_name='Дисциплина'),
        ),
        migrations.AlterField(
            model_name='specialitycourses',
            name='speciality',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='educational_division.specialities', verbose_name='Специальность'),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Professor'), (2, 'Worker'), (3, 'Admin')], null=True),
        ),
    ]
