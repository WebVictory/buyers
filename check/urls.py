from django.urls import include, path
from rest_framework import routers
from . import views
from .views import ListPosition, ListStore, ListPositionFull, SumCheckAmount

router = routers.DefaultRouter()
router.register(r'check', views.CheckViewSet, basename='cheks_all')

urlpatterns = [

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/positons-buyer-full/', ListPositionFull.as_view()),
    path('api/positons-buyer/', ListPosition.as_view()),
    path('api/store-buyer/', ListStore.as_view()),
    path('api/sum/', SumCheckAmount.as_view()),
    path('api/', include(router.urls)),
]