from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
#models klasöründe importlar ve classlar arasında iki satır boşluklar olmalı

class UserProfileManager(BaseUserManager): #Bu sınıf, kendi yazdığımız UserProfile modeli için özel bir yönetici (manager) tanımlar.Yani: “Kullanıcı nasıl oluşturulacak?”, “Süper kullanıcı nasıl oluşur?” sorularını burada cevaplıyoruz.
    """Manager for user profiles"""

    def create_user(self, email, name, password=None): 
        """Create a new user profile"""
        if not email:
            raise ValueError('users must have an email address')

        email = self.normalize_email(email=email) #Email'i küçük harfe çevirip düzenler
        user = self.model(email=email,name=name) #Email'i küçük harfe çevirip düzenler

        user.set_password(password) #Şifreyi hash’ler (güvenli hale getirir)
        user.save(using=self._db) #Veritabanına kaydeder

        return user #Oluşturulan kullanıcıyı döner
    
    def create_superuser(self, email, name, password):
        """Create and save a new superuser with given details"""
        user = self.create_user(email=email,name=name,password=password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True) #kullanıcı aktif mi diye bakıyoruz
    is_staff = models.BooleanField(default=False) #çalışan mı bunu belirliyor

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Retrive full name of user"""
        return self.name
    
    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name
    
    def __str__(self):
        """Return string representation of our user"""
        return self.email