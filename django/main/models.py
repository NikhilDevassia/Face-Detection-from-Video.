from django.db import models

# Create your models here.
class Video(models.Model):
    caption = models.CharField(max_length=100, unique=True)
    Video = models.FileField(upload_to='video/%y')
    def __str__(self):
        return self.caption

class Output(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media/output', null=True)

class Model_weight(models.Model):
    caption = models.CharField(max_length=100)
    model = models.FileField(upload_to='media/Model', null=True)
    def __str__(self):
        return self.caption

