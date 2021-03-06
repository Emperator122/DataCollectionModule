from django.db import models
from django.contrib.auth.models import User


class Struct(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    fio = models.CharField(max_length=100, blank=True)
    post = models.CharField(max_length=200, blank=True)
    addressStr = models.CharField(max_length=200, blank=True)
    site = models.CharField(max_length=60, blank=True)
    email = models.CharField(max_length=60, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=True)
    divisionClauseDocLinkFileNames = models.JSONField(null=True, blank=True)
