from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, VerifyAccountSerializer, OrderSerializer, OrderCompleteSerializer
from .emails import *
from .models import User
from django.shortcuts import render, get_object_or_404, redirect
from .models import Bike, Station, Order
import datetime
from django.core import serializers
from .forms import EditOrderForm, CompleteOrderForm
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse
import json
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import  SessionAuthentication

# Create your views here.

class ProtectedAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        data = {'message': 'I am proteted'}
        return Response(data)



class RegisterAPI(APIView):
    
    def post(self, request):
        try:
            data = request.data
            serializer = UserSerializer(data = data)
            if serializer.is_valid():
                serializer.save()
                send_otp_via_email(serializer.data['email'])
                return Response({
                    'status' : 200,
                    'message' : 'registration successfully check email',
                    'data' : serializer.data,
                })


            return Response({
                    'status' : 400,
                    'message' : 'Something went wrong',
                    'data' : serializer.errors,
                })
        except Exception as e:
            print(e)

class VerifyOTP(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        try:
            data = request.data
            serializer = VerifyAccountSerializer(data = data)

            if serializer.is_valid():
                email = serializer.data['email']
                otp = serializer.data['otp']

                user = User.objects.filter(email = email)

                if not user.exists():
                    return Response({
                    'status' : 400,
                    'message' : 'Something went wrong',
                    'data' : 'invalid email',
                })

                if user[0].otp != otp:
                    return Response({
                    'status' : 400,
                    'message' : 'Something went wrong',
                    'data' : 'Wrong OTP',
                })

                user =user.first()
                user.is_verified = True
                print("here-api",user)
                user.save() 

                return Response({
                    'status' : 200,
                    'message' : 'Account Verified',
                    'data' : {},
                })


            return Response({
                    'status' : 400,
                    'message' : 'Something went wrong',
                    'data' : serializer.errors,
                })
       
       
        except Exception as e:
            print(e) 



class UserOrders(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer


    def post(self, request):
        print(request)
        print("----",request.data.get('email'))
        
        try:
            serializer = self.serializer_class(data = request.data)
            
            if serializer.is_valid():
                
                try:
                    email = serializer.validated_data.get('email')
                    user = User.objects.get(email = email)
                
                except:
                    return Response({
                    'status' : 400,
                    'message' : 'Something went wrong',
                    'data' : 'User Does not Exist',
                })


                if not user:
                    return Response({
                    'status' : 400,
                    'message' : 'Something went wrong',
                    'data' : 'invalid email',
                })

                if not user.is_verified:
                    return Response({
                    'status' : 400,
                    'message' : 'Something went wrong',
                    'data' : 'User Not verified',
                })

                else:
                    try:
                        orders = Order.objects.filter(user = user, is_complete = False)
                        print("here-api",orders)
                        data = {}
                        for order in orders:
                            bike_name = order.bike.bike_name
                            start_station = order.start_station.station_name
                            start_time = str(Order.objects.get(pk=35).start_time)[:19]
                            data[order.pk] = [bike_name, start_station, start_time]
                        
                        print(data)
                        """res = {
                            'email':email,
                            'bike_name':bike_name,
                            'start_station':start_station,
                            'start_time':start_time
                        }"""

                        return Response({
                            "status" : 200,
                            "message" : "Your Ordres",
                            "data" : data,
                        })
                    except Exception as e:
                        print(e)
                        return Response({
                        'status' : 400,
                        'message' : 'Something went wrong',
                        'data' : 'No order for user',
                    })
       
        except Exception as e:
            print(e) 


class UserCompleteOrders(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderCompleteSerializer


    def post(self, request):
        print(request)
        print("----",request.data.get('email'))
        
        try:
            serializer = self.serializer_class(data = request.data)
            
            if serializer.is_valid():
                
                try:
                    email = serializer.validated_data.get('email')
                    user = User.objects.get(email = email)
                                                        
                
                except:
                    return Response({
                    'status' : 400,
                    'message' : 'Something went wrong',
                    'data' : 'User Does not Exist',
                })


                if not user:
                    return Response({
                    'status' : 400,
                    'message' : 'Something went wrong',
                    'data' : 'invalid email',
                })

                if not user.is_verified:
                    return Response({
                    'status' : 400,
                    'message' : 'Something went wrong',
                    'data' : 'User Not verified',
                })

                else:
                    try:
                        
                        order = Order.objects.get(user = user, bike = serializer.validated_data.get('bike_id'), is_complete = False, )
                        order.is_complete = True
                        end_stn = Station.objects.get(pk = serializer.validated_data.get('end_station_id'))
                        order.end_station = end_stn
                        order.start_station = end_stn
                        bike = Bike.objects.get(pk = serializer.validated_data.get('bike_id'))
                        bike.in_use = False
                        bike.station = end_stn
                        bike.save()
                        order.save()  

                        return Response({
                            "status" : 200,
                            "message" : "Your Order is complete",
                            "data" : {},
                        })
                    except Exception as e:
                        print(e)
                        return Response({
                        'status' : 400,
                        'message' : 'Something went wrong',
                        'data' : 'No order for user',
                    })
       
        except Exception as e:
            print(e) 





"""def home(request):
    return render(request, 'home.html')


def how_it_works(request):
    locations = Station.objects.all()
    return render(request, 'how_it_works.html', context={'locations':locations})
"""



def DashboardView(request):

    user = None
    data = None
    print("here1")
    print(request.method)
    print(str(request.user) == 'AnonymousUser')
    if (str(request.user) == 'AnonymousUser'):
        messages.success(request, ("Anonymous User. Please signin"))	
        return redirect('login')
    else :
        user_ver = User.objects.get(email =str(request.user))
        if not user_ver.is_verified:
            messages.success(request, ("User not verified. Please signin"))
            return redirect('login')
        if not(str(request.user) == 'AnonymousUser') and (not request.method == 'POST'):
            print("here2")
            print(request.user)
            #customers_orders = Order.objects.all().filter(user = request.user, is_complete = False)
            user = request.user
            email = str(request.user)
            print(user_ver.aut_token)
            headers = {"Authorization": user_ver.aut_token}
            response = requests.post(settings.API_URL+'orders/', data={'email':email}, headers=headers)
            print(response.json())

            if response.status_code==200:
                data = list(response.json()['data'].values())
                print("---")
                print(data)
        elif not(str(request.user) == 'AnonymousUser') and (request.method == 'POST') :
            user = request.user
            email = str(request.user)
            print(request)

            if request.POST.get('end_station'):
                if not(str(request.user) == 'AnonymousUser'):
                    bike_id = request.POST.get('bike')
                    end_stn_id = request.POST.get('end_station')
                    headers = {"Authorization": user_ver.aut_token}   
                    response = requests.post(settings.API_URL+'orderscomplete/', data={'email':email, 'bike_id':bike_id, 'end_station_id':end_stn_id}, headers = headers)
                    print(response.json())

                    if response.status_code==200:
                        data = list(response.json()['data'].values())
            
                        messages.success(request, ("Saved"))	
                        return redirect('dashboard')
                    else:
                        #messages.success(request, ("Saved"))	
                        return redirect('dashboard')
                        


            else:
                if request.POST.get('qr'):
                    print(request.POST)
                    bike = Bike.objects.get(pk = int(request.POST.get('bike')), in_use = False)
                    code = bike.qr_code
                    url = bike.qr_url

                    form = EditOrderForm(request.POST)

                    context = {
                        'form':form,
                        'code':code,
                        'url':url
                    }

                    return render(request, 'accounts/dashboard.html', context=context) 


                else:

                    print("form here 1")
                    if not(str(request.user) == 'AnonymousUser'):
                        print(request.POST)
                        order = Order()
                        bike = Bike.objects.get(pk=request.POST.get('bike'))
                        bike.in_use = True
                        bike.save()
                        bike = Bike.objects.get(pk=request.POST.get('bike'))
                        
                        user = request.user
                        start_time = datetime.datetime.now()

                        order.user = user
                        order.start_time = start_time
                        order.start_station = Station.objects.get(pk=request.POST.get('start_station'))
                        order.bike = bike
                        
                        print(order)
                        
                        order.save()

                    
                        print("form here 4")
                        customers_orders = Order.objects.all().filter(user = request.user, is_complete = False)

                        messages.success(request, ("Saved"))	
                        return redirect('dashboard')	
                    
        form = EditOrderForm()
        form3 = EditOrderForm()
        form2 = CompleteOrderForm()
        if not(str(request.user) == 'AnonymousUser'):
            ord = Order.objects.filter(user = request.user, is_complete = False)
            bk = []
            for i in range(0, ord.count()):
                bk.append((ord.values()[i])['bike_id'])

            bk = Bike.objects.filter(pk__in = bk)

            form2.fields['end_station'].queryset = Station.objects.all()
            form2.fields['bike'].queryset = bk
            

        context = {
            'data':data,
            'user':user,
            'form':form,
            'form2':form2,
            'form3':form3
            }


        return render(request, 'accounts/dashboard.html', context=context)


def load_bikes(request):
    station = request.GET.get('station')
    bikes = Bike.objects.filter(station=station, in_use=False).order_by('bike_name')
    return render(request, 'accounts/bikes.html', {'bikes': bikes})



