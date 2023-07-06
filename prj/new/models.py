from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Rating(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='todos', default=1)
    username = models.CharField(max_length=20)
    rating = models.IntegerField()

    def __str__(self):
        return self.username
    