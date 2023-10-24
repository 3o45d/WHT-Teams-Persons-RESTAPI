from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='First Name')
    last_name = models.CharField(max_length=50, verbose_name='Last Name')
    email = models.EmailField(unique=True, verbose_name='Email')

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Name')
    description = models.TextField(blank=True, verbose_name='Description')
    members = models.ManyToManyField(Person, blank=True, related_name='teams', verbose_name='Members')

    def __str__(self):
        return self.name
