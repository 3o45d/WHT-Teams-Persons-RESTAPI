from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='Ім\'я')
    last_name = models.CharField(max_length=50, verbose_name='Прізвище')

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class TeamMember(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name='Людина')
    position = models.CharField(max_length=100, verbose_name='Позиція')

    def __str__(self):
        return f"[{self.position}] {self.person.full_name}"


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Назва команди')
    description = models.TextField(blank=True, verbose_name='Опис команди')
    members = models.ManyToManyField(TeamMember, related_name='team_members')

    def __str__(self):
        return self.name
