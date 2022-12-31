from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from accounts.models import User, Bike, Station
from random import randint
# Create your models here.

class QrModel(models.Model):
    name = models.CharField(max_length=200)
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE, blank=False, null=False)
    station = models.ForeignKey(Station, on_delete=models.CASCADE, blank=False, null=False)
    qr_code = models.ImageField(upload_to='qr_codes')

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        
        self.name = str(self.bike.pk) + "/" + str(self.station.pk) 
        qrcode_img = qrcode.make(self.name)
        canvas = Image.new('RGB', (290, 290), 'white')
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.name}.png'
        buffer = BytesIO()
        canvas.save(buffer,'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        print(self.name)
        super().save(*args, **kwargs)