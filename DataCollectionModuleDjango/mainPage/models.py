from django.db import models
from django.contrib.auth.models import User


# Структура и органы упрвавления образовательной организацией
class Struct(models.Model):
    name = models.CharField(max_length=100, blank=True, null=False)
    fio = models.CharField(max_length=100, blank=True)
    post = models.CharField(max_length=200, blank=True)
    addressStr = models.CharField(max_length=200, blank=True)
    site = models.CharField(max_length=60, blank=True)
    email = models.CharField(max_length=60, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=True)
    divisionClauseDocLinkFileNames = models.JSONField(null=True, blank=True)


# Основные сведения
class Common(models.Model):
    name = models.CharField(max_length=100, blank=True, null=False)
    regDate = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=False)
    workTime = models.TextField(blank=True, null=False)
    telephone = models.CharField(max_length=100, blank=True, null=False)
    fax = models.CharField(max_length=100, blank=True, null=False)
    email = models.CharField(max_length=100, blank=True, null=False)
    additionalInformation = models.TextField(blank=True, null=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=True)


# Основные сведения -> Информация об учередителях
class UchredLaw(models.Model):
    nameUchred = models.CharField(max_length=100, blank=True, null=False)
    fullnameUchred = models.CharField(max_length=100, blank=True, null=False)
    addressUchred = models.CharField(max_length=300, blank=True, null=False)
    telUchred = models.CharField(max_length=100, blank=True, null=False)
    mailUchred = models.CharField(max_length=100, blank=True, null=False)
    websiteUchred = models.CharField(max_length=100, blank=True, null=False)
    isIndividual = models.BooleanField(null=False, default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=True)


# Основные сведения -> Информация о филиалах
class FilInfo(models.Model):
    nameFil = models.CharField(max_length=100, blank=True, null=False)
    addressFil = models.CharField(max_length=100, blank=True, null=False)
    workTimeFil = models.CharField(max_length=300, blank=True, null=False)
    telephoneFil = models.CharField(max_length=100, blank=True, null=False)
    emailFil = models.CharField(max_length=100, blank=True, null=False)
    websiteFil = models.CharField(max_length=100, blank=True, null=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=True)


# Основные сведения -> Информация о представительствах
class RepInfo(models.Model):
    nameRep = models.CharField(max_length=101, blank=True, null=False)
    addressRep = models.CharField(max_length=100, blank=True, null=False)
    workTimeRep = models.CharField(max_length=300, blank=True, null=False)
    telephoneRep = models.CharField(max_length=100, blank=True, null=False)
    emailRep = models.CharField(max_length=100, blank=True, null=False)
    websiteRep = models.CharField(max_length=100, blank=True, null=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=True)
