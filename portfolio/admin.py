from django.contrib import admin
from .models import UserProfile, Project, ProjectView


admin.site.register(UserProfile)
admin.site.register(Project)
admin.site.register(ProjectView)