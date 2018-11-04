from django.db import models

class ApplicationForm(models.Model):
    pass


class ApplicationFormItem(models.Model):
    text = models.TextField(default='')
    applicationform = models.TextField(default='')
    #applicationform = models.ForeignKey(ApplicationForm, default=None)
# Create your models here test- resume at "A New Field Means a New Migration".
