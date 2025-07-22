from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views

router= DefaultRouter()
router.register('hello-viewset', views.HelloViewSet, basename= 'hello-viewset')
router.register('profile', views.UserProfileViewSet) #queryset zaten yazdık o yüzden basename'e gerek yok
router.register('feed', views.UserProfileFeedViewSet)

urlpatterns = [
    path('hello-view/', views.HelloApiView.as_view()),
    path('login/', views.UserLoginApiView.as_view()),
    path('', include(router.urls)),
]