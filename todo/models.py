from django.db import models
from django.contrib.auth.models import User


class ToDo(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="Название",
    )
    memo = models.TextField(
        blank=True,
        verbose_name="Описание",
    )
    date_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации",
    )
    date_complete = models.DateTimeField(
        null=True, blank=True,
    )
    important = models.BooleanField(
        default=False,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.title