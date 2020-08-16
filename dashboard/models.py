from django.db import models

# Create your models here.
class UserSubscriber(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    created_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)