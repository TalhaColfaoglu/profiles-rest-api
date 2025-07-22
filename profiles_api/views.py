from rest_framework.views import APIView #➡️ DRF’in temel APIView sınıfını içeri aktarır. Bu, HTTP isteklerini (GET, POST, vs.) işleyebilmeni sağlar.
from rest_framework.response import Response #➡️ API'den JSON formatında veri döndürmek için kullanılır. Django'nun HttpResponse'una benzer ama DRF'e özel.
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from profiles_api import permissions
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated

from profiles_api import serializers
from profiles_api import models

class HelloApiView(APIView): #➡️ APIView'den türeyen özel bir sınıf tanımladın. Bu senin kendi API endpoint’in olacak. Yani bu sınıf, bir URL adresine bağlanıp cevap verecek.
    """Test API View"""
    serializer_class = serializers.HelloSerializer


    def get(self, request, format=None): #➡️ Bu metod, biri tarayıcıdan ya da Postman'den GET isteği gönderdiğinde çalışır. format=None demek, örneğin .json uzantısı alabilir ama zorunlu değil.
        """Returns a list of APIView features"""
        an_apiview = [ #➡️ Bu, APIView'in ne işe yaradığını açıklayan bir liste. Öğretici amaçlı yazılmış.
            'Uses HTTP methods as function (get, post, patch, put, delete)',
            'Is similar to a traditional Django View',
            'Gives you the most control over you application logic',
            'Is mapped manually to URLs'
        ]

        return Response({'message': 'Hello', 'an_apiview': an_apiview})

    def post(self, request):
        """Create a hello message with our name"""
        serializers = self.serializer_class(data=request.data)

        if serializers.is_valid():
            name = serializers.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message': message})
        else:
            return Response(
                serializers.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
    def put(self, request, pk=None):
        """Handle updating an object"""
        return Response({'method': 'PUT'})
    
    def patch(self, request, pk=None):
        """Handle a partial update of an object"""
        return Response({'method': 'PATCH'})
    
    def delete(self, request, pk=None):
        """Delete an object"""
        return Response({'method': 'DELETE'})


class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet"""
    serializer_class = serializers.HelloSerializer

    def list(self, request):
        """Return a hello message"""

        a_viewset = [
            'Uses actions (list, create, retrieve, update, partial_update)',
            'Automatically maps to URLs using Routers',
            'Provides more functionality with less code',
        ]

        return Response({'message': 'Hello!', 'a_viewset': a_viewset})
    
    def create(self, request):
        """Create a new hello message"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}!'
            return Response({'message' : message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
    def retrieve(self, request, pk = None):
        """Handle getting an object by its ID
        retrieve() ViewSet içinde tek bir objeyi döner (ID ile)
        URL: /endpoint/<id>/
        DRF bunu otomatik bağlar → router ile
        get_object_or_404(Model, pk=pk) kullanılır genelde
        Bu methodu kullanmak için Detail view olmalı (/5/ gibi)
        """
        return Response({'htto_method': 'GET'})
    
    def update(self, request, pk=None):
        """Handle updating an object"""
        return Response({'http_method': 'PUT'})
    
    def partial_update(self, request, pk=None):
        """Handle updating part of an object"""
        return Response({'http_method': 'PATCH'})
    
    def destroy(self, request, pk=None):
        """Handle removing an object"""
        return Response({'http_method': 'DELETE'})

        
class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', 'email',)

class UserLoginApiView(ObtainAuthToken):
    """Handling creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class UserProfileFeedViewSet(viewsets.ModelViewSet):
     """Handles creating, reading and updating profile feed items"""
     authentication_classes = (TokenAuthentication, )
     serializer_class = serializers.ProfileFeedItemSerializer
     queryset = models.ProfileFeedItem.objects.all() #Veritabanından hangi verileri kullanacağını söyler
     permission_classes = (
         permissions.UpdateOwnStatus, #Kendi objesi mi?
         IsAuthenticated #Giriş yapmış mı?
     )

     def perform_create(self, serializer): #Bu özel bir fonksiyon. ModelViewSet bir şey oluştururken (POST) bu fonksiyonu çalıştırır. Yani aşağıdaki satırı çalıştırır
         """Sets the user profile to the logged in user"""
         serializer.save(user_profile=self.request.user) #"Yeni bir veri kaydederken, hangi kullanıcı giriş yaptıysa, onun adını otomatik olarak bu veriye yaz."
         # Sen uygulamaya Talha olarak giriş yaptın ve bir feed (gönderi) oluşturdun:
        # {
        #   "status_text": "Bugün göğüs günü çalıştım"
        # }
        # Ama bu JSON’un içinde "bu mesajı kim yazdı?" bilgisi yok.
        # Bu satır diyor ki:
        # self.request.user → şu an giriş yapmış kullanıcı
        # user_profile=... → veritabanında bu feed kime ait olacak?
