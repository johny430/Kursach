from django.contrib.auth.models import AbstractUser
from django.db import models


class Courses(models.Model):
    name = models.CharField("Название специальности", max_length=100)
    description = models.CharField("Описание специальности", max_length=100)
    hours = models.IntegerField('Количество студентов')

    def __str__(self):
        return f"Название: {self.name} Описание:{self.description} Часы: {self.hours}"

    class Meta:
        verbose_name = 'Дисциплина'
        verbose_name_plural = 'Дисциплины'


class Specialities(models.Model):
    name = models.CharField("Название специальности", max_length=100)
    description = models.CharField("Описание специальности", max_length=100)
    code = models.IntegerField('Номер специальности')
    speciality_courses = models.ManyToManyField(Courses, verbose_name="Курсы специальнсти",
                                                related_name="speciality_course", through='SpecialityCourses')

    def __str__(self):
        return f'Название: {self.name} Описание: {self.description} Код: {self.code}'

    class Meta:
        verbose_name = 'Специальность'
        verbose_name_plural = 'Специальности'


class SpecialityCourses(models.Model):
    speciality = models.ForeignKey(Specialities, on_delete=models.CASCADE, verbose_name='Специальность')
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, verbose_name='Дисциплина')

    def __str__(self):
        return f'{self.speciality.name} - {self.course.name}'

    class Meta:
        verbose_name = 'Курс Специальности'
        verbose_name_plural = 'Курсы специальностей'


class Group(models.Model):
    number = models.IntegerField("Номер группы")
    student_count = models.IntegerField('Количество студентов группы')
    specialty = models.ForeignKey(Specialities, on_delete=models.CASCADE)

    def __str__(self):
        return f'Номер:{self.number} Количество студентов: {self.student_count} Специальность: {self.specialty.name}'

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class Professors(models.Model):
    last_name = models.CharField("Фамилия", max_length=100)
    first_name = models.CharField("Имя", max_length=100)
    surname = models.CharField('Отчетсво', max_length=100)
    email = models.CharField('Адрес электронной почты', max_length=100)
    phone_number = models.CharField("Номер телефона", max_length=100)
    courses = models.ManyToManyField(Courses, through="Contracts")

    Academic_Degree = (
        (1, 'Нет'),
        (2, 'Кандидат наук'),
        (3, 'Доктор наук'),
    )

    Academic_Title = (
        (1, 'Ассистент'),
        (2, 'Преподаватель'),
        (3, 'Старший преподаватель'), (4, 'Доцент'),
        (5, 'Профессор'),

    )
    academic_degree = models.PositiveSmallIntegerField(choices=Academic_Degree, blank=True, null=True)
    academic_title = models.PositiveSmallIntegerField(choices=Academic_Title, blank=True, null=True)

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.surname}'

    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'


class Contracts(models.Model):
    professor = models.ForeignKey(Professors, on_delete=models.CASCADE, verbose_name='Преподаватель')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='Группа')
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, verbose_name='Предмет')
    type = models.CharField('Тип проводимых занятий', max_length=100)
    hours = models.IntegerField('Количество проводимых часов')
    beginning_date = models.DateField('Дата начала контракта', default="2023-02-08")
    end_date = models.DateField('Дата окончания контракта', default="2023-06-08")

    def __str__(self):
        return f"Преподаватель: {self.professor.last_name + ' ' + self.professor.first_name + ' ' + self.professor.surname} " \
               f"Предмет: {self.course.name} " \
               f"Часы: {self.hours} " \
               f"Тип занятий: {self.type}"

    class Meta:
        verbose_name = 'Контракт'
        verbose_name_plural = 'Контракты'


class Acts(models.Model):
    contract = models.ForeignKey(Contracts, verbose_name='Контракт', on_delete=models.CASCADE)
    worked_hours = models.IntegerField('Количество проводимых часов')
    beginning_date = models.DateField('Дата начала периода')
    end_date = models.DateField('Дата окончания периода')
    creation_date = models.DateField('Дата создания акта')

    class Meta:
        verbose_name = 'Акт выполненных работ'
        verbose_name_plural = 'Акты выполненных работ'

    def __str__(self):
        return f'{self.contract} {self.worked_hours} {self.beginning_date} {self.end_date}'


class User(AbstractUser):
    Professor = 1
    Worker = 2
    Admin = 3

    ROLE_CHOICES = (
        (Professor, 'Professor'),
        (Worker, 'Worker'),
        (Admin, 'Admin'),
    )
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)
    professor_data = models.ForeignKey(Professors, on_delete=models.DO_NOTHING, blank=True, null=True)

    @property
    def __str__(self):
        return f'{self.username} {self.role} Администратор: {str(self.is_superuser)}'
