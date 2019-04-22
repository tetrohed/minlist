from django.db import models
from django.urls import reverse


class Item(models.Model):
    list = models.ForeignKey("List", on_delete=models.CASCADE)
    text = models.TextField(default=None)

    class Meta:
        unique_together = ('list', 'text')

class List(models.Model):

    def get_absolute_url(self):
        return reverse('lists:view_list', args=[self.id])
