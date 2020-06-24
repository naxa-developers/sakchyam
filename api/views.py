from rest_framework import viewsets
from api.models import LogCategory, LogSubCategory, MilestoneYear, LogData, Province, District, Municipality, \
    Automation, Partner, AutomationPartner, FinancialProgram, FinancialLiteracy, Project, Partnership
from api.serializers import LogCategorySerializer, LogSubCategorySerializer, LogDataSerializer, MilestoneYearSerializer, \
    LogDataAlternativeSerializer, ProvinceSerializer, DistrictSerializer, MunicipalitySerializer, AutomationSerializer, \
    FinancialProgramSerializer, FinancialLiteracySerializer, FinancialPartnerSerializer, ProjectSerializer, \
    PartnerSerializer, PartnershipSerializer, InvestmentSerializer

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


class FinancialProgramApi(viewsets.ModelViewSet):
    serializer_class = FinancialProgramSerializer
    queryset = FinancialProgram.objects.all()
    permission_classes = [IsAuthenticated, ]


class FinancialLiteracyApi(viewsets.ModelViewSet):
    serializer_class = FinancialLiteracySerializer
    queryset = FinancialLiteracy.objects.all()
    permission_classes = [IsAuthenticated, ]


class FinancialPartnerApi(viewsets.ModelViewSet):
    serializer_class = FinancialPartnerSerializer
    queryset = FinancialLiteracy.objects.distinct('partner_id')
    permission_classes = [IsAuthenticated, ]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['partner_type', ]


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


class ProjectApi(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'name', 'code', 'investment_primary', 'investment_secondary', ]

    def get_queryset(self):
        filter_data = self.request.data
        investment = filter_data['investment_primary']

        # for i in range(0, len(id_indicator)):
        #     id_indicator[i] = int(id_indicator[i])
        if investment:
            queryset = Project.objects.filter(investment_primary__in=investment).order_by('id')
        else:
            queryset = Project.objects.order_by('id')

        return queryset

    def get_serializer_class(self):
        serializer_class = ProjectSerializer
        return serializer_class


class InvestmentApi(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'investment_primary', ]

    def get_queryset(self):
        queryset = Project.objects.distinct('investment_primary')

        return queryset

    def get_serializer_class(self):
        serializer_class = InvestmentSerializer
        return serializer_class


class PartnerApi(viewsets.ModelViewSet):
    serializer_class = PartnerSerializer
    queryset = Partner.objects.order_by('id')
    permission_classes = [IsAuthenticated, ]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'name', 'code', 'type', ]


class PartnershipApi(viewsets.ModelViewSet):
    serializer_class = PartnershipSerializer
    queryset = Partnership.objects.order_by('id')
    permission_classes = [IsAuthenticated, ]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'partner_id', 'partner_id__name', 'partner_id__type', 'project_id',
                        'project_id__investment_primary']


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


class AutomationTimeline(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = True

    def list(self, request, **kwargs):
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        group = Group.objects.get(user=user)
        year = [d.year for d in AutomationPartner.objects.all().dates('date', 'year')]
        print(year)
        year_data = []

        for i in range(0, len(year)):
            date_t = AutomationPartner.objects.filter(date__year=year[i])
            print(date_t)
            partner_data = []
            for t in date_t:
                partner_data.append({
                    'id': t.id,
                    'partner_name': t.partner.name,
                    'partner_id': t.partner.id,
                    'latitude': t.latitude,
                    'longitude': t.longitude,
                })

            year_data.append({
                year[i]: partner_data
            })
        user_info = [{
            "year": year,
            "timeline": year_data,
            # "email": user_data.email,
            # "image": user_data.thumbnail.url,
            # "permission": permission,

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
                'full_data': part.date,
                'date_year': part.date.year,
                'date_month_name': part.date.strftime('%B'),
                'date_day': part.date.day,
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
        partners_id = request.GET.getlist('partner')
        prov_id = request.GET.getlist('province')
        dist_id = request.GET.getlist('district')
        mun_id = request.GET.getlist('municipality')
        if filter_type == 'partner':
            for i in range(0, len(partners_id)):
                partners_id[i] = int(partners_id[i])
        else:
            if prov_id:
                for i in range(0, len(prov_id)):
                    prov_id[i] = int(prov_id[i])
                partners_id = Automation.objects.values_list('partner__partner__id', flat=True).filter(
                    province_id__code__in=prov_id).distinct('partner')
            if dist_id:
                for i in range(0, len(dist_id)):
                    dist_id[i] = int(dist_id[i])
                partners_id = Automation.objects.values_list('partner__partner__id', flat=True).filter(
                    district_id__code__in=dist_id).distinct('partner')
            if mun_id:
                for i in range(0, len(mun_id)):
                    mun_id[i] = int(mun_id[i])
                print(mun_id)
                partners_id = Automation.objects.values_list('partner__partner__id', flat=True).filter(
                    municipality_id__code__in=mun_id).distinct('partner')

        partner = AutomationPartner.objects.filter(partner__in=partners_id).order_by('id')
        total_beneficiary = partner.aggregate(
            Sum('beneficiary'))
        tablet_total = 0
        branch_total = 0
        for part in partner:
            if filter_type == 'partner':
                automation = Automation.objects.filter(partner__id=part.id)
                if prov_id:
                    automation = Automation.objects.filter(partner__id=part.id).filter(
                        province_id__code__in=prov_id)
                if dist_id:
                    automation = Automation.objects.filter(partner__id=part.id).filter(
                        district_id__code__in=dist_id)
                if mun_id:
                    automation = Automation.objects.filter(partner__id=part.id).filter(
                        municipality_id__code__in=mun_id)
            else:
                if prov_id:
                    automation = Automation.objects.filter(partner__id=part.id).filter(
                        province_id__code__in=prov_id)
                if dist_id:
                    automation = Automation.objects.filter(partner__id=part.id).filter(
                        district_id__code__in=dist_id)
                if mun_id:
                    automation = Automation.objects.filter(partner__id=part.id).filter(
                        municipality_id__code__in=mun_id)

            if automation:
                tablet_sum = automation.aggregate(
                    Sum('num_tablet_deployed'))
                tablet = tablet_sum['num_tablet_deployed__sum']
            else:
                tablet = 0
            dist_cov = automation.distinct('district_id').count()
            prov_cov = automation.distinct('province_id').count()
            mun_cov = automation.distinct('municipality_id').count()
            branch = automation.count()
            tablet_total = tablet + tablet_total
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
                'tablets_deployed': tablet,
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
                    map_data = Automation.objects.filter(province_id__code=int(prov_id[i])).filter(
                        partner__partner__id__in=partner).order_by('id')
                    tablet_sum = map_data.aggregate(Sum('num_tablet_deployed'))
                    prov_data = Province.objects.get(code=int(prov_id[i]))
                    # print(json.loads(serialize('json', map_data)))
                    data.append({
                        'id': prov_data.id,
                        'name': prov_data.name,
                        'code': prov_data.code,
                        'tablets_deployed': tablet_sum['num_tablet_deployed__sum'],
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
                    map_data = Automation.objects.filter(district_id__code=int(dist_id[i])).filter(
                        partner__partner__id__in=partner).order_by('id')
                    tablet_sum = map_data.aggregate(Sum('num_tablet_deployed'))
                    dist_data = District.objects.values('id', 'name', 'n_code').get(code=int(dist_id[i]))
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
                    if map_data:
                        data.append({
                            'id': mun['id'],
                            'name': mun['name'],
                            'code': mun['code'],
                            'tablets_deployed': tablet_sum['num_tablet_deployed__sum'],
                        })

                    else:
                        print('a')
                        data.append({
                            'id': mun['id'],
                            'name': mun['name'],
                            'code': mun['code'],
                            'tablets_deployed': 0,
                        })
            else:
                for i in range(0, len(mun_id)):
                    mun_id[i] = int(mun_id[i])
                    map_data = Automation.objects.filter(municipality_id__code=int(mun_id[i])).filter(
                        partner__partner__id__in=partner).order_by('id')
                    tablet_sum = map_data.aggregate(Sum('num_tablet_deployed'))
                    mun_data = Municipality.objects.values('id', 'name', 'code').get(code=int(mun_id[i]))
                    data.append({
                        'id': mun_data['id'],
                        'name': mun_data['name'],
                        'code': mun_data['code'],
                        'tablets_deployed': tablet_sum['num_tablet_deployed__sum'],
                    })

        return Response(data)


class AutomationDataTable(viewsets.ModelViewSet):
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
                prov_data = Province.objects.values_list('id', flat=True).order_by('id')
                map_data = Automation.objects.only('id').filter(province_id__in=prov_data).filter(
                    partner__partner__id__in=partner).order_by('id')
                for m in map_data:
                    data.append({
                        'id': m.id,
                        'partner': m.partner.partner.name,
                        'partner_id': m.partner.partner.id,
                        'branch': m.branch,
                        'province': m.province_id.name,
                        'province_code': m.province_id.code,
                        'district': m.district_id.name,
                        'district_code': m.district_id.code,
                        'municipality': m.municipality_id.name,
                        'municipality_code': m.municipality_id.code,
                        'tablets': m.num_tablet_deployed,
                        'latitude': m.partner.latitude,
                        'longitude': m.partner.longitude,

                    })
            else:
                for i in range(0, len(prov_id)):
                    prov_id[i] = int(prov_id[i])
                map_data = Automation.objects.filter(province_id__code__in=prov_id).filter(
                    partner__partner__id__in=partner).order_by('id')

                for m in map_data:
                    data.append({
                        'id': m.id,
                        'partner': m.partner.partner.name,
                        'partner_id': m.partner.partner.id,
                        'branch': m.branch,
                        'province': m.province_id.name,
                        'province_code': m.province_id.code,
                        'district': m.district_id.name,
                        'district_code': m.district_id.code,
                        'municipality': m.municipality_id.name,
                        'municipality_code': m.municipality_id.code,
                        'tablets': m.num_tablet_deployed,
                        'latitude': m.partner.latitude,
                        'longitude': m.partner.longitude,

                    })

        if dist_id:
            if dist_id[0] == '0':
                dist_data = District.objects.values_list('id', flat=True).order_by('id')
                map_data = Automation.objects.filter(district_id__in=dist_data).filter(
                    partner__partner__id__in=partner).order_by('id')
                for m in map_data:
                    data.append({
                        'id': m.id,
                        'partner': m.partner.partner.name,
                        'partner_id': m.partner.partner.id,
                        'branch': m.branch,
                        'province': m.province_id.name,
                        'province_code': m.province_id.code,
                        'district': m.district_id.name,
                        'district_code': m.district_id.code,
                        'municipality': m.municipality_id.name,
                        'municipality_code': m.municipality_id.code,
                        'tablets': m.num_tablet_deployed,
                        'latitude': m.partner.latitude,
                        'longitude': m.partner.longitude,

                    })

            else:
                for i in range(0, len(dist_id)):
                    dist_id[i] = int(dist_id[i])
                print(dist_id)
                map_data = Automation.objects.filter(district_id__code__in=dist_id).filter(
                    partner__partner__id__in=partner).order_by('id')
                print(map_data)
                for m in map_data:
                    data.append({
                        'id': m.id,
                        'partner': m.partner.partner.name,
                        'partner_id': m.partner.partner.id,
                        'branch': m.branch,
                        'province': m.province_id.name,
                        'province_code': m.province_id.code,
                        'district': m.district_id.name,
                        'district_code': m.district_id.code,
                        'municipality': m.municipality_id.name,
                        'municipality_code': m.municipality_id.code,
                        'tablets': m.num_tablet_deployed,
                        'latitude': m.partner.latitude,
                        'longitude': m.partner.longitude,

                    })
        if mun_id:
            if mun_id[0] == '0':
                mun_data = Municipality.objects.values_list('id', flat=True).order_by('id')
                map_data = Automation.objects.filter(municipality_id__in=mun_data).filter(
                    partner__partner__id__in=partner).order_by('id')
                for m in map_data:
                    data.append({
                        'id': m.id,
                        'partner': m.partner.partner.name,
                        'partner_id': m.partner.partner.id,
                        'branch': m.branch,
                        'province': m.province_id.name,
                        'province_code': m.province_id.code,
                        'district': m.district_id.name,
                        'district_code': m.district_id.code,
                        'municipality': m.municipality_id.name,
                        'municipality_code': m.municipality_id.code,
                        'tablets': m.num_tablet_deployed,
                        'latitude': m.partner.latitude,
                        'longitude': m.partner.longitude,

                    })
            else:
                for i in range(0, len(mun_id)):
                    mun_id[i] = int(mun_id[i])
                map_data = Automation.objects.filter(municipality_id__code__in=mun_id).filter(
                    partner__partner__id__in=partner).order_by('id')

                for m in map_data:
                    data.append({
                        'id': m.id,
                        'partner': m.partner.partner.name,
                        'partner_id': m.partner.partner.id,
                        'branch': m.branch,
                        'province': m.province_id.name,
                        'province_code': m.province_id.code,
                        'district': m.district_id.name,
                        'district_code': m.district_id.code,
                        'municipality': m.municipality_id.name,
                        'municipality_code': m.municipality_id.code,
                        'tablets': m.num_tablet_deployed,
                        'latitude': m.partner.latitude,
                        'longitude': m.partner.longitude,

                    })

        return Response(data)


class PartnershipFilter(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = True
    serializer_class = PartnershipSerializer

    def list(self, request, **kwargs):
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        group = Group.objects.get(user=user)
        data = []
        filter_data = request.data
        prov_id = filter_data['province_id']
        dist_id = filter_data['district_id']
        mun_id = filter_data['municipality_id']
        project_id = filter_data['project_id']
        partner_id = filter_data['partner_id']
        view = filter_data['view']
        status = filter_data['status']
        if partner_id:
            if partner_id[0] == 0:
                partner = Partner.objects.values_list('id', flat=True).order_by('id')
            else:
                partner = partner_id

        if project_id:
            if project_id[0] == 0:
                project = Project.objects.values_list('id', flat=True).order_by('id')
            else:
                project = project_id

        if prov_id:
            if prov_id[0] == 0:
                prov_data = Province.objects.order_by('id')
                for provi in prov_data:
                    if status:
                        map_data = Partnership.objects.filter(province_id=provi.id).filter(
                            partner_id__in=partner, project_id__in=project, status=status).order_by('id')
                    else:
                        map_data = Partnership.objects.filter(province_id=provi.id).filter(
                            partner_id__in=partner, project_id__in=project).order_by('id')

                    if map_data:
                        count_data = map_data.aggregate(Sum(view))
                        total = count_data[view + '__sum']
                    else:
                        total = 0
                    data.append({
                        'id': provi.id,
                        'name': provi.name,
                        'code': provi.code,
                        view: total,
                    })
            else:
                for i in range(0, len(prov_id)):
                    prov_id[i] = int(prov_id[i])
                    if status:
                        map_data = Partnership.objects.filter(province_id=prov_id[i]).filter(
                            partner_id__in=partner, project_id__in=project, status=status).order_by('id')
                    else:
                        map_data = Partnership.objects.filter(province_id=prov_id[i]).filter(
                            partner_id__in=partner, project_id__in=project).order_by('id')

                    if map_data:
                        count_data = map_data.aggregate(Sum(view))
                        total = count_data[view + '__sum']
                    else:
                        total = 0
                    prov_data = Province.objects.get(code=int(prov_id[i]))
                    # print(json.loads(serialize('json', map_data)))
                    data.append({
                        'id': prov_data.id,
                        'name': prov_data.name,
                        'code': prov_data.code,
                        view: total,
                    })

        if dist_id:
            if dist_id[0] == 0:
                dist_data = District.objects.values('id', 'name', 'n_code').order_by('id')
                for dist in dist_data:
                    if status:
                        map_data = Partnership.objects.filter(district_id=dist['id']).filter(
                            partner_id__in=partner, project_id__in=project, status=status).order_by('id')
                    else:
                        map_data = Partnership.objects.filter(district_id=dist['id']).filter(
                            partner_id__in=partner, project_id__in=project).order_by('id')

                    if map_data:
                        count_data = map_data.aggregate(Sum(view))
                        total = count_data[view + '__sum']
                    else:
                        total = 0

                    data.append({
                        'id': dist['id'],
                        'name': dist['name'],
                        'code': dist['n_code'],
                        view: total,
                    })
            else:
                for i in range(0, len(dist_id)):
                    dist_id[i] = int(dist_id[i])
                    if status:
                        map_data = Partnership.objects.filter(district_id__n_code=dist_id[i]).filter(
                            partner_id__in=partner, project_id__in=project, status=status).order_by('id')
                    else:
                        map_data = Partnership.objects.filter(district_id__n_code=dist_id[i]).filter(
                            partner_id__in=partner, project_id__in=project).order_by('id')

                    if map_data:
                        count_data = map_data.aggregate(Sum(view))
                        total = count_data[view + '__sum']
                    else:
                        total = 0
                    dist_data = District.objects.values('id', 'name', 'n_code').get(n_code=int(dist_id[i]))
                    data.append({
                        'id': dist_data['id'],
                        'name': dist_data['name'],
                        'code': dist_data['n_code'],
                        view: total,
                    })
        if mun_id:
            if mun_id[0] == 0:
                mun_data = Municipality.objects.values('id', 'name', 'code').order_by('id')
                for mun in mun_data:
                    if status:
                        map_data = Partnership.objects.filter(municipality_id=mun['id']).filter(
                            partner_id__in=partner, project_id__in=project, status=status).order_by('id')
                    else:
                        map_data = Partnership.objects.filter(municipality_id=mun['id']).filter(
                            partner_id__in=partner, project_id__in=project).order_by('id')

                    if map_data:
                        count_data = map_data.aggregate(Sum(view))
                        total = count_data[view + '__sum']
                    else:
                        total = 0

                    data.append({
                        'id': mun['id'],
                        'name': mun['name'],
                        'code': mun['code'],
                        view: total,
                    })
            else:
                for i in range(0, len(mun_id)):
                    mun_id[i] = int(mun_id[i])
                    if status:
                        map_data = Partnership.objects.filter(municipality_id__code=mun_id[i]).filter(
                            partner_id__in=partner, project_id__in=project, status=status).order_by('id')
                    else:
                        map_data = Partnership.objects.filter(municipality_id__code=mun_id[i]).filter(
                            partner_id__in=partner, project_id__in=project).order_by('id')

                    if map_data:
                        count_data = map_data.aggregate(Sum(view))
                        total = count_data[view + '__sum']
                    else:
                        total = 0

                    mun_data = Municipality.objects.values('id', 'name', 'code').get(code=int(mun_id[i]))
                    data.append({
                        'id': mun_data['id'],
                        'name': mun_data['name'],
                        'code': mun_data['code'],
                        view: total,
                    })

        return Response(data)


class PartnershipRadial(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = True

    def list(self, request, **kwargs):
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        group = Group.objects.get(user=user)
        investment = []

        if request.GET.getlist('province_id'):
            province_get = request.GET['province_id']
            province_filter_list = province_get.split(",")
            for i in range(0, len(province_filter_list)):
                province_filter_list[i] = int(province_filter_list[i])

        else:
            province_filter_list = list(Province.objects.values_list('id', flat=True).distinct())

        if request.GET.getlist('district_id'):
            district_get = request.GET['district_id']
            district_filter_list = district_get.split(",")
            for i in range(0, len(district_filter_list)):
                district_filter_list[i] = int(district_filter_list[i])

        else:
            district_filter_list = list(District.objects.values_list('id', flat=True).distinct())

        if request.GET.getlist('municipality_id'):
            municipality_get = request.GET['municipality_id']
            municipality_filter_list = municipality_get.split(",")
            for i in range(0, len(municipality_filter_list)):
                municipality_filter_list[i] = int(municipality_filter_list[i])

        else:
            municipality_filter_list = list(Municipality.objects.values_list('id', flat=True).distinct())

        if request.GET.getlist('view'):
            view = request.GET['view']
        else:
            view = 'allocated_budget'

        if request.GET.getlist('investment_filter'):
            investment_get = request.GET['investment_filter']
            investment_list = investment_get.split(",")
            # for i in range(0, len(investment_filter_id)):
            #     investment_filter_id[i] = int(investment_filter_id[i])
            investment_list = list(
                Project.objects.filter(investment_primary__in=investment_list).values_list('investment_primary',
                                                                                           flat=True).distinct())
        else:
            investment_list = list(Project.objects.values_list('investment_primary', flat=True).distinct())

        if request.GET.getlist('partner_type_filter'):
            partner_type_get = request.GET['partner_type_filter']
            partner_types = partner_type_get.split(",")
            partner_types = list(
                Partner.objects.filter(type__in=partner_types).values_list('type', flat=True).distinct())

        else:
            partner_types = list(Partner.objects.values_list('type', flat=True).distinct())

        if request.GET.getlist('partner_filter'):
            partner_get = request.GET['partner_filter']
            partner_filter_list = partner_get.split(",")
            for i in range(0, len(partner_filter_list)):
                partner_filter_list[i] = int(partner_filter_list[i])
            partner_filter_list = list(
                Partner.objects.filter(id__in=partner_filter_list).values_list('id', flat=True).distinct())

        else:
            partner_filter_list = list(Partner.objects.values_list('id', flat=True).distinct())

        if request.GET.getlist('project_filter'):
            project_get = request.GET['project_filter']
            project_filter_list = project_get.split(",")
            for i in range(0, len(project_filter_list)):
                project_filter_list[i] = int(project_filter_list[i])
            project_filter_list = list(
                Project.objects.filter(id__in=project_filter_list).values_list('id', flat=True).distinct())

        else:
            project_filter_list = list(Project.objects.values_list('id', flat=True).distinct())

        partnership_query = Partnership.objects.filter(province_id__in=province_filter_list,
                                                       district_id__in=district_filter_list,
                                                       municipality_id__in=municipality_filter_list,
                                                       )
        for i in range(0, len(investment_list)):
            invest_query = partnership_query.filter(project_id__investment_primary=investment_list[i])
            invest_val = invest_query.aggregate(Sum(view))
            total = invest_val[view + '__sum']
            partner_type = []
            for x in range(0, len(partner_types)):
                p_type = invest_query.filter(partner_id__type=partner_types[x])
                p_type_list = list(
                    p_type.filter(partner_id__in=partner_filter_list).values_list('partner_id', flat=True).distinct(
                        'partner_id'))
                p_data = []
                if p_type_list:
                    for y in range(0, len(p_type_list)):
                        partner_q = p_type.filter(partner_id=int(p_type_list[y]))
                        project_list = partner_q.filter(project_id__in=project_filter_list).values_list('project_id',
                                                                                                        flat=True).distinct(
                            'project_id')

                        partner_data = []
                        for z in range(0, len(project_list)):
                            project_q = partner_q.filter(project_id=int(project_list[z]))
                            project_count = project_q.aggregate(Sum(view))
                            total_pro_b = project_count[view + '__sum']
                            partner_data.append({
                                "name": project_q[0].project_id.name,
                                "size": total_pro_b,

                            })

                        if partner_q:
                            partner_count = partner_q.aggregate(Sum(view))
                            total_p_b = partner_count[view + '__sum']
                            p_data.append({
                                "name": partner_q[0].partner_id.name,
                                "size": total_p_b,
                                "children": partner_data,

                            })
                if p_type:
                    part_count = p_type.aggregate(Sum(view))
                    total_part = part_count[view + '__sum']
                    partner_type.append({
                        "name": partner_types[x],
                        "size": total_part,
                        "children": p_data,

                    })

            investment.append({
                "name": investment_list[i],
                "size": total,
                "children": partner_type
            })

        overall = partnership_query.aggregate(Sum(view))[view + '__sum']
        return Response({"name": "Partnership", "size": overall, "children": investment})


class PartnershipRadar(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = True

    def list(self, request, **kwargs):
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        group = Group.objects.get(user=user)
        view = 'allocated_budget'
        investment = []
        if request.GET.getlist('investment_filter'):
            investment_get = request.GET['investment_filter']
            investment_list = investment_get.split(",")
            # for i in range(0, len(investment_filter_id)):
            #     investment_filter_id[i] = int(investment_filter_id[i])
            investment_list = list(
                Project.objects.filter(investment_primary__in=investment_list).values_list('investment_primary',
                                                                                           flat=True).distinct())
        else:
            investment_list = list(Project.objects.values_list('investment_primary', flat=True).distinct())

        total_invest = Partnership.objects.values('id', 'branch', 'blb', 'extension_counter', 'tablet')
        total_invest_branch = total_invest.aggregate(Sum('branch'))['branch__sum']
        total_invest_blb = total_invest.aggregate(Sum('blb'))['blb__sum']
        total_invest_extension_counter = total_invest.aggregate(Sum('extension_counter'))['extension_counter__sum']
        total_invest_tablet = total_invest.aggregate(Sum('tablet'))['tablet__sum']

        for i in range(0, len(investment_list)):
            invest_query = Partnership.objects.values('id', 'branch', 'blb', 'extension_counter', 'tablet',
                                                      'project_id__investment_primary').filter(
                project_id__investment_primary=investment_list[i])
            invest_branch = invest_query.aggregate(Sum('branch'))['branch__sum']
            invest_blb = invest_query.aggregate(Sum('blb'))['blb__sum']
            invest_extension_counter = invest_query.aggregate(Sum('extension_counter'))['extension_counter__sum']
            invest_tablet = invest_query.aggregate(Sum('tablet'))['tablet__sum']

            percentage_branch = float((invest_branch / total_invest_branch) * 100)
            percentage_blb = float((invest_blb / total_invest_blb) * 100)
            percentage_extension_counter = float((invest_extension_counter / total_invest_extension_counter) * 100)
            percentage_tablet = float((invest_tablet / total_invest_tablet) * 100)
            data = list([percentage_branch, percentage_blb, percentage_extension_counter, percentage_tablet])
            investment.append({
                'name': invest_query[0]['project_id__investment_primary'],
                'data': data,
            })

        return Response(investment)


class InvestmentSankey(viewsets.ModelViewSet):
    queryset = True
    serializer_class = PartnershipSerializer

    def list(self, request, *args, **kwargs):
        node = []
        links = []
        investment_id = []
        project_id = []
        partner_id = []
        partner_id_t = []

        if request.GET.getlist('view'):
            view = request.GET['view']
        else:
            view = 'allocated_budget'

        if request.GET.getlist('province_id'):
            province_get = request.GET['province_id']
            province_filter_list = province_get.split(",")
            for i in range(0, len(province_filter_list)):
                province_filter_list[i] = int(province_filter_list[i])

        else:
            province_filter_list = list(Province.objects.values_list('id', flat=True).distinct())

        if request.GET.getlist('district_id'):
            district_get = request.GET['district_id']
            district_filter_list = district_get.split(",")
            for i in range(0, len(district_filter_list)):
                district_filter_list[i] = int(district_filter_list[i])

        else:
            district_filter_list = list(District.objects.values_list('id', flat=True).distinct())

        if request.GET.getlist('municipality_id'):
            municipality_get = request.GET['municipality_id']
            municipality_filter_list = municipality_get.split(",")
            for i in range(0, len(municipality_filter_list)):
                municipality_filter_list[i] = int(municipality_filter_list[i])

        else:
            municipality_filter_list = list(Municipality.objects.values_list('id', flat=True).distinct())

        if request.GET.getlist('partner_type_filter'):
            partner_type_get = request.GET['partner_type_filter']
            partner_types = partner_type_get.split(",")
            partner_types = list(
                Partner.objects.filter(type__in=partner_types).values_list('type', flat=True).distinct())

        else:
            partner_types = list(Partner.objects.values_list('type', flat=True).distinct())

        if request.GET.getlist('partner_filter'):
            partner_get = request.GET['partner_filter']
            partner_filter_list = partner_get.split(",")
            for i in range(0, len(partner_filter_list)):
                partner_filter_list[i] = int(partner_filter_list[i])
            partner_filter_list = list(
                Partner.objects.filter(id__in=partner_filter_list).values_list('id', flat=True).distinct())

        else:
            partner_filter_list = list(Partner.objects.values_list('id', flat=True).distinct())

        if request.GET.getlist('project_filter'):
            project_get = request.GET['project_filter']
            project_filter_list = project_get.split(",")
            for i in range(0, len(project_filter_list)):
                project_filter_list[i] = int(project_filter_list[i])
            project_filter_list = list(
                Project.objects.filter(id__in=project_filter_list).values_list('id', flat=True).distinct())

        else:
            project_filter_list = list(Project.objects.values_list('id', flat=True).distinct())

        if request.GET.getlist('investment_filter'):
            investment_get = request.GET['investment_filter']
            investment_list = investment_get.split(",")
            # for i in range(0, len(investment_filter_id)):
            #     investment_filter_id[i] = int(investment_filter_id[i])
            investment_list = list(
                Project.objects.filter(investment_primary__in=investment_list).values_list('investment_primary',
                                                                                           flat=True).distinct())
        else:
            investment_list = list(Project.objects.values_list('investment_primary', flat=True).distinct())

        partnership_query = Partnership.objects.filter(project_id__investment_primary__in=investment_list,
                                                       project_id__in=project_filter_list,
                                                       partner_id__type__in=partner_types,
                                                       partner_id__in=partner_filter_list,
                                                       province_id__in=province_filter_list,
                                                       district_id__in=district_filter_list,
                                                       municipality_id__in=municipality_filter_list,
                                                       )

        investment = partnership_query.values("project_id__investment_primary").distinct(
            'project_id__investment_primary')

        for p in investment:
            node.append({
                'id': p['project_id__investment_primary'],
                "color": "hsl(2, 70%, 50%)",
                'type': 'investment',
            })
            investment_id.append(p['project_id__investment_primary'])

        project = partnership_query.values("project_id__name", "project_id").distinct('project_id')
        for c in project:
            node.append({
                'id': c['project_id__name'],
                "color": "hsl(205, 70%, 50%)",
                'type': 'project',
            })
            project_id.append(c['project_id'])

        partner_type = partnership_query.values("partner_id", "partner_id__type").distinct('partner_id__type')
        for part_tt in partner_type:
            node.append({
                'id': part_tt['partner_id__type'],
                "color": "hsl(262, 70%, 50%)",
                'type': 'partner_type',
            })
            partner_id_t.append(part_tt['partner_id__type'])

        partner = partnership_query.values("partner_id__name", "partner_id").distinct('partner_id')
        for part in partner:
            node.append({
                'id': part['partner_id__name'],
                "color": "hsl(262, 70%, 50%)",
                'type': 'partner',
            })
            partner_id.append(part['partner_id'])

        for i in range(0, len(project_id)):
            q = partnership_query.values('project_id__investment_primary', 'project_id__name',
                                         'allocated_budget').filter(project_id=project_id[i])
            budget = q.aggregate(Sum(view))
            source = q[0]['project_id__investment_primary']
            target = q[0]['project_id__name']
            links.append({
                'source': source,
                'target': target,
                'value': int(budget[view + '__sum']),
            })

        for x in range(0, len(project_id)):
            q = partnership_query.values('partner_id__type', 'partner_id__name', 'project_id__name', ).filter(
                project_id=project_id[x])

            budget = q.aggregate(Sum(view))
            source = q[0]['project_id__name']
            target = q[0]['partner_id__type']
            links.append({
                'source': source,
                'target': target,
                'value': int(budget[view + '__sum']),
            })

        for x in range(0, len(partner_id)):
            q = partnership_query.values('partner_id', 'partner_id__name', 'partner_id__type', ).filter(
                partner_id=partner_id[x])

            budget = q.aggregate(Sum(view))
            source = q[0]['partner_id__type']
            target = q[0]['partner_id__name']
            links.append({
                'source': source,
                'target': target,
                'value': int(budget[view + '__sum']),
            })

        return Response({"nodes": node, "links": links})


class PartnershipOverview(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = True

    def list(self, request, **kwargs):
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        group = Group.objects.get(user=user)
        investment = []

        if request.GET.getlist('province_id'):
            province_get = request.GET['province_id']
            province_filter_list = province_get.split(",")
            for i in range(0, len(province_filter_list)):
                province_filter_list[i] = int(province_filter_list[i])

        else:
            province_filter_list = list(Province.objects.values_list('id', flat=True).distinct())

        if request.GET.getlist('district_id'):
            district_get = request.GET['district_id']
            district_filter_list = district_get.split(",")
            for i in range(0, len(district_filter_list)):
                district_filter_list[i] = int(district_filter_list[i])

        else:
            district_filter_list = list(District.objects.values_list('id', flat=True).distinct())

        if request.GET.getlist('municipality_id'):
            municipality_get = request.GET['municipality_id']
            municipality_filter_list = municipality_get.split(",")
            for i in range(0, len(municipality_filter_list)):
                municipality_filter_list[i] = int(municipality_filter_list[i])

        else:
            municipality_filter_list = list(Municipality.objects.values_list('id', flat=True).distinct())

        if request.GET.getlist('view'):
            view = request.GET['view']
        else:
            view = 'allocated_budget'

        if request.GET.getlist('investment_filter'):
            investment_get = request.GET['investment_filter']
            investment_list = investment_get.split(",")
            # for i in range(0, len(investment_filter_id)):
            #     investment_filter_id[i] = int(investment_filter_id[i])
            investment_list = list(
                Project.objects.filter(investment_primary__in=investment_list).values_list('investment_primary',
                                                                                           flat=True).distinct())
        else:
            investment_list = list(Project.objects.values_list('investment_primary', flat=True).distinct())

        if request.GET.getlist('partner_type_filter'):
            partner_type_get = request.GET['partner_type_filter']
            partner_types = partner_type_get.split(",")
            partner_types = list(
                Partner.objects.filter(type__in=partner_types).values_list('type', flat=True).distinct())

        else:
            partner_types = list(Partner.objects.values_list('type', flat=True).distinct())

        if request.GET.getlist('partner_filter'):
            partner_get = request.GET['partner_filter']
            partner_filter_list = partner_get.split(",")
            for i in range(0, len(partner_filter_list)):
                partner_filter_list[i] = int(partner_filter_list[i])
            partner_filter_list = list(
                Partner.objects.filter(id__in=partner_filter_list).values_list('id', flat=True).distinct())

        else:
            partner_filter_list = list(Partner.objects.values_list('id', flat=True).distinct())

        if request.GET.getlist('project_filter'):
            project_get = request.GET['project_filter']
            project_filter_list = project_get.split(",")
            for i in range(0, len(project_filter_list)):
                project_filter_list[i] = int(project_filter_list[i])
            project_filter_list = list(
                Project.objects.filter(id__in=project_filter_list).values_list('id', flat=True).distinct())

        else:
            project_filter_list = list(Project.objects.values_list('id', flat=True).distinct())

        partnership_query = Partnership.objects.filter(project_id__investment_primary__in=investment_list,
                                                       project_id__in=project_filter_list,
                                                       partner_id__type__in=partner_types,
                                                       partner_id__in=partner_filter_list,
                                                       province_id__in=province_filter_list,
                                                       district_id__in=district_filter_list,
                                                       municipality_id__in=municipality_filter_list,
                                                       )
        partner = partnership_query.values('partner_id').distinct().count()
        project = partnership_query.values('project_id').distinct().count()
        investment = partnership_query.values('project_id__investment_primary').distinct().count()
        other_products = partnership_query.aggregate(Sum('other_products'))['other_products__sum']
        tablet = partnership_query.aggregate(Sum('tablet'))['tablet__sum']
        branch = partnership_query.aggregate(Sum('branch'))['branch__sum']
        blb = partnership_query.aggregate(Sum('blb'))['blb__sum']
        budget = partnership_query.aggregate(Sum('allocated_budget'))['allocated_budget__sum']
        beneficiary = partnership_query.aggregate(Sum('total_beneficiary'))['total_beneficiary__sum']
        return Response({
            'investment_focus': investment,
            'total_budget': budget,
            'beneficiary': beneficiary,
            'project': project,
            'partner': partner,
            'other_products': other_products,
            'branch': branch,
            'blb': blb,
            'tablet': tablet,

        })


class PartnershipMap(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = True

    def list(self, request, **kwargs):
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        group = Group.objects.get(user=user)
        data = []

        if request.GET.getlist('status'):
            status_get = request.GET['status']
            status = status_get.split(",")
        else:
            status = ['Ongoing', 'Completed']

        if request.GET.getlist('investment_filter'):
            investment_get = request.GET['investment_filter']
            investment_list = investment_get.split(",")
            # for i in range(0, len(investment_filter_id)):
            #     investment_filter_id[i] = int(investment_filter_id[i])
            investment_list = list(
                Project.objects.filter(investment_primary__in=investment_list).values_list('investment_primary',
                                                                                           flat=True).distinct())
        else:
            investment_list = list(Project.objects.values_list('investment_primary', flat=True).distinct())

        if request.GET.getlist('partner_type_filter'):
            partner_type_get = request.GET['partner_type_filter']
            partner_types = partner_type_get.split(",")
            partner_types = list(
                Partner.objects.filter(type__in=partner_types).values_list('type', flat=True).distinct())

        else:
            partner_types = list(Partner.objects.values_list('type', flat=True).distinct())

        if request.GET.getlist('partner_filter'):
            partner_get = request.GET['partner_filter']
            partner_filter_list = partner_get.split(",")
            for i in range(0, len(partner_filter_list)):
                partner_filter_list[i] = int(partner_filter_list[i])
            partner_filter_list = list(
                Partner.objects.filter(id__in=partner_filter_list).values_list('id', flat=True).distinct())

        else:
            partner_filter_list = list(Partner.objects.values_list('id', flat=True).distinct())

        if request.GET.getlist('project_filter'):
            project_get = request.GET['project_filter']
            project_filter_list = project_get.split(",")
            for i in range(0, len(project_filter_list)):
                project_filter_list[i] = int(project_filter_list[i])
            project_filter_list = list(
                Project.objects.filter(id__in=project_filter_list).values_list('id', flat=True).distinct())

        else:
            project_filter_list = list(Project.objects.values_list('id', flat=True).distinct())

        partnership_query = Partnership.objects.filter(project_id__investment_primary__in=investment_list,
                                                       project_id__in=project_filter_list,
                                                       partner_id__type__in=partner_types,
                                                       partner_id__in=partner_filter_list,
                                                       status__in=status,
                                                       ).values('project_id', 'project_id__name')

        if request.GET.getlist('province_id'):
            province_get = request.GET['province_id']
            if province_get == '0':
                province_filter_list = Province.objects.values('id', 'name', 'code').order_by('id')
                for y in province_filter_list:
                    prov = partnership_query.values('district_id', 'province_id', 'partner_id').filter(
                        province_id=y['id'])
                    project_list = prov.values_list('project_id__name', flat=True).distinct('project_id')
                    count = prov.distinct('project_id').count()
                    data.append({
                        'id': y['id'],
                        'name': y['name'],
                        'code': y['code'],
                        'project_list': project_list,
                        'count': count,
                    })

            else:
                province_filter_list = province_get.split(",")
                for i in range(0, len(province_filter_list)):
                    province_filter_list[i] = int(province_filter_list[i])
                province_filter_list_id = Province.objects.filter(code__in=province_filter_list).values('id', 'name',
                                                                                                        'code').order_by(
                    'id')
                for y in province_filter_list_id:
                    prov = partnership_query.values('district_id', 'province_id', 'partner_id').filter(
                        province_id=y['id'])
                    project_list = prov.values_list('project_id__name', flat=True).distinct('project_id')
                    count = prov.distinct('project_id').count()
                    data.append({
                        'id': y['id'],
                        'name': y['name'],
                        'code': y['code'],
                        'project_list': project_list,
                        'count': count,
                    })

        if request.GET.getlist('district_id'):
            district_get = request.GET['district_id']
            if district_get == '0':
                district_filter_list = District.objects.values('id', 'n_code', 'name').order_by('id')
                for x in district_filter_list:
                    dist = partnership_query.values('project_id', 'project_id__name').filter(district_id=x['id'])

                    project_list = dist.values_list('project_id__name', flat=True).distinct('project_id')
                    count = dist.distinct('project_id').count()
                    data.append({
                        'id': x['id'],
                        'name': x['name'],
                        'code': x['n_code'],
                        'project_list': project_list,
                        'count': count,
                    })

            else:
                district_filter_list = district_get.split(",")
                for i in range(0, len(district_filter_list)):
                    district_filter_list[i] = int(district_filter_list[i])
                district_filter_list_id = District.objects.filter(n_code__in=district_filter_list).values('id',
                                                                                                          'n_code',
                                                                                                          'name').order_by(
                    'id')
                for x in district_filter_list_id:
                    dist = partnership_query.values('project_id', 'project_id__name').filter(district_id=x['id'])

                    project_list = dist.values_list('project_id__name', flat=True).distinct('project_id')
                    count = dist.distinct('project_id').count()
                    data.append({
                        'id': x['id'],
                        'name': x['name'],
                        'code': x['n_code'],
                        'project_list': project_list,
                        'count': count,
                    })

        if request.GET.getlist('municipality_id'):
            municipality_get = request.GET['municipality_id']
            if municipality_get == '0':
                municipality_filter_list = Municipality.objects.values('id', 'name', 'code').order_by('id')
                for i in municipality_filter_list:
                    mun = partnership_query.values('project_id', 'project_id__name').filter(
                        municipality_id=i['id'])
                    project_list = mun.values_list('project_id__name', flat=True).distinct('project_id')
                    count = mun.distinct('project_id').count()
                    data.append({
                        'id': i['id'],
                        'name': i['name'],
                        'code': i['code'],
                        'project_list': project_list,
                        'count': count,
                    })
            else:
                municipality_filter_list = municipality_get.split(",")
                for i in range(0, len(municipality_filter_list)):
                    municipality_filter_list[i] = int(municipality_filter_list[i])
                municipality_filter_list_id = Municipality.objects.filter(code__in=municipality_filter_list).values(
                    'id', 'name', 'code').order_by('id')

                for i in municipality_filter_list_id:
                    mun = partnership_query.values('project_id', 'project_id__name').filter(
                        municipality_id=i['id'])
                    project_list = mun.values_list('project_id__name', flat=True).distinct('project_id')
                    count = mun.distinct('project_id').count()
                    data.append({
                        'id': i['id'],
                        'name': i['name'],
                        'code': i['code'],
                        'project_list': project_list,
                        'count': count,
                    })

        return Response(data)
