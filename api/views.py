from rest_framework import viewsets
from api.models import LogCategory, LogSubCategory, MilestoneYear, LogData, Province, District, Municipality, \
    Automation, Partner, AutomationPartner
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
import json
from django.core.serializers import serialize
from rest_framework.decorators import action


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
    filterset_fields = ['id', 'partner__partner__id', 'branch', 'province_id', 'district_id', 'municipality_id', ]


class ProvinceViewSet(viewsets.ModelViewSet):
    serializer_class = ProvinceSerializer

    def get_queryset(self):
        print(self.request.POST.getlist('id'))
        province_id = self.request.POST.getlist('id')
        if province_id[0] == '0':
            queryset = Province.objects.order_by('id')
        else:
            for i in range(0, len(province_id)):
                province_id[i] = int(province_id[i])
                queryset = Province.objects.filter(id__in=province_id).order_by('id')

        return queryset


class DistrictViewSet(viewsets.ModelViewSet):
    serializer_class = DistrictSerializer

    def get_queryset(self):
        print(self.request.POST.getlist('id'))
        province_id = self.request.POST.getlist('id')
        if province_id[0] == '0':
            queryset = District.objects.order_by('id')
        else:
            for i in range(0, len(province_id)):
                province_id[i] = int(province_id[i])
                queryset = District.objects.filter(province_id__in=province_id).order_by('id')

        return queryset


class MunicipalityViewSet(viewsets.ModelViewSet):
    serializer_class = MunicipalitySerializer

    def get_queryset(self):
        print(self.request.POST.getlist('id'))
        dist_id = self.request.POST.getlist('id')
        if dist_id[0] == '0':
            queryset = Municipality.objects.order_by('id')
        else:
            for i in range(0, len(dist_id)):
                dist_id[i] = int(dist_id[i])
                queryset = Municipality.objects.filter(district_id__in=dist_id).order_by('id')

        return queryset


class UserPermission(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = True

    def list(self, request, **kwargs):
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

            category = {
                'id': cat.id,
                'name': cat.name,
                'title': cat.title,

            }

            log_subcat = LogSubCategory.objects.filter(category__id=cat.id).order_by('id')

            for sub_cat in log_subcat:

                log_data = LogData.objects.filter(sub_category__id=sub_cat.id).order_by('id')
                sub_category = {
                    'id': sub_cat.id,
                    'name': sub_cat.name,
                    'title': sub_cat.title,
                    'category': sub_cat.category.id,
                    'description': sub_cat.description
                }

                for frame in log_data:

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


class AutomationDataAll(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = True

    def list(self, request, **kwargs):
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        group = Group.objects.get(user=user)
        data = []
        total_data = []
        partner = AutomationPartner.objects.order_by('id')
        total_beneficiary = partner.aggregate(
            Sum('beneficiary'))
        tablet_total = 0
        branch_total = 0
        for part in partner:
            automation = Automation.objects.filter(partner__id=part.id)
            tablet_sum = automation.aggregate(
                Sum('num_tablet_deployed'))
            dist_cov = automation.distinct('district_id').count()
            prov_cov = automation.distinct('province_id').count()
            mun_cov = automation.distinct('municipality_id').count()
            branch = automation.count()
            tablet_total = tablet_sum['num_tablet_deployed__sum'] + tablet_total
            branch_total = branch + branch_total
            data.append({
                'id': part.id,
                'partner_id': part.partner.id,
                'partner_name': part.partner.name,
                'district_covered': dist_cov,
                'province_covered': prov_cov,
                'municipality_covered': mun_cov,
                'branch': branch,
                'beneficiary': part.beneficiary,
                'lat': part.latitude,
                'long': part.longitude,
                'tablets_deployed': tablet_sum['num_tablet_deployed__sum'],
            })

        total_data.append({
            'total_tablet': tablet_total,
            'total_branch': branch_total,
            'total_partner': partner.count(),
            'total_beneficiary': total_beneficiary['beneficiary__sum'],
            'partner_data': data,

        })

        return Response(total_data)


class AutomationDataPartner(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = True

    def list(self, request, **kwargs):
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        group = Group.objects.get(user=user)
        data = []
        total_data = []
        filter_type = request.GET['filter_type']
        if filter_type == 'partner':
            partners_id = request.GET.getlist('partner')
            for i in range(0, len(partners_id)):
                partners_id[i] = int(partners_id[i])
        else:
            prov_id = request.GET.getlist('province')
            dist_id = request.GET.getlist('district')
            mun_id = request.GET.getlist('municipality')
            if prov_id:
                for i in range(0, len(prov_id)):
                    prov_id[i] = int(prov_id[i])
                partners_id = Automation.objects.values_list('partner__partner__id', flat=True).filter(
                    province_id__in=prov_id).distinct('partner')
            if dist_id:
                for i in range(0, len(dist_id)):
                    dist_id[i] = int(dist_id[i])
                partners_id = Automation.objects.values_list('partner__partner__id', flat=True).filter(
                    district_id__in=dist_id).distinct('partner')
            if mun_id:
                for i in range(0, len(mun_id)):
                    mun_id[i] = int(mun_id[i])
                partners_id = Automation.objects.values_list('partner__partner__id', flat=True).filter(
                    municipality_id__in=mun_id).distinct('partner')

        partner = AutomationPartner.objects.filter(partner__in=partners_id).order_by('id')
        total_beneficiary = partner.aggregate(
            Sum('beneficiary'))
        tablet_total = 0
        branch_total = 0
        for part in partner:
            if filter_type == 'partner':
                automation = Automation.objects.filter(partner__id=part.id)
            else:
                if prov_id:
                    automation = Automation.objects.filter(partner__id=part.id).filter(
                        province_id__in=prov_id)
                if dist_id:
                    automation = Automation.objects.filter(partner__id=part.id).filter(
                        district_id__in=dist_id)
                if mun_id:
                    automation = Automation.objects.filter(partner__id=part.id).filter(
                        municipality_id__in=mun_id)

            tablet_sum = automation.aggregate(
                Sum('num_tablet_deployed'))
            dist_cov = automation.distinct('district_id').count()
            prov_cov = automation.distinct('province_id').count()
            mun_cov = automation.distinct('municipality_id').count()
            branch = automation.count()
            tablet_total = tablet_sum['num_tablet_deployed__sum'] + tablet_total
            branch_total = branch + branch_total
            data.append({
                'id': part.id,
                'partner_id': part.partner.id,
                'partner_name': part.partner.name,
                'district_covered': dist_cov,
                'province_covered': prov_cov,
                'municipality_covered': mun_cov,
                'branch': branch,
                'beneficiary': part.beneficiary,
                'lat': part.latitude,
                'long': part.longitude,
                'tablets_deployed': tablet_sum['num_tablet_deployed__sum'],
            })

        total_data.append({
            'total_tablet': tablet_total,
            'total_branch': branch_total,
            'total_partner': partner.count(),
            'total_beneficiary': total_beneficiary['beneficiary__sum'],
            'partner_data': data,

        })

        return Response(total_data)


class AutomationDataMap(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = True

    def list(self, request, **kwargs):
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        group = Group.objects.get(user=user)
        data = []
        partners_id = request.GET.getlist('partner')
        prov_id = request.GET.getlist('province')
        dist_id = request.GET.getlist('district')
        mun_id = request.GET.getlist('municipality')

        if partners_id[0] == '0':
            partner = AutomationPartner.objects.values_list('partner__id', flat=True).order_by('id')

        else:
            for i in range(0, len(partners_id)):
                partners_id[i] = int(partners_id[i])
                partner = AutomationPartner.objects.values_list('partner__id', flat=True).filter(
                    partner__id__in=partners_id).order_by('id')

        if prov_id:
            if prov_id[0] == '0':
                prov_data = Province.objects.order_by('id')
                for provi in prov_data:
                    map_data = Automation.objects.filter(province_id=provi.id).filter(
                        partner__partner__id__in=partner).order_by('id')
                    tablet_sum = map_data.aggregate(Sum('num_tablet_deployed'))
                    data.append({
                        'id': provi.id,
                        'name': provi.name,
                        'code': provi.code,
                        'tablets_deployed': tablet_sum['num_tablet_deployed__sum'],
                    })
            else:
                for i in range(0, len(prov_id)):
                    prov_id[i] = int(prov_id[i])
                    map_data = Automation.objects.filter(province_id=int(prov_id[i])).filter(
                        partner__partner__id__in=partner).order_by('id')
                    tablet_sum = map_data.aggregate(Sum('num_tablet_deployed'))
                    prov_data = Province.objects.get(id=int(prov_id[i]))
                    print(json.loads(serialize('json', map_data)))
                    data.append({
                        'id': prov_data.id,
                        'name': prov_data.name,
                        'code': prov_data.code,
                        'tablets_deployed': tablet_sum['num_tablet_deployed__sum'],
                        'tb_data': json.loads(serialize('json', map_data)),
                    })

        if dist_id:
            if dist_id[0] == '0':
                dist_data = District.objects.values('id', 'name', 'n_code').order_by('id')
                for dist in dist_data:
                    map_data = Automation.objects.filter(district_id=dist['id']).filter(
                        partner__partner__id__in=partner).order_by('id')
                    tablet_sum = map_data.aggregate(Sum('num_tablet_deployed'))
                    data.append({
                        'id': dist['id'],
                        'name': dist['name'],
                        'code': dist['n_code'],
                        'tablets_deployed': tablet_sum['num_tablet_deployed__sum'],
                    })
            else:
                for i in range(0, len(dist_id)):
                    dist_id[i] = int(dist_id[i])
                    map_data = Automation.objects.filter(district_id=int(dist_id[i])).filter(
                        partner__partner__id__in=partner).order_by('id')
                    tablet_sum = map_data.aggregate(Sum('num_tablet_deployed'))
                    dist_data = District.objects.values('id', 'name', 'n_code').get(id=int(dist_id[i]))
                    data.append({
                        'id': dist_data['id'],
                        'name': dist_data['name'],
                        'code': dist_data['n_code'],
                        'tablets_deployed': tablet_sum['num_tablet_deployed__sum'],
                    })
        if mun_id:
            if mun_id[0] == '0':
                mun_data = Municipality.objects.values('id', 'name', 'code').order_by('id')
                for mun in mun_data:
                    map_data = Automation.objects.filter(municipality_id=mun['id']).filter(
                        partner__partner__id__in=partner).order_by('id')
                    tablet_sum = map_data.aggregate(Sum('num_tablet_deployed'))
                    data.append({
                        'id': mun['id'],
                        'name': mun['name'],
                        'code': mun['code'],
                        'tablets_deployed': tablet_sum['num_tablet_deployed__sum'],
                    })
            else:
                for i in range(0, len(mun_id)):
                    mun_id[i] = int(mun_id[i])
                    map_data = Automation.objects.filter(municipality_id=int(mun_id[i])).filter(
                        partner__partner__id__in=partner).order_by('id')
                    tablet_sum = map_data.aggregate(Sum('num_tablet_deployed'))
                    mun_data = Municipality.objects.values('id', 'name', 'code').get(id=int(mun_id[i]))
                    data.append({
                        'id': mun_data['id'],
                        'name': mun_data['name'],
                        'code': mun_data['code'],
                        'tablets_deployed': tablet_sum['num_tablet_deployed__sum'],
                    })

        return Response(data)
