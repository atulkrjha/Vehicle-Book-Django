from django.shortcuts import render, redirect
from .models import QrModel
from accounts.models import Bike, Order, Station, User
from django.contrib import messages

def home_view(request, pk1, pk2):
    print(pk1, pk2, request.user)
    print(not(str(request.user) == 'AnonymousUser'))
    #print(request.user.is_verified)
    if (Bike.objects.filter(pk=pk1)):
        print(Bike.objects.filter(pk=pk1))
        if (Bike.objects.get(pk=pk1).station.pk == pk2):
            if not(str(request.user) == 'AnonymousUser'):
                if User.objects.get(email = request.user).is_verified:
                        
                    ord1 = Order()
                    ord1.bike = Bike.objects.get(pk = pk1)
                    ord1.user = request.user
                    ord1.start_station = Station.objects.get(pk = pk2)
                    

                    bik1 = Bike.objects.get(pk=pk1)
                    bik1.in_use = True
                    bik1.save()
                    
                    ord1.save()

                    messages.success(request, ("Order Successful"))	
                    return redirect('dashboard')

    return redirect('dashboard')


def display_view(request):
    stations = Station.objects.all()
    bikes = Bike.objects.filter(in_use = False)

    context = {
        'stations':stations,
        'bikes':bikes
    }
    return render(request, 'qrcodeweb/displaylist.html', context = context)	
