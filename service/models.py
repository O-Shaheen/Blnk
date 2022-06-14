from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
# Create your models here.
class Fund_options(models.Model):   
    #FID = models.UUIDField()
    mn_amount = models.PositiveBigIntegerField(null=True)
    mx_amount = models.PositiveBigIntegerField(null=True)
    interst_numerator  = models.PositiveIntegerField(null=True)
    interst_denominator   = models.PositiveIntegerField(null=True)
    fund_duration = models.PositiveIntegerField(null=True)

class Loan_options(models.Model):
    #LID = models.UUIDField()
    mn_amount = models.PositiveBigIntegerField(null=True)
    mx_amount = models.PositiveBigIntegerField(null=True)
    interst_numerator  = models.PositiveIntegerField(null=True)
    interst_denominator = models.PositiveIntegerField(null=True)
    loan_duration = models.PositiveIntegerField(null=True)

REVIEW = 1
ACCEPTED  = 2
REJECTED = 3
STATUS_CHOICES = (
    (REVIEW, 'Review'),
    (ACCEPTED, 'accepted'),
    (REJECTED, 'rejected'),
)
class Fund_applications(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    FID = models.ForeignKey(Fund_options, related_name='FundApplication', on_delete= models.CASCADE)
    #provider = models.ForeignKey('users.provider', related_name='FundApplication', on_delete= models.CASCADE )
    stat = models.PositiveIntegerField(choices=STATUS_CHOICES, default= 0)
    money = models.PositiveIntegerField(blank=False)

class Loan_applications(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    LID = models.ForeignKey(Loan_options, related_name='LoanApplication', on_delete= models.CASCADE)
    #bor = models.ForeignKey('users.borrower', related_name='LoanApplication', on_delete= models.CASCADE )
    stat = models.PositiveIntegerField(choices=STATUS_CHOICES, default= 0)
    money = models.PositiveIntegerField(blank=False)


class User(AbstractUser):
    is_loaner = models.BooleanField(default=False)
    is_funder = models.BooleanField(default=False)
    is_banker = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=254)
    def _str_(self):
        return self.first_name

class loaner(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    balance = models.IntegerField(default=0)
    dueMoney = models.IntegerField(default=0)
    
class funder(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    balance = models.IntegerField(default=0)

class banker(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    balance = models.IntegerField(default=0)
    
"""class banker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)"""