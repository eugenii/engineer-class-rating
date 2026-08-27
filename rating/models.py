from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    CLASS_CHOICES = [
        (5, '5 класс'),
        (6, '6 класс'),
        (7, '7 класс'),
        (8, '8 класс'),
    ]
    
    nickname = models.CharField("Никнейм для рейтинга", max_length=50, unique=True, null=True, blank=True)
    school_class = models.IntegerField("Класс", choices=CLASS_CHOICES, null=True, blank=True)
    is_teacher = models.BooleanField("Статус учителя", default=False)

    def __str__(self):
        if self.is_teacher:
            return f"Учитель: {self.last_name} {self.first_name}"
        return f"{self.last_name} {self.first_name} ({self.nickname or 'Нет ника'})"


class Subject(models.Model):
    name = models.CharField("Название предмета", max_length=100, unique=True)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    # Добавили related_name='lessons' для связи предмета с уроками
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='lessons', verbose_name="Предмет")
    date = models.DateField("Дата проведения")
    topic = models.CharField("Тема урока", max_length=255)
    max_score = models.PositiveIntegerField("Максимальный балл", default=10)

    def __str__(self):
        return f"{self.date} | {self.subject.name} | {self.topic}"


class Grade(models.Model):
    # Добавили related_name='grades' для ученика и урока
    student = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='grades', 
        verbose_name="Ученик", 
        limit_choices_to={'is_teacher': False}
    )
    lesson = models.ForeignKey(
        Lesson, 
        on_delete=models.CASCADE, 
        related_name='grades', 
        verbose_name="Урок"
    )
    score = models.PositiveIntegerField("Полученный балл")

    class Meta:
        unique_together = ('student', 'lesson')
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"

    def __str__(self):
        return f"{self.student.nickname or self.student.username} -> {self.lesson.topic}: {self.score}"
