from django.contrib import admin

from .models import Vacancy, Office, WorkDirection

# Register your models here.
admin.site.register(Vacancy)
admin.site.register(Office)
admin.site.register(WorkDirection)