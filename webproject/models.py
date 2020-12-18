from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

class Question(models.Model):
    class Meta:
        ordering = ['id']

    text = models.CharField(max_length=200, verbose_name='вопрос')
    answer = models.CharField(max_length=50, verbose_name='ответ')
    points = models.IntegerField(
        default=1,
        verbose_name='балл за правильный ответ'
    )
    test = models.ForeignKey('Test', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.answer = self.answer.strip().lower()
        super().save(*args, **kwargs)


class Test(models.Model):
    name = models.CharField(max_length=50, verbose_name='название теста')
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    date_time_created = models.DateTimeField(auto_now_add=True)


class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name='название курса')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    models.UniqueConstraint(
        fields=['name', 'author'],
        name='unique_name_per_user'
    )

    date_time_created = models.DateTimeField(auto_now_add=True)


class QuestionAnswer(models.Model):
    question_text = models.CharField(max_length=200, verbose_name='вопрос')
    correct_answer = models.CharField(
        max_length=50,
        verbose_name='верный ответ'
    )
    given_answer = models.CharField(max_length=50, verbose_name='ответ')
    total_points = models.IntegerField(
        verbose_name='балл за правильный ответ'
    )
    scored_points = models.IntegerField(
        default=0,
        verbose_name='полученный балл',
        validators=[MinValueValidator(0), ]
    )
    testResult = models.ForeignKey('TestResult', on_delete=models.CASCADE)

    def save(self, **kwargs):
        self.given_answer = self.given_answer.strip().lower()
        if self.given_answer == self.correct_answer:
            self.scored_points = self.total_points
        else:
            self.scored_points = 0
        super().save(**kwargs)


class TestResult(models.Model):
    isActive = models.BooleanField(default=True)
    taken_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    date_time_created = models.DateTimeField(auto_now_add=True)
