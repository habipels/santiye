from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image
from io import BytesIO
# Create your models here.
class CustomUser(AbstractUser):

    STATUS = (
        ('sirket', 'sirket'),
        ('sirketcalisani', 'sirketcalisani'),
        ('moderator', 'moderator'),
    )

    email = models.EmailField(unique=True)
    status = models.CharField(max_length=100, choices=STATUS, default='sirket')
    description = models.TextField("Açıklama", max_length=600, default='', blank=True)
    kullanicilar_db = models.ForeignKey('self',blank=True,null=True,related_name='children',on_delete=models.CASCADE)
    kullanici_silme_bilgisi = models.BooleanField(default= False)
    image  = models.ImageField(upload_to='profile/',verbose_name="Profile",blank=True,null=True,)
    background_image  = models.ImageField(upload_to='background/',verbose_name="background",blank=True,null=True,)
    telefon_numarasi =  models.CharField(max_length= 20 , verbose_name="Telefon Numarası ",blank=True,null = True)
    gorevi = models.CharField(max_length = 250 ,verbose_name="Görevi",blank = True,null = True)

    
    def save(self, *args, **kwargs):
        super(CustomUser, self).save(*args, **kwargs)
        if self.image:
            with Image.open(self.image.path) as img:
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                width, height = img.size
                if width > 800:
                    new_width = 800
                    new_height = int((new_width / width) * height)
                    img = img.resize((new_width, new_height), Image.ANTIALIAS)
                    buffer = BytesIO()
                    img.save(buffer, format='JPEG', quality=60)
                    self.image.save(self.image.name, content=buffer, save=False)
                    super(CustomUser, self).save(*args, **kwargs)
    def __str__(self):
        return self.username


class personel_dosyalari(models.Model):
    kullanici = models.ForeignKey(CustomUser, on_delete = models.SET_NULL,blank  =True,null = True,verbose_name="Kullanıcı Bilgisi")
    dosyalari  = models.FileField(verbose_name="Kullanıcı Dosyası",upload_to='kullanici_dosyasi/',blank=True,null=True)
    