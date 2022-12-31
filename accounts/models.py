from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from django.utils import timezone
from auth import settings
from PIL import Image, ImageDraw
import qrcode
from io import BytesIO
from django.core.files import File
from django.conf import settings
# Create your models here.





class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default = False)
    otp = models.CharField(max_length=6, null=False, blank=False)
    aut_token = models.CharField(max_length=100, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def name(self):
        return self.first_name + ' ' +self.last_name

    def __str__(self):
        return self.email

    @property
    def verified(self):
        return self.is_verified

    @property
    def primarykey(self):
        return self.pk

    @property
    def emailid(self):
        return self.email



class Station(models.Model):
    station_name = models.CharField(max_length=100, default="")
    station_place = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.station_name + ", " +self.station_place

    @property
    def number_of_bikes(self):
        available_bikes = self.bike_set.all().filter(in_use=False, is_faulty=False)
        return available_bikes.count()



class Bike(models.Model):
    bike_name = models.CharField(max_length=100, default="")
    in_use = models.BooleanField(default=False)
    is_faulty = models.BooleanField(default=False)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    qr_code = models.ImageField(upload_to='qr_codes', null = True, blank = True)
    qr_url =  models.CharField(max_length=100, default="",  null = True, blank = True)
    qrimg_url = models.CharField(max_length=100, default="",  null = True, blank = True)
    class Meta:
        verbose_name_plural = 'Bikes'

    def current_usage(self):
        if self.in_use:
            return "In Use"
        else:
            return "Free"

    def condition(self):
        if self.is_faulty:
            return "Faulty"
        else:
            return "Good"

    def __str__(self):
        return self.bike_name


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        baseurl = settings.QRCODE_URL + "qrcode/"
        self.qr_url = str(baseurl + str(self.pk) +"/"+ str(self.station.pk))
        qrcode_img = qrcode.make(str(baseurl + str(self.pk) +"/"+ str(self.station.pk)))
        canvas = Image.new('RGB', (350, 350), 'white')
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.bike_name}.png'
        self.qrimg_url = settings.MEDIA_URL + "qrcode/" + fname
        buffer = BytesIO()
        canvas.save(buffer,'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        #print(self.name)
        super().save(*args, **kwargs)



class Order(models.Model):

    bike = models.ForeignKey(Bike, on_delete=models.CASCADE, related_name='bike')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    start_station = models.ForeignKey(Station, on_delete=models.CASCADE, default="", related_name='startstation')
    end_station = models.ForeignKey(Station, on_delete=models.CASCADE, default=None, null=True, blank=True)
    start_time = models.DateTimeField(default=timezone.now)
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return "Order ID: {}\nCustomer ID: {}\nBike ID: {} ".format(self.pk, self.user, self.bike)


