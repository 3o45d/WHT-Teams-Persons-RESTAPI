from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='Ім\'я')
    last_name = models.CharField(max_length=50, verbose_name='Прізвище')
    email = models.EmailField(unique=True, verbose_name='Електронна пошта')

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Назва команди')
    description = models.TextField(blank=True, verbose_name='Опис команди')
    members = models.ManyToManyField(Person, blank=True, related_name='teams')

    def __str__(self):
        return self.name
