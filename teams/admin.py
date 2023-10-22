from django.contrib import admin
from .models import Person, Team


class PersonAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'full_name']
    search_fields = ['first_name', 'last_name']
    list_filter = ['first_name', 'last_name']


class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']
    list_filter = ['name']
    filter_horizontal = ('members',)


admin.site.register(Person, PersonAdmin)
admin.site.register(Team, TeamAdmin)
