from rest_framework import viewsets
from api.models import LogCategory, LogSubCategory, MilestoneYear, LogData
from api.serializers import LogCategorySerializer, LogSubCategorySerializer, LogDataSerializer, MilestoneYearSerializer, \
    LogDataAlternativeSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView



class LogCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = LogCategorySerializer
    queryset = LogCategory.objects.all()
    permission_classes = []


class LogSubCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = LogSubCategorySerializer
    queryset = LogSubCategory.objects.all()
    permission_classes = []


class MilestoneYearViewSet(viewsets.ModelViewSet):
    serializer_class = MilestoneYearSerializer
    queryset = MilestoneYear.objects.all()
    permission_classes = []


class LogDataViewSet(viewsets.ModelViewSet):
    serializer_class = LogDataSerializer
    queryset = LogData.objects.all()
    permission_classes = []


class LogDataAlternativeViewSet(viewsets.ModelViewSet):
    serializer_class = LogDataAlternativeSerializer
    queryset = LogData.objects.all()
    permission_classes = []

