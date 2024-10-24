from django.contrib.auth.models import AbstractUser
from django.db import models


class AppUser(AbstractUser):
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    account_type = models.CharField(max_length=50, default='basic')
    name = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=50, blank=True, null=True)
    dob = models.CharField(max_length=50, blank=True, null=True)
    qualification = models.CharField(max_length=50, blank=True, null=True)
    vcn_number = models.CharField(max_length=50, blank=True, null=True)  # New field
    specialization_category = models.CharField(max_length=100, blank=True, null=True)  # New field
    university = models.CharField(max_length=100, blank=True, null=True)  # New field
    state = models.CharField(max_length=100, blank=True, null=True)  # New field

    def __str__(self):
        return self.name if self.name else self.username