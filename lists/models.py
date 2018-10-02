from django.db import models

class Item(models.Model):
    text = models.TextField(default='')
# Create your models here test- resume at "A New Field Means a New Migration".
