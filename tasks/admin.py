from asyncio import tasks
from django.contrib import admin
from .models import Module, Task, Answer


admin.site.register(Module)
admin.site.register(Task)
admin.site.register(Answer)
