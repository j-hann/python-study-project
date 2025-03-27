from django.contrib import admin

from jobs.models import JobPost, Favorite

admin.site.register(JobPost)
admin.site.register(Favorite)