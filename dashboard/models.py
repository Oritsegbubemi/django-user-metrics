from django.db import models

# Create your models here.
class UserSubscriber(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True,blank=False,default='')
    created_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    def __str__(self):
	    return '%s' % (self.email)