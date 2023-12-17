from django.contrib.auth.models import AbstractUser
from django.db import models

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
    def __str__(self):
        return self.username
