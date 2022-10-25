from django.db import models

# Create your models here.
class SimpleHash(models.Model):
    data = models.CharField(max_length=255)
    h1 = models.CharField(max_length=300)
    h2 = models.CharField(max_length=300)
    h3 = models.CharField(max_length=300)
    
class ClientTable(models.Model):
    date = models.CharField(max_length=32)
    name = models.CharField(max_length=64)
    records = models.IntegerField()
    task_id = models.CharField(max_length=128)

    
class ClientTask(models.Model):
    date = models.CharField(max_length=32)
    label = models.CharField(max_length=128)
    table = models.CharField(max_length=32)
    host = models.CharField(max_length=32)
    port = models.IntegerField()
    results = models.IntegerField()
    runtime = models.IntegerField()
    status = models.IntegerField()
    
    
class ClientResult(models.Model):
    date = models.CharField(max_length=32)
    name = models.CharField(max_length=64)
    records = models.IntegerField()
    task_id = models.CharField(max_length=128)