from rest_framework import serializers
from .models import Fund_options, Fund_applications, Loan_options, Loan_applications, loaner, funder, banker
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        User = get_user_model()
        model = User
        fields = ('email', 'username', 'password', 'is_loaner', 'is_funder')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

class fund_options_serializers(serializers.ModelSerializer):
    class Meta:
        model = Fund_options
        fields = ['mn_amount', 'mx_amount', 'interst_numerator', 'interst_denominator','fund_duration' , 'FundApplication']

class Fund_applications_serializers(serializers.ModelSerializer):
    class Meta:
        model = Fund_applications
        fields = '__all__'


class Loan_options_serializers(serializers.ModelSerializer):
    class Meta:
        model = Loan_options
        fields = ['pk','mn_amount', 'mx_amount', 'interst_numerator', 'interst_denominator','loan_duration' , 'LoanApplication']

class Loan_applications_serializers(serializers.ModelSerializer):
    class Meta:
        model = Loan_applications
        fields = '__all__'

class Loaner_serializers(serializers.ModelSerializer):
    class Meta:
        model = loaner
        fields = '__all__'

class Funder_serializers(serializers.ModelSerializer):
    class Meta:
        model = funder
        fields = '__all__'

class banker_serializers(serializers.ModelSerializer):
    class Meta:
        model = banker
        fields = '__all__'