from django.db import models

# Create your models here.
class ValidationModel(models.Model):
    email = models.EmailField(unique=True)
    validation = models.CharField(max_length=4)
    create_time = models.DateTimeField(auto_now_add=True)

