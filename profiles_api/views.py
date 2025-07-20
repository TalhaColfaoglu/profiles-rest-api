from rest_framework.views import APIView #➡️ DRF’in temel APIView sınıfını içeri aktarır. Bu, HTTP isteklerini (GET, POST, vs.) işleyebilmeni sağlar.
from rest_framework.response import Response #➡️ API'den JSON formatında veri döndürmek için kullanılır. Django'nun HttpResponse'una benzer ama DRF'e özel.
from rest_framework import status

from profiles_api import serializers


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
