from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import Loan_applications, Loan_options, Fund_applications, Fund_options, User, loaner, funder, banker
# Register your models here.

admin.site.register(Loan_applications)
admin.site.register(Loan_options)
admin.site.register(Fund_applications)
admin.site.register(Fund_options)
admin.site.register(loaner)
admin.site.register(funder)
admin.site.register(banker)
admin.site.register(User)
