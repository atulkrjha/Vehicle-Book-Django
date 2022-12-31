#from accounts.models import User
from django import forms
from .models import Order, Bike, Station


class EditOrderForm(forms.ModelForm):	    
    
    class Meta:
        model = Order
        fields = ( "bike", "start_station",)
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bike'].queryset = Bike.objects.filter(station = Station.objects.first(), in_use = False)
    

class CompleteOrderForm(forms.ModelForm):	    
    
    class Meta:
        model = Order
        fields = ( "bike", "end_station",)

    
        
    


