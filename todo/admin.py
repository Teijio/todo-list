from django.contrib import admin
from .models import ToDo


class ToDoAdmin(admin.ModelAdmin):
    readonly_fields = ("date_created",)


admin.site.register(ToDo, ToDoAdmin)
