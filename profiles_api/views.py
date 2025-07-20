from rest_framework.views import APIView #➡️ DRF’in temel APIView sınıfını içeri aktarır. Bu, HTTP isteklerini (GET, POST, vs.) işleyebilmeni sağlar.
from rest_framework.response import Response #➡️ API'den JSON formatında veri döndürmek için kullanılır. Django'nun HttpResponse'una benzer ama DRF'e özel.

class HelloApiView(APIView): #➡️ APIView'den türeyen özel bir sınıf tanımladın. Bu senin kendi API endpoint’in olacak. Yani bu sınıf, bir URL adresine bağlanıp cevap verecek.
    """Test API View"""

    def get(self, request, format=None): #➡️ Bu metod, biri tarayıcıdan ya da Postman'den GET isteği gönderdiğinde çalışır. format=None demek, örneğin .json uzantısı alabilir ama zorunlu değil.
        """Returns a list of APIView features"""
        an_apiview = [ #➡️ Bu, APIView'in ne işe yaradığını açıklayan bir liste. Öğretici amaçlı yazılmış.
            'Uses HTTP methods as function (get, post, patch, put, delete)',
            'Is similar to a traditional Django View',
            'Gives you the most control over you application logic',
            'Is mapped manually to URLs'
        ]

        return Response({'message': 'Hello', 'an_apiview': an_apiview})
