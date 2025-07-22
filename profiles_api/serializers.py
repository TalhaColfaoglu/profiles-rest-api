from rest_framework import serializers

from profiles_api import models


class HelloSerializer(serializers.Serializer):
    """Serializes a name field for testing our APIView"""
    name = serializers.CharField(max_length = 10)


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""

    class Meta:
        model = models.UserProfile #Meta içinde hangi modelle çalışacağını söylüyorsun: UserProfile
        fields = ('id', 'email', 'name', 'password') #Bu modelden sadece id, email, name, password alanlarını API'ye açıyorsun
        extra_kwargs= {
            'password': {
                'write_only': True, #`write_only=True` → API'de şifre **gösterilmesin**, sadece yazılabilsin
                'style': {'input_type': 'password'} #`style` → Browsable API arayüzünde şifre kutusu görünüşünü ayarlıyor (●●● şeklinde
            }
        }

    def create(self, validated_data): #Kullanıcı API’den kayıt olmaya çalışırsa bu create() fonksiyonu çalışacak
        """Create and return a new user"""
        user = models.UserProfile.objects.create_user( #- Bu satırda kullanıcıyı **custom create_user()** fonksiyonuyla kaydediyorsun  
            email=validated_data['email'], #- Çünkü `UserProfile` modelinde `create_user()` metodu var (şifreyi hash'li kaydetmek için)
            name=validated_data['name'],
            password=validated_data['password'],
        )

        return user

class ProfileFeedItemSerializer(serializers.ModelSerializer): #ModelSerializer kullandığın için, modelin alanlarını otomatik olarak alıyor. Elinle tek tek tanımlamıyorsun
    """Serializes profile feed items"""

    class Meta:
        model = models.ProfileFeedItem #Hangi modeli kullanıyoruz? → ProfileFeedItem modelini
        fields = ('id', 'user_profile', 'status_text', 'created_on') #Bu alanlar JSON’a dahil edilecek. Evet, fields kısmını eklemeseydin, Django hangi alanları serialize edeceğini bilemezdi ve hata verirdi. Yani, bir şeyleri serialize etmek istiyorsan hangi alanları dahil etmek istediğini yazmalısın.
        extra_kwargs = {'user_profile': {'read_only': True}} #user_profile alanını sadece okumaya izin ver, yani kullanıcı bu alanı post, put, patch ile değiştiremesin. fields = (...) ile alanları belirtiyorsun, ama her alanın tek tek özelliklerini ayarlamak için extra_kwargs kullanman gerekiyor.