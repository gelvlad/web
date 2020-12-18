from django.contrib import admin

from . import models

admin.site.register(models.Course)
admin.site.register(models.Test)
admin.site.register(models.Question)
admin.site.register(models.TestResult)
admin.site.register(models.QuestionAnswer)
