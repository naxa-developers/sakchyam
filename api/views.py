from rest_framework import viewsets
from api.models import LogCategory, LogSubCategory, MilestoneYear, LogData, Province, District, Municipality, Automation
from api.serializers import LogCategorySerializer, LogSubCategorySerializer, LogDataSerializer, MilestoneYearSerializer, \
    LogDataAlternativeSerializer, ProvinceSerializer, DistrictSerializer, MunicipalitySerializer, AutomationSerializer

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User, Group, Permission
from dashboard.models import UserProfile
from django.core import serializers
from django.db.models import Sum


class LogCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = LogCategorySerializer
    queryset = LogCategory.objects.all()
    permission_classes = [IsAuthenticated, ]


class LogSubCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = LogSubCategorySerializer
    queryset = LogSubCategory.objects.all()
    permission_classes = [IsAuthenticated, ]


class MilestoneYearViewSet(viewsets.ModelViewSet):
    serializer_class = MilestoneYearSerializer
    queryset = MilestoneYear.objects.all()
    permission_classes = [IsAuthenticated, ]


class LogDataViewSet(viewsets.ModelViewSet):
    serializer_class = LogDataSerializer
    queryset = LogData.objects.all()
    permission_classes = [IsAuthenticated, ]


class LogDataAlternativeViewSet(viewsets.ModelViewSet):
    serializer_class = LogDataAlternativeSerializer
    queryset = LogData.objects.order_by('id')
    permission_classes = [IsAuthenticated, ]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'category', 'sub_category', 'year', 'is_related']


class AutomationViewSet(viewsets.ModelViewSet):
    serializer_class = AutomationSerializer
    queryset = Automation.objects.order_by('id')
    permission_classes = [IsAuthenticated, ]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'partner_institution', 'branch', 'province_id', 'district_id', 'municipality_id', ]


class ProvinceViewSet(viewsets.ModelViewSet):
    serializer_class = ProvinceSerializer
    queryset = Province.objects.order_by('id')
    permission_classes = [IsAuthenticated, ]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', ]


class DistrictViewSet(viewsets.ModelViewSet):
    serializer_class = DistrictSerializer
    queryset = District.objects.order_by('id')
    permission_classes = [IsAuthenticated, ]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', ]


class MunicipalityViewSet(viewsets.ModelViewSet):
    serializer_class = MunicipalitySerializer
    queryset = Municipality.objects.order_by('id')
    permission_classes = [IsAuthenticated, ]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', ]


class UserPermission(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = True

    def list(self, request, **kwargs):
        print('user', self.request.user.id)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        group = Group.objects.get(user=user)
        permission = Permission.objects.values_list('codename', flat=True).filter(group=group)

        user_info = [{
            "id": user_data.id,
            "name": user_data.full_name,
            "email": user_data.email,
            "image": user_data.thumbnail.url,
            "permission": permission,

        }]

        return Response(user_info)


class LogDataSingle(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
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

            log_subcat = LogSubCategory.objects.filter(category__id=cat.id).order_by('id')

            for sub_cat in log_subcat:
                print('sub-cat', sub_cat.name)

                log_data = LogData.objects.filter(sub_category__id=sub_cat.id).order_by('id')
                sub_category = {
                    'id': sub_cat.id,
                    'name': sub_cat.name,
                    'title': sub_cat.title,
                    'category': sub_cat.category.id,
                    'description': sub_cat.description
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

        return Response(data)


class AutomationDataDistrict(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = True

    def list(self, request, **kwargs):
        print('user', self.request.user.id)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        group = Group.objects.get(user=user)
        data = []
        district = District.objects.values('id', 'name', 'code', ).order_by('id')
        for dist in district:
            automation = Automation.objects.filter(district_id=dist['id'])
            tablet_sum = automation.aggregate(
                Sum('num_tablet_deployed'))
            data_auto = []
            for auto in automation:
                data_auto.append({
                    'province_id': auto.province_id.id,
                    'district_id': auto.district_id.id,
                    'municipality_id': auto.municipality_id.id,
                    'partner_institution': auto.partner_institution,
                    'branch': auto.branch,
                    'num_tablet_deployed': auto.num_tablet_deployed,
                })

            data.append(
                {
                    "id": dist['id'],
                    "name": dist['name'],
                    "code": dist['code'],
                    "num_tablet_deployed": tablet_sum['num_tablet_deployed__sum'],
                    'data': data_auto,

                }
            )

        return Response(data)


class AutomationDataProvince(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = True

    def list(self, request, **kwargs):
        print('user', self.request.user.id)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        group = Group.objects.get(user=user)
        data = []
        province = Province.objects.values('id', 'name', 'code', ).order_by('id')
        for prov in province:
            automation = Automation.objects.filter(province_id=prov['id'])
            tablet_sum = automation.aggregate(
                Sum('num_tablet_deployed'))
            data_auto = []
            for auto in automation:
                data_auto.append({
                    'province_id': auto.province_id.id,
                    'district_id': auto.district_id.id,
                    'municipality_id': auto.municipality_id.id,
                    'partner_institution': auto.partner_institution,
                    'branch': auto.branch,
                    'num_tablet_deployed': auto.num_tablet_deployed,
                })

            data.append(
                {
                    "id": prov['id'],
                    "name": prov['name'],
                    "code": prov['code'],
                    "num_tablet_deployed": tablet_sum['num_tablet_deployed__sum'],
                    'data': data_auto,

                }
            )

        return Response(data)


class AutomationDataMunicipality(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = True

    def list(self, request, **kwargs):
        print('user', self.request.user.id)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        group = Group.objects.get(user=user)
        data = []
        municipality = Municipality.objects.values('id', 'name', 'code', ).order_by('id')
        for mun in municipality:
            automation = Automation.objects.filter(municipality_id=mun['id'])
            tablet_sum = automation.aggregate(
                Sum('num_tablet_deployed'))
            data_auto = []
            for auto in automation:
                data_auto.append({
                    'province_id': auto.province_id.id,
                    'district_id': auto.district_id.id,
                    'municipality_id': auto.municipality_id.id,
                    'partner_institution': auto.partner_institution,
                    'branch': auto.branch,
                    'num_tablet_deployed': auto.num_tablet_deployed,
                })

            if data_auto:
                data.append(
                    {
                        "id": mun['id'],
                        "name": mun['name'],
                        "code": mun['code'],
                        "num_tablet_deployed": tablet_sum['num_tablet_deployed__sum'],
                        'data': data_auto,

                    }
                )

        return Response(data)


class AutomationDataPartner(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = True

    def list(self, request, **kwargs):
        print('user', self.request.user.id)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        group = Group.objects.get(user=user)
        data = []
        partner = Automation.objects.values('partner_institution', 'id').distinct("partner_institution")
        print(partner)
        for part in partner:
            print(part['partner_institution'])
            automation = Automation.objects.filter(partner_institution=part['partner_institution'])
            tablet_sum = automation.aggregate(
                Sum('num_tablet_deployed'))
            data_auto = []
            for auto in automation:
                data_auto.append({
                    'province_id': auto.province_id.id,
                    'district_id': auto.district_id.id,
                    'municipality_id': auto.municipality_id.id,
                    'partner_institution': auto.partner_institution,
                    'branch': auto.branch,
                    'num_tablet_deployed': auto.num_tablet_deployed,
                })

            if data_auto:
                data.append(
                    {
                        "id": part['id'],
                        "name": part['partner_institution'],
                        "num_tablet_deployed": tablet_sum['num_tablet_deployed__sum'],
                        'data': data_auto,

                    }
                )

        return Response(data)
