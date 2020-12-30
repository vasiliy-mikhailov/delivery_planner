from django.db import models

# Create your models here.

class ExternalTaskDAO(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    system = models.CharField(max_length=255)
    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE)

class AbilityEnumDAO(models.TextChoices):
    SYSTEM_ANALYSIS = 'SYSTEM_ANALYSIS'
    DEVELOPMENT = 'DEVELOPMENT'
    SYSTEM_TESTING = 'SYSTEM_TESTING'

class ExternalTaskEffortLeftDAO(models.Model):
    external_task = models.ForeignKey(ExternalTaskDAO, on_delete=models.CASCADE)
    ability = models.CharField(max_length=255, choices=AbilityEnumDAO.choices)
    hours = models.FloatField()
