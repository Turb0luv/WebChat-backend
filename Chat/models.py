from django.contrib.auth.models import User
from django.db import models


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='user_id')
    user_name = models.CharField(max_length=255, null=False)
    content = models.TextField(null=False)
    created_at = models.DateTimeField(null=True)
