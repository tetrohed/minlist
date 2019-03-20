from django.db import models

class Item(models.Model):
    list = models.ForeignKey("List", on_delete=models.CASCADE)
    text = models.TextField(default=None)
    
class List(models.Model):
    pass
    