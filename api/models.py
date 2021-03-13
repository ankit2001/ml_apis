from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from MediaScanner import settings
from jsonfield import JSONField
import json

class DeveloperManager(BaseUserManager):
    def create_user(self, name, email, password, organisation):
        if not email:
            raise ValueError("Please provide us your email")
        email = self.normalize_email(email)
        developer = self.model(email = email, name = name, organisation = organisation)
        developer.set_password(password)
        developer.save(using = self._db)
        return developer
    
    def create_superuser(self, name, email, password, organisation):
        creator = self.create_user(name, email, password, organisation)
        creator.is_superuser = True
        creator.is_staff = True
        creator.save(using = self._db)
        return creator

class DeveloperProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique = True, max_length = 255, default = "scanner@email.com")
    name = models.CharField(max_length = 20, default = "Media Scanner")
    organisation = models.CharField(max_length = 20, default = "Media Scanner")
    is_staff = models.BooleanField(default = False)

    objects = DeveloperManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'organisation']

    def __str__(self):
        return self.email

class PCOSModel(models.Model):
    objects = DeveloperManager()
    developer_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
    )
    timing = models.DateTimeField(auto_now_add = True)
    # age, Chin, Cheeks, Lips, Breast, Arms, Thigh, Exercise, Eat, PCOS, BMI, Weight, Period, Concieve, Skin, Hairthin, Patch, Tired, Mood, Can, City
    age = models.IntegerField(blank=True, null=True)
    Chin = models.IntegerField(blank=True, null=True)
    Cheeks = models.IntegerField(blank=True, null=True)
    Lips = models.IntegerField(blank=True, null=True)
    Breast = models.IntegerField(blank=True, null=True)
    Arms = models.IntegerField(blank=True, null=True)
    Thigh = models.IntegerField(blank=True, null=True)
    Exercise = models.IntegerField(blank=True, null=True)
    Eat = models.IntegerField(blank=True, null=True)
    PCOS = models.CharField(max_length=100)
    BMI = models.CharField(max_length=100)
    Weight = models.CharField(max_length=100)
    Period = models.CharField(max_length=100)
    Concieve = models.CharField(max_length=100)
    Skin = models.CharField(max_length=100)
    Hairthin = models.CharField(max_length=100)
    Patch = models.CharField(max_length=100)
    Tired = models.CharField(max_length=100)
    Mood = models.CharField(max_length=100)
    Can = models.CharField(max_length=100)
    City = models.CharField(max_length=100)
    
    report = JSONField({})
    def __str__(self):
        return self.timing

class CervicalModel(models.Model):
    objects = DeveloperManager()
    developer_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
    )
    timing = models.DateTimeField(auto_now_add = True)
    # [age, no_of_sexual_parteners, age_of_first_intercourse, no_of_pregnancies, smokes, smokes_packs, hormonal_contraceptives, intra_uterine, STDS, any_std, condylomatosis, cervical_condylomatosis, vaginal, vulvo_perineal, syphilis, pelvic, genital, molluscum, AIDS, HIV, hepatitis, HPV, diagnosis_std, cancer, neoplasis, diagnosis_hpv]
    age = models.FloatField(blank=True, null=True)
    no_of_sexual_parteners = models.FloatField(blank=True, null=True)
    age_of_first_intercourse = models.FloatField(blank=True, null=True)
    no_of_pregnancies = models.FloatField(blank=True, null=True)
    smokes = models.FloatField(blank=True, null=True)
    smokes_packs = models.FloatField(blank=True, null=True)
    hormonal_contraceptives = models.FloatField(blank=True, null=True)
    intra_uterine = models.FloatField(blank=True, null=True)
    STDS = models.FloatField(blank=True, null=True)
    any_std = models.FloatField(blank=True, null=True)
    condylomatosis = models.FloatField(blank=True, null=True)
    cervical_condylomatosis = models.FloatField(blank=True, null=True)
    vaginal = models.FloatField(blank=True, null=True)
    vulvo_perineal = models.FloatField(blank=True, null=True)
    syphilis = models.FloatField(blank=True, null=True)
    pelvic = models.FloatField(blank=True, null=True)
    genital = models.FloatField(blank=True, null=True)
    molluscum = models.FloatField(blank=True, null=True)
    AIDS = models.FloatField(blank=True, null=True)
    HIV = models.FloatField(blank=True, null=True)
    hepatitis = models.FloatField(blank=True, null=True)
    HPV = models.FloatField(blank=True, null=True)
    diagnosis_std = models.FloatField(blank=True, null=True)
    cancer = models.FloatField(blank=True, null=True)
    neoplasis = models.FloatField(blank=True, null=True)
    diagnosis_hpv = models.FloatField(blank=True, null=True)

    report = JSONField({})
    def __str__(self):
        return self.timing