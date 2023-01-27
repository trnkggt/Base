from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Task(models.Model):
    content = models.TextField(max_length=250, null=False)
    title = models.CharField(max_length=50, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    complete = models.BooleanField(default=False)