from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verification_code = models.CharField(max_length=6, default="", blank=True)
    avatar = models.ImageField(upload_to='avatars/', default="avatars/default.png")

    def __str__(self):
        return self.user.username

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=75)
    description = models.TextField()
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
    
class ProjectView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=None)