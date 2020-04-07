from rest_framework import viewsets
from api.models import LogCategory, LogSubCategory, MilestoneYear, LogData
from api.serializers import LogCategorySerializer, LogSubCategorySerializer, LogDataSerializer, MilestoneYearSerializer, \
    LogDataAlternativeSerializer

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend


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
    queryset = LogData.objects.order_by('id')
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'category', 'sub_category', 'year', 'is_related']


class LogDataSingle(viewsets.ModelViewSet):
    queryset = True

    def list(self, request, **kwargs):
        data = []

        log_cat = LogCategory.objects.order_by('id')

        for cat in log_cat:
            print('category', cat.name)

            category = {
                'id': cat.id,
                'name': cat.name,
                'title': cat.title,

            }

            log_subcat = LogSubCategory.objects.filter(category__id=cat.id)

            for sub_cat in log_subcat:
                print('sub-cat', sub_cat.name)

                log_data = LogData.objects.filter(sub_category__id=sub_cat.id)
                sub_category = {
                    'id': sub_cat.id,
                    'name': sub_cat.name,
                    'title': sub_cat.title,
                    'category': sub_cat.category.id
                }

                for frame in log_data:
                    print('data', frame.sub_category.name)

                    if frame.year.period == 'y1':
                        try:
                            achieved = frame.achieved
                            planned = frame.planned_afp
                        except:
                            achieved = 0
                            planned = 0

                    elif frame.year.period == 'y2':

                        try:
                            prev = LogData.objects.get(sub_category__id=sub_cat.id, year__period='y1')
                            planned = str(float(frame.planned_afp) - float(prev.planned_afp))
                            achieved = str(float(frame.achieved) - float(prev.achieved))
                        except:
                            planned = 0
                            achieved = 0

                    elif frame.year.period == 'y3':
                        try:
                            prev = LogData.objects.get(sub_category__id=sub_cat.id, year__period='y2')
                            planned = str(float(frame.planned_afp) - float(prev.planned_afp))
                            achieved = str(float(frame.achieved) - float(prev.achieved))
                        except:
                            planned = 0
                            achieved = 0
                    elif frame.year.period == 'y4':
                        try:
                            prev = LogData.objects.get(sub_category__id=sub_cat.id, year__period='y3')
                            planned = str(float(frame.planned_afp) - float(prev.planned_afp))
                            achieved = str(float(frame.achieved) - float(prev.achieved))
                        except:
                            planned = 0
                            achieved = 0
                    elif frame.year.period == 'y5':
                        try:
                            prev = LogData.objects.get(sub_category__id=sub_cat.id, year__period='y4')
                            planned = str(float(frame.planned_afp) - float(prev.planned_afp))
                            achieved = str(float(frame.achieved) - float(prev.achieved))
                        except:
                            planned = 0
                            achieved = 0
                    elif frame.year.period == 'y6':
                        try:
                            prev = LogData.objects.get(sub_category__id=sub_cat.id, year__period='y5')
                            planned = str(float(frame.planned_afp) - float(prev.planned_afp))
                            achieved = str(float(frame.achieved) - float(prev.achieved))
                        except:
                            planned = 0
                            achieved = 0
                    elif frame.year.period == 'y7':
                        try:
                            prev = LogData.objects.get(sub_category__id=sub_cat.id, year__period='y6')
                            planned = str(float(frame.planned_afp) - float(prev.planned_afp))
                            achieved = str(float(frame.achieved) - float(prev.achieved))
                        except:
                            planned = 0
                            achieved = 0
                    elif frame.year.period == 'y8':
                        try:
                            prev = LogData.objects.get(sub_category__id=sub_cat.id, year__period='y7')
                            planned = str(float(frame.planned_afp) - float(prev.planned_afp))
                            achieved = str(float(frame.achieved) - float(prev.achieved))
                        except:
                            planned = 0
                            achieved = 0
                    elif frame.year.period == 'y9':
                        try:
                            prev = LogData.objects.get(sub_category__id=sub_cat.id, year__period='y8')
                            planned = str(float(frame.planned_afp) - float(prev.planned_afp))
                            achieved = str(float(frame.achieved) - float(prev.achieved))
                        except:
                            planned = 0
                            achieved = 0
                    elif frame.year.period == 'y10':
                        try:
                            prev = LogData.objects.get(sub_category__id=sub_cat.id, year__period='y9')
                            planned = str(float(frame.planned_afp) - float(prev.planned_afp))
                            achieved = str(float(frame.achieved) - float(prev.achieved))
                        except:
                            planned = 0
                            achieved = 0
                    else:
                        planned = 0
                        achieved = 0
                    year = {
                        'id': frame.year.id,
                        'name': frame.year.name,
                        'range': frame.year.range,
                    }
                    data.append(
                        {
                            'id': frame.id,
                            'data_type': frame.data_type,
                            'planned_afp': planned,
                            'achieved': achieved,
                            'unit': frame.unit,
                            'is_related': frame.is_related,
                            'year': year,
                            'sub_category': sub_category,
                            'category': category

                        }
                    )

        return Response({"results": data})
