from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Stuff(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title


    class Meta:
        order_with_respect_to = 'user'