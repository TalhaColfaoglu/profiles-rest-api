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
