from operator import imod
import json as js
import stat
from rest_framework import request, status, viewsets
from .models import Loan_options, Loan_applications, Fund_options, Fund_applications, loaner, funder, banker
from .serializers import Loan_options_serializers, Loan_applications_serializers, fund_options_serializers, Fund_applications_serializers, UserSerializer, Loaner_serializers, Funder_serializers, banker_serializers
from rest_framework.response import Response 
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from .permissions import Is_loaner
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.decorators import action 

class LoanOptionViewSet(viewsets.ModelViewSet): 
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,)
    queryset = Loan_options.objects.all()
    serializer_class = Loan_options_serializers
    
    @action(detail=True, methods=['get'])
    def amortization(self, request, pk=None):
        if Loan_options.objects.filter(id=pk).exists() and 'money' in request.data:
            option = Loan_options.objects.get(id=pk)
            dur = option.loan_duration
            money = int(request.data['money'])
            if int(money) <= option.mx_amount and int(money) >= option.mn_amount:
                print(money,  option.interst_numerator, option.interst_denominator)
                dict_response = {}
                for i in range(1, dur+1):
                    ind = "year "+ str(i)
                    dict_response[ind] = (money * option.interst_numerator) / option.interst_denominator
                ind = "year "+ str(dur)
                dict_response[ind] = dict_response[ind] + money
                json = js.dumps(dict_response) 
                return Response(json , status=status.HTTP_202_ACCEPTED)
            else: 
                json = {
                    'message': 'money out bounds'
                }
                return Response(json , status=status.HTTP_400_BAD_REQUEST)  
        else:
            json = {
                'message': 'money or option do not exist'
            }
            return Response(json , status=status.HTTP_400_BAD_REQUEST)             

    @action(detail=True, methods=['post'])
    def applyForLoan(self, request, pk=None):
        if 'money' in request.data:
            option = Loan_options.objects.get(id=pk)
            money = int(request.data['money'])
            user = request.user
            if(request.user.is_loaner == False):
                json = {
                    'message': 'you are not a loaner'
                }
                return Response(json , status=status.HTTP_400_BAD_REQUEST)
            
            if int(money) <= option.mx_amount and int(money) >= option.mn_amount:
                try:
                    # update
                    application = Loan_applications.objects.get(author=user.id, LID=option.id) # specific rate 
                    application.money = money
                    application.stat = 1
                    application.save()
                    serializer = Loan_applications_serializers(application, many=False)
                    json = {
                        'message': 'application update',
                        'result': serializer.data
                    }
                    return Response(json , status=status.HTTP_202_ACCEPTED)
                except:
                    # create if the rate not exist 
                    application = Loan_applications.objects.create(money=money, LID=option, author=user, stat = 1)
                    serializer = Loan_applications_serializers(application, many=False)
                    json = {
                        'message': 'application Created',
                        'result': serializer.data
                    }
                    return Response(json , status=status.HTTP_200_OK)
            else:
                json = {
                    'message': 'money is out of bounds'
                }
                return Response(json , status=status.HTTP_400_BAD_REQUEST)     
        else:
            json = {
                'message': 'money not provided'
            }
            return Response(json , status=status.HTTP_400_BAD_REQUEST)

class FundOptionViewSet(viewsets.ModelViewSet):
    queryset = Fund_options.objects.all()
    serializer_class = fund_options_serializers
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods=['get'])
    def amortization(self, request, pk=None):
        if Fund_options.objects.filter(id=pk).exists() and 'money' in request.data:
            option = Fund_options.objects.get(id=pk)
            dur = option.fund_duration
            money = int(request.data['money'])
            if int(money) <= option.mx_amount and int(money) >= option.mn_amount:
                print(money,  option.interst_numerator, option.interst_denominator)
                dict_response = { }
                for i in range(1, dur+1):
                    ind = "year "+ str(i)
                    dict_response[ind] = (money * option.interst_numerator) / option.interst_denominator
                ind = "year "+ str(dur)
                dict_response[ind] = dict_response[ind] + money
                json = js.dumps(dict_response) 
                return Response(json , status=status.HTTP_202_ACCEPTED)
            else: 
                json = {
                    'message': 'mony out bounds'
                }
                return Response(json , status=status.HTTP_400_BAD_REQUEST)  
        else:
            json = {
                'message': 'mony or option do not exist'
            }
            return Response(json , status=status.HTTP_400_BAD_REQUEST) 

    @action(detail=True, methods=['post'])
    def applyForFund(self, request, pk=None):
        if(request.user.is_funder == False):
            json = {
                'message': 'you are not a funder'
            }
            return Response(json , status=status.HTTP_400_BAD_REQUEST)
        if 'money' in request.data:
            option = Fund_options.objects.get(id=pk)
            money = int(request.data['money'])
            user = request.user
            if int(money) <= option.mx_amount and int(money) >= option.mn_amount:
                try:
                    # update
                    application = Fund_applications.objects.get(author=user.id, FID=option.id) # specific rate 
                    application.money = money
                    application.save()
                    serializer = fund_options_serializers(application, many=False)
                    json = {
                        'message': 'Fund application update',
                        'result': serializer.data
                    }
                    return Response(json , status=status.HTTP_202_ACCEPTED)
                except:
                    # create if the rate not exist 
                    application = Fund_applications.objects.create(money=money, FID=option, author=user, stat = 1)
                    serializer = Fund_applications_serializers(application, many=False)
                    json = {
                        'message': 'Fund application Created',
                        'result': serializer.data
                    }
                    return Response(json , status=status.HTTP_200_OK)
            else:
                json = {
                    'message': 'money is out of bounds'
                }
                return Response(json , status=status.HTTP_400_BAD_REQUEST)     
        else:
            json = {
                'message': 'money not provided'
            }
            return Response(json , status=status.HTTP_400_BAD_REQUEST)







class LoanAppViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication, )
    permission_classes =  (Is_loaner,)
    queryset = Loan_applications.objects.all()
    serializer_class = Loan_applications_serializers

    @action(detail=True, methods=['post'])
    def review(self, request, pk = None):
        if(request.user.is_banker == False):
            json = {
                'message': 'you are not a banker'
            }
            return Response(json , status=status.HTTP_400_BAD_REQUEST)
        if 'stat'in request.data:
            if Loan_applications.objects.filter(id=pk).exists():
                newStat = request.data['stat']
                application = Loan_applications.objects.get(id=pk)
                owner = application.author
                if(application.stat != 1):
                    appserializer = Loan_applications_serializers(application, many=False)
                    json = {
                        'message': 'application already reviewed',
                        'app result': appserializer.data
                    }
                    return Response(json , status=status.HTTP_400_BAD_REQUEST)
                if(newStat == '2'):
                    bankAcc = banker.objects.get(user_id=1)
                    if(int(application.money) > bankAcc.balance):
                        bankserializer = banker_serializers(bankAcc, many=False)
                        json = {
                            'message': 'we donot have enough money',
                            'app result': bankserializer.data
                        }
                        return Response(json , status=status.HTTP_400_BAD_REQUEST)                    
                    application.stat = int(newStat)
                    loanerAcc = loaner.objects.get(user=owner)
                    loanerAcc.balance = loanerAcc.balance + int(application.money)
                    application.save()
                    loanerAcc.save()
                    appserializer = Loan_applications_serializers(application, many=False)
                    loanserializer = Loaner_serializers(loanerAcc, many=False)
                    json = {
                        'message': 'application accepted',
                        'app result': appserializer.data, 
                        'transfer result': loanserializer.data
                    }
                    return Response(json , status=status.HTTP_202_ACCEPTED)
                else:
                    application.stat = int(newStat)
                    application.save()
                    appserializer = Loan_applications_serializers(application, many=False)
                    json = {
                        'message': 'application rejected',
                        'app result': appserializer.data
                    }
                    return Response(json , status=status.HTTP_400_BAD_REQUEST)      
            else:
                json = {
                    'message': 'no applications with such ID'
                }
                return Response(json , status=status.HTTP_400_BAD_REQUEST)
        else:
            json = {
                'message': 'stat is missing'
            }
            return Response(json , status=status.HTTP_400_BAD_REQUEST)
    def update(self, request, *args, **kwargs):
        response = {
            'message': 'Invalid way to create or update '
            }

        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def create(self, request, *args, **kwargs):
        response = {
            'message': 'Invalid way to create or update '
            }

        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    


class FundAppViewSet(viewsets.ModelViewSet):
    queryset = Fund_applications.objects.all()
    serializer_class = Fund_applications_serializers
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods=['post'])
    def review(self, request, pk = None):
        if(request.user.is_banker == False):
            json = {
                'message': 'you are not a banker'
            }
            return Response(json , status=status.HTTP_400_BAD_REQUEST)
        if'stat'in request.data:
            newStat = request.data['stat']
            if Fund_applications.objects.filter(id=pk).exists():
                print("new Stat>>>>>>>>", newStat)
                application = Fund_applications.objects.get(id=pk)
                print(application)
                owner = application.author
                if(application.stat != 1):
                    appserializer = Fund_applications_serializers(application, many=False)
                    json = {
                        'message': 'application already reviewed',
                        'app result': appserializer.data
                    }
                    return Response(json , status=status.HTTP_202_ACCEPTED)
                if(newStat == '2'):
                    bankAcc = banker.objects.get(user_id=1)
                    application.stat = int(newStat)
                    funderAcc = funder.objects.get(user=owner)
                    funderAcc.balance = funderAcc.balance - int(application.money)
                    bankAcc.balance = bankAcc.balance + int(application.money)
                    bankAcc.save()
                    application.save()
                    funderAcc.save()
                    appserializer = Fund_applications_serializers(application, many=False)
                    fundserializer = Funder_serializers(funderAcc, many=False)
                    bankserializer = banker_serializers(bankAcc, many = False)
                    json = {
                        'message': 'application accepted',
                        'app result': appserializer.data, 
                        'fund result': fundserializer.data, 
                        'our bank': bankserializer.data
                    }
                    return Response(json , status=status.HTTP_202_ACCEPTED)
                else:
                    application.stat = int(newStat)
                    application.save()
                    appserializer = Fund_applications_serializers(application, many=False)
                    json = {
                        'message': 'application rejected',
                        'app result': appserializer.data
                    }
                    return Response(json , status=status.HTTP_202_ACCEPTED)      
            else:
                json = {
                    'message': 'no applications with such values'
                }
                return Response(json , status=status.HTTP_400_BAD_REQUEST)
        else:
            json = {
                'message': 'either fid or author or stat is missing'
            }
            return Response(json , status=status.HTTP_400_BAD_REQUEST)
    def update(self, request, *args, **kwargs):
        response = {
            'message': 'Invalid way to create or update '
            }

        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def create(self, request, *args, **kwargs):
        response = {
            'message': 'Invalid way to create or update '
            }

        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    






















class FunderViewSet(viewsets.ModelViewSet):
    queryset = funder.objects.all()
    serializer_class = Funder_serializers
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,)

class LoanerViewSet(viewsets.ModelViewSet):
    queryset = loaner.objects.all()
    serializer_class = Loaner_serializers
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods=['post'])
    def pay(self, request, pk = None):
        if(request.user.is_loaner == False):
            json = {
                'message': 'you are not a loaner'
            }
            return Response(json , status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        print(user, user.id)
        if 'money' in request.data and loaner.objects.filter(user=user.id).exists():
            acc = loaner.objects.get(user=user.id)
            money = int(request.data['money'])
            if int(money) <= acc.balance and money <= acc.dueMoney:
                acc.balance = acc.balance - money
                acc.dueMoney = acc.dueMoney - money
                acc.save()
                serializer = Loaner_serializers(acc, many=False)
                json = {
                    'message': 'money was paid',
                    'result': serializer.data
                }
                return Response(json , status=status.HTTP_202_ACCEPTED)
            else:
                json = {
                    'message': 'money is out of bounds'
                }
                return Response(json , status=status.HTTP_400_BAD_REQUEST)     
        else:
            json = {
                'message': 'money not provided or you donot have an account'
            }
            return Response(json , status=status.HTTP_400_BAD_REQUEST)
    def update(self, request, *args, **kwargs):
        response = {
            'message': 'Invalid way to create or update '
            }

        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def create(self, request, *args, **kwargs):
        response = {
            'message': 'Invalid way to create or update '
            }

        return Response(response, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
    User = get_user_model()
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # #authentication_classes = (TokenAuthentication, )
    permission_classes = (AllowAny,)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        token, created = Token.objects.get_or_create(user=serializer.instance)
        return Response({
                'token': token.key, 
                }, 
            status=status.HTTP_201_CREATED)
    
    def list(self, request, *args, **kwargs):
        response = {'message': 'You cant create money like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)



