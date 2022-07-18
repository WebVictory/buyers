from zoneinfo import ZoneInfo

from rest_framework import permissions
from .models import Check, PositionCheck
from .serializers import CheckSerializer, PositionCheckSerializer
from rest_framework import viewsets, generics
from django.db.models import Sum
from django.utils.dateparse import parse_datetime
from rest_framework.views import APIView
from rest_framework.response import Response

class CheckViewSet(viewsets.ModelViewSet):
    queryset = Check.objects.all().order_by('id')
    serializer_class = CheckSerializer
    permission_classes = [permissions.AllowAny]
    filterset_fields = {
        'issue_date': ['gte', 'lte', 'exact'],
    }

class ListPositionFull(generics.ListAPIView):
    serializer_class = PositionCheckSerializer

    def get_queryset(self):
        buyer = self.request.query_params.get('buyer')
        checks =Check.objects.filter(buyer=buyer)
        queryset = PositionCheck.objects.filter(parent_check__in=checks)
        return queryset

class ListStore(APIView):
    def get(self, request,):
        buyer = self.request.query_params.get('buyer')
        if buyer is None:
            return Response({'error': 'Нужно указать имя пользователя'})
        checks = Check.objects.filter(buyer=buyer).values_list('store',flat=True).distinct()
        return Response({'stores':checks})

class ListPosition(APIView):
    def get(self, request,):
        buyer = self.request.query_params.get('buyer')
        if buyer is None:
            return Response({'error': 'Нужно указать имя пользователя'})
        checks = Check.objects.filter(buyer=buyer)
        queryset = PositionCheck.objects.filter(parent_check__in=checks).values_list('name',flat=True).distinct()
        return Response({'positions': queryset})

class SumCheckAmount(APIView):
    def get(self, request,):
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if start_date is None or end_date is None:
            return Response({'error': 'Нужно указать начальную и конечную дату'})

        start_date_naive = parse_datetime(start_date)
        start_date_valid = start_date_naive.replace(tzinfo=ZoneInfo("Europe/Moscow"))
        end_date_naive = parse_datetime(end_date)
        end_date_valid = end_date_naive.replace(tzinfo=ZoneInfo("Europe/Moscow"))
        sum = Check.objects.filter(issue_date__range=(start_date_valid,end_date_valid)).aggregate(Sum('check_amount'))
        return Response({'sum': sum['check_amount__sum']})