from rest_framework import viewsets
from api.models import LogCategory, LogSubCategory, MilestoneYear, LogData, Province, District, Municipality, \
    Automation, Partner, AutomationPartner, FinancialProgram, FinancialLiteracy, Project, Partnership, Product, \
    ProductProcess, SecondaryData, Outreach, MFS, Insurance, Payment
from api.serializers import LogCategorySerializer, LogSubCategorySerializer, LogDataSerializer, MilestoneYearSerializer, \
    LogDataAlternativeSerializer, ProvinceSerializer, DistrictSerializer, MunicipalitySerializer, AutomationSerializer, \
    FinancialProgramSerializer, FinancialLiteracySerializer, FinancialPartnerSerializer, ProjectSerializer, \
    PartnerSerializer, PartnershipSerializer, InvestmentSerializer, ProductSerializer, ProductProcessSerializer, \
    SecondarySerializer, PaymentSerial

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User, Group, Permission
from dashboard.models import UserProfile
from django.core import serializers
from django.db.models import Sum, Count
import json
from django.core.serializers import serialize
from rest_framework.decorators import action


class LogCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = LogCategorySerializer
    queryset = LogCategory.objects.all()
    permission_classes = [IsAuthenticated, ]


class SecondaryViewSet(viewsets.ModelViewSet):
    serializer_class = SecondarySerializer
    permission_classes = [IsAuthenticated, ]

    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['id', 'province_id', 'district_id', 'municipality_id']

    def get_queryset(self):
        queryset = SecondaryData.objects.all()
        if self.request.GET.getlist('province_id'):
            province_id = self.request.GET['province_id'].split(",")
            for i in range(0, len(province_id)):
                province_id[i] = int(province_id[i])
            queryset = SecondaryData.objects.filter(province_id__code__in=province_id)

        if self.request.GET.getlist('district_id'):
            district_id = self.request.GET['district_id'].split(",")
            for i in range(0, len(district_id)):
                district_id[i] = int(district_id[i])
            queryset = SecondaryData.objects.filter(district_id__n_code__in=district_id)

        if self.request.GET.getlist('municipality_id'):
            municipality_id = self.request.GET['municipality_id'].split(",")
            for i in range(0, len(municipality_id)):
                municipality_id[i] = int(municipality_id[i])
            queryset = SecondaryData.objects.filter(municipality_id__code__in=municipality_id)

        return queryset


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


class ProductApi(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated, ]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', ]


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
        if investment:
            queryset = Project.objects.filter(investment_primary__in=investment).order_by('id')
        else:
            queryset = Project.objects.order_by('id')

        return queryset

    def get_serializer_class(self):
        serializer_class = ProjectSerializer
        return serializer_class


class ProductProcessApi(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'partner_id', 'partner_id__name', 'product_id', 'product_id__name', 'product_id__type',
                        'innovation_area',
                        'market_failure']

    def get_queryset(self):
        queryset = ProductProcess.objects.order_by('id')
        return queryset

    def get_serializer_class(self):
        serializer_class = ProductProcessSerializer
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
        # print(self.request.POST.getlist('id'))
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
        # print(self.request.POST.getlist('id'))
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
        # print(self.request.POST.getlist('id'))
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
        # print(year)
        year_data = []

        for i in range(0, len(year)):
            date_t = AutomationPartner.objects.filter(date__year=year[i])
            # print(date_t)
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
        if request.GET.getlist('partner'):
            partners_id = request.GET['partner'].split(",")
        else:
            partners_id = []

        if request.GET.getlist('province'):
            prov_id = request.GET['province'].split(",")
        else:
            prov_id = []

        if request.GET.getlist('district'):
            dist_id = request.GET['district'].split(",")
        else:
            dist_id = []

        if request.GET.getlist('municipality'):
            mun_id = request.GET['municipality'].split(",")
        else:
            mun_id = []

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
                # print(mun_id)
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
    queryset = Automation.objects.values('id')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'partner', 'province_id', 'district_id', 'municipality_id']

    def list(self, request, **kwargs):
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        group = Group.objects.get(user=user)
        data = []
        partners_ids = request.GET['partner']
        partners_id = partners_ids.split(",")

        automation_query = Automation.objects.values('partner__id', 'num_tablet_deployed')
        if request.GET['partner'] == '0':
            automation_query = automation_query

        else:
            for i in range(0, len(partners_id)):
                partners_id[i] = int(partners_id[i])
            automation_query = automation_query.filter(partner__partner__id__in=partners_id)

        if request.GET.getlist('province_id'):
            if request.GET['province_id'] == '0':
                map_data = automation_query.values('province_id', 'province_id__name', 'province_id__code').annotate(
                    Sum('num_tablet_deployed'))
                for d in map_data:
                    data.append({
                        'id': d['province_id'],
                        'name': d['province_id__name'],
                        'code': d['province_id__code'],
                        'tablets_deployed': d['num_tablet_deployed__sum'],
                    })
            else:
                prov_ids = request.GET['province_id']
                prov_id = prov_ids.split(",")
                for i in range(0, len(prov_id)):
                    prov_id[i] = int(prov_id[i])
                map_data = automation_query.filter(province_id__code__in=prov_id).values('province_id',
                                                                                         'province_id__name',
                                                                                         'province_id__code').annotate(
                    Sum('num_tablet_deployed'))
                for d in map_data:
                    data.append({
                        'id': d['province_id'],
                        'name': d['province_id__name'],
                        'code': d['province_id__code'],
                        'tablets_deployed': d['num_tablet_deployed__sum'],
                    })

        if request.GET.getlist('district_id'):
            if request.GET['district_id'] == '0':
                map_data = automation_query.values('district_id', 'district_id__name', 'district_id__n_code').annotate(
                    Sum('num_tablet_deployed'))
                for dist_data in map_data:
                    data.append({
                        'id': dist_data['district_id'],
                        'name': dist_data['district_id__name'],
                        'code': dist_data['district_id__n_code'],
                        'tablets_deployed': dist_data['num_tablet_deployed__sum'],
                    })
            else:
                dist_ids = request.GET['district_id']
                dist_id = dist_ids.split(",")
                for i in range(0, len(dist_id)):
                    dist_id[i] = int(dist_id[i])
                map_data = automation_query.filter(district_id__n_code__in=dist_id).values('district_id',
                                                                                           'district_id__name',
                                                                                           'district_id__n_code').annotate(
                    Sum('num_tablet_deployed'))
                for dist_data in map_data:
                    data.append({
                        'id': dist_data['district_id'],
                        'name': dist_data['district_id__name'],
                        'code': dist_data['district_id__n_code'],
                        'tablets_deployed': dist_data['num_tablet_deployed__sum'],
                    })
        if request.GET.getlist('municipality_id'):
            if request.GET['municipality_id'] == '0':
                map_data = automation_query.values('municipality_id', 'municipality_id__name',
                                                   'municipality_id__code').annotate(
                    Sum('num_tablet_deployed'))
                for mun_data in map_data:
                    data.append({
                        'id': mun_data['municipality_id'],
                        'name': mun_data['municipality_id__name'],
                        'code': mun_data['municipality_id__code'],
                        'tablets_deployed': mun_data['num_tablet_deployed__sum'],
                    })
            else:
                mun_ids = request.GET['municipality_id']
                mun_id = mun_ids.split(",")
                for i in range(0, len(mun_id)):
                    mun_id[i] = int(mun_id[i])
                map_data = automation_query.filter(municipality_id__code__in=mun_id).values('municipality_id',
                                                                                            'municipality_id__name',
                                                                                            'municipality_id__code').annotate(
                    Sum('num_tablet_deployed'))
                for mun_data in map_data:
                    data.append({
                        'id': mun_data['municipality_id'],
                        'name': mun_data['municipality_id__name'],
                        'code': mun_data['municipality_id__code'],
                        'tablets_deployed': mun_data['num_tablet_deployed__sum'],
                    })

        return Response(data)


class AutomationDataTable(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = Automation.objects.values('id')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'partner', 'province_id', 'district_id', 'municipality_id']

    def list(self, request, **kwargs):
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        group = Group.objects.get(user=user)
        data = []

        automation_query = Automation.objects.values('id', 'partner__partner__name', 'partner__partner__id',
                                                     'branch', 'province_id__name', 'province_id__code',
                                                     'district_id__name', 'district_id__n_code',
                                                     'municipality_id__name', 'municipality_id__code',
                                                     'num_tablet_deployed', 'partner__latitude',
                                                     'partner__longitude').order_by('id')

        if request.GET.getlist('partner'):
            partners_ids = request.GET['partner']
            partners_id = partners_ids.split(",")
            for i in range(0, len(partners_id)):
                partners_id[i] = int(partners_id[i])
            automation_query = automation_query.filter(partner__partner__id__in=partners_id)

        if request.GET.getlist('province_id'):
            prov_ids = request.GET['province_id']
            prov_id = prov_ids.split(",")
            for i in range(0, len(prov_id)):
                prov_id[i] = int(prov_id[i])
            automation_query = automation_query.filter(province_id__code__in=prov_id)

        if request.GET.getlist('district_id'):
            dist_ids = request.GET['district_id']
            dist_id = dist_ids.split(",")
            for i in range(0, len(dist_id)):
                dist_id[i] = int(dist_id[i])
            automation_query = automation_query.filter(district_id__n_code__in=dist_id)

        if request.GET.getlist('municipality_id'):
            mun_ids = request.GET['municipality_id']
            mun_id = mun_ids.split(",")
            for i in range(0, len(mun_id)):
                mun_id[i] = int(mun_id[i])
            automation_query = automation_query.filter(municipality_id__code__in=mun_id)

        for m in automation_query:
            data.append({
                'id': m['id'],
                'partner': m['partner__partner__name'],
                'partner_id': m['partner__partner__id'],
                'branch': m['branch'],
                'province': m['province_id__name'],
                'province_code': m['province_id__code'],
                'district': m['district_id__name'],
                'district_code': m['district_id__n_code'],
                'municipality': m['municipality_id__name'],
                'municipality_code': m['municipality_id__code'],
                'tablets': m['num_tablet_deployed'],
                'latitude': m['partner__latitude'],
                'longitude': m['partner__longitude'],

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
        partner_type = filter_data['partner_type']
        prov_id = filter_data['province_id']
        dist_id = filter_data['district_id']
        mun_id = filter_data['municipality_id']
        investment_filter = filter_data['investment_filter']
        investment = filter_data['investment']
        investment_project = filter_data['investment_project']
        project_id = filter_data['project_id']
        partner_id = filter_data['partner_id']
        view = filter_data['view']
        status = filter_data['status']
        investment_province = filter_data['investment_province']
        investment_district = filter_data['investment_district']
        investment_municipality = filter_data['investment_municipality']

        partnership_query = Partnership.objects.all()

        if partner_type:
            partnership_query = partnership_query.filter(partner_id__partnership__in=partner_type)

        if investment_filter:
            partnership_query = partnership_query.filter(project_id__investment_primary__in=investment_filter)

        if partner_id:
            if partner_id[0] == 0:
                partnership_query = partnership_query
                # partner = Partner.objects.values_list('id', flat=True).order_by('id')
            else:
                partner = partner_id
                partnership_query = partnership_query.filter(partner_id__in=partner)

        if project_id:
            if project_id[0] == 0:
                partnership_query = partnership_query
                # project = Project.objects.values_list('id', flat=True).order_by('id')
            else:
                project = project_id
                partnership_query = partnership_query.filter(project_id__in=project)

        if status:
            partnership_query = partnership_query.filter(status=status)

        else:
            partnership_query = partnership_query

        if investment_project:
            if investment_province:
                partnership_query = partnership_query.filter(province_id__code__in=investment_province)

            if investment_district:
                partnership_query = partnership_query.filter(district_id__n_code__in=investment_district)

            if investment_municipality:
                partnership_query = partnership_query.filter(municipality_id__code__in=investment_municipality)

            map_data = partnership_query.filter(project_id__investment_primary__in=investment_project).values(
                'project_id', 'project_id__name').annotate(Sum(view), Sum('female_beneficiary'))
            if map_data:
                for d in map_data:
                    data.append({
                        'id': d['project_id'],
                        'name': d['project_id__name'],
                        'code': 0,
                        view: d[view + '__sum'],
                        'female': d['female_beneficiary__sum'],
                    })

        if investment:
            if investment_province:
                partnership_query = partnership_query.filter(province_id__code__in=investment_province)

            if investment_district:
                partnership_query = partnership_query.filter(district_id__n_code__in=investment_district)

            if investment_municipality:
                partnership_query = partnership_query.filter(municipality_id__code__in=investment_municipality)
            map_data = partnership_query.filter(project_id__investment_primary__in=investment).values(
                'project_id__investment_primary').annotate(Sum(view), Sum('female_beneficiary'))
            if map_data:
                for d in map_data:
                    data.append({
                        'id': 1,
                        'name': d['project_id__investment_primary'],
                        'code': 0,
                        view: d[view + '__sum'],
                        'female': d['female_beneficiary__sum'],
                    })

        if prov_id:
            if prov_id[0] == 0:
                map_data = partnership_query.values('province_id', 'province_id__name', 'province_id__code').annotate(
                    Sum(view), Sum('female_beneficiary'))

                if map_data:
                    for d in map_data:
                        data.append({
                            'id': d['province_id'],
                            'name': d['province_id__name'],
                            'code': d['province_id__code'],
                            view: d[view + '__sum'],
                            'female': d['female_beneficiary__sum'],
                        })


            else:
                for i in range(0, len(prov_id)):
                    prov_id[i] = int(prov_id[i])
                map_data = partnership_query.filter(province_id__code__in=prov_id).values('province_id',
                                                                                          'province_id__name',
                                                                                          'province_id__code').annotate(
                    Sum(view), Sum('female_beneficiary'))

                if map_data:
                    for d in map_data:
                        data.append({
                            'id': d['province_id'],
                            'name': d['province_id__name'],
                            'code': d['province_id__code'],
                            view: d[view + '__sum'],
                            'female': d['female_beneficiary__sum'],
                        })

        if dist_id:
            if dist_id[0] == 0:
                map_data = partnership_query.values('district_id__n_code', 'district_id__name', 'district_id__id',
                                                    'province_id__code').annotate(
                    Sum(view), Sum('female_beneficiary'))

                if map_data:
                    for dist_data in map_data:
                        data.append({
                            'id': dist_data['district_id__id'],
                            'name': dist_data['district_id__name'],
                            'province_code': dist_data['province_id__code'],
                            'code': dist_data['district_id__n_code'],
                            view: dist_data[view + '__sum'],
                            'female': dist_data['female_beneficiary__sum'],
                        })


            else:
                for i in range(0, len(dist_id)):
                    dist_id[i] = int(dist_id[i])
                map_data = partnership_query.filter(district_id__n_code__in=dist_id).values('district_id__n_code',
                                                                                            'district_id__name',
                                                                                            'district_id__id',
                                                                                            'province_id__code').annotate(
                    Sum(view), Sum('female_beneficiary'))

                if map_data:
                    for dist_data in map_data:
                        data.append({
                            'id': dist_data['district_id__id'],
                            'name': dist_data['district_id__name'],
                            'province_code': dist_data['province_id__code'],
                            'code': dist_data['district_id__n_code'],
                            view: dist_data[view + '__sum'],
                            'female': dist_data['female_beneficiary__sum'],
                        })

        if mun_id:

            if mun_id[0] == 0:
                # mun_data = Municipality.objects.values('id', 'name', 'code', 'municipality_id__code',
                #                                        'province_id__code').order_by('id')
                map_data = partnership_query.values('municipality_id__code', 'municipality_id__name',
                                                    'municipality_id__id',
                                                    'province_id__code', 'district_id__n_code').annotate(
                    Sum(view), Sum('female_beneficiary'))

                if map_data:
                    for mun_data in map_data:
                        data.append({
                            'id': mun_data['municipality_id__id'],
                            'name': mun_data['municipality_id__name'],
                            'province_code': mun_data['province_id__code'],
                            'district_code': mun_data['district_id__n_code'],
                            'code': mun_data['municipality_id__code'],
                            view: mun_data[view + '__sum'],
                            'female': mun_data['female_beneficiary__sum'],
                        })


            else:
                for i in range(0, len(mun_id)):
                    mun_id[i] = int(mun_id[i])
                map_data = partnership_query.filter(municipality_id__code__in=mun_id).values('municipality_id__code',
                                                                                             'municipality_id__name',
                                                                                             'municipality_id__id',
                                                                                             'province_id__code',
                                                                                             'district_id__n_code').annotate(
                    Sum(view), Sum('female_beneficiary'))

                if map_data:
                    for mun_data in map_data:
                        data.append({
                            'id': mun_data['municipality_id__id'],
                            'name': mun_data['municipality_id__name'],
                            'province_code': mun_data['province_id__code'],
                            'district_code': mun_data['district_id__n_code'],
                            'code': mun_data['municipality_id__code'],
                            view: mun_data[view + '__sum'],
                            'female': mun_data['female_beneficiary__sum'],
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

        partnership_query = Partnership.objects.values('id', 'project_id__investment_primary', 'project_id',
                                                       'project_id__name', 'partner_id__name',
                                                       'partner_id', 'partner_id__name', 'allocated_budget',
                                                       'total_beneficiary')

        if request.GET.getlist('status'):
            status_get = request.GET['status']
            status = status_get.split(",")
            partnership_query = partnership_query.filter(status__in=status)
        else:
            status = ['Ongoing', 'Completed']
            partnership_query = partnership_query.filter(status__in=status)

        if request.GET.getlist('province_id'):
            province_get = request.GET['province_id']
            province_filter_list = province_get.split(",")
            for i in range(0, len(province_filter_list)):
                province_filter_list[i] = int(province_filter_list[i])
                partnership_query = partnership_query.filter(province_id__in=province_filter_list)

        else:
            # province_filter_list = list(Province.objects.values_list('id', flat=True).distinct())
            partnership_query = partnership_query

        if request.GET.getlist('district_id'):
            district_get = request.GET['district_id']
            district_filter_list = district_get.split(",")
            for i in range(0, len(district_filter_list)):
                district_filter_list[i] = int(district_filter_list[i])
            partnership_query = partnership_query.filter(district_id__in=district_filter_list)

        else:
            # district_filter_list = list(District.objects.values_list('id', flat=True).distinct())
            partnership_query = partnership_query

        if request.GET.getlist('municipality_id'):
            municipality_get = request.GET['municipality_id']
            municipality_filter_list = municipality_get.split(",")
            for i in range(0, len(municipality_filter_list)):
                municipality_filter_list[i] = int(municipality_filter_list[i])
            partnership_query = partnership_query.filter(municipality_id__in=municipality_filter_list)
        else:
            # municipality_filter_list = list(Municipality.objects.values_list('id', flat=True).distinct())
            partnership_query = partnership_query

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
                Partner.objects.filter(partnership__in=partner_types).values_list('partnership', flat=True).distinct())

        else:
            partner_types = list(Partner.objects.values_list('partnership', flat=True).distinct())

        if request.GET.getlist('partner_filter'):
            partner_get = request.GET['partner_filter']
            partner_filter_list = partner_get.split(",")
            for i in range(0, len(partner_filter_list)):
                partner_filter_list[i] = int(partner_filter_list[i])
            partner_filter_list = list(
                Partner.objects.filter(id__in=partner_filter_list).values_list('id', flat=True).distinct())
            partnership_query = partnership_query.filter(partner_id__in=partner_filter_list)

        else:
            # partner_filter_list = list(Partner.objects.values_list('id', flat=True).distinct())
            partnership_query = partnership_query

        if request.GET.getlist('project_filter'):
            project_get = request.GET['project_filter']
            project_filter_list = project_get.split(",")
            for i in range(0, len(project_filter_list)):
                project_filter_list[i] = int(project_filter_list[i])
            project_filter_list = list(
                Project.objects.filter(id__in=project_filter_list).values_list('id', flat=True).distinct())
            partnership_query = partnership_query.filter(project_id__in=project_filter_list)

        else:
            # project_filter_list = list(Project.objects.values_list('id', flat=True).distinct())
            partnership_query = partnership_query

        # partnership_query = Partnership.objects.values('id', 'project_id__investment_primary', 'project_id',
        #                                                'project_id__name', 'partner_id__name',
        #                                                'partner_id', 'partner_id__name', 'allocated_budget').filter(
        #
        #     district_id__in=district_filter_list,
        #     municipality_id__in=municipality_filter_list,
        #     project_id__in=project_filter_list,
        #     partner_id__in=partner_filter_list,
        #
        # )

        # print(partnership_query[0])
        for i in range(0, len(investment_list)):
            invest_query = partnership_query.values('project_id__investment_primary').filter(
                project_id__investment_primary=investment_list[i]).annotate(Sum(view))
            partner_type = []
            if invest_query:
                total = invest_query[0][view + '__sum']
                investment.append({
                    "name": investment_list[i],
                    "size": total,
                    "children": partner_type
                })

                for x in range(0, len(partner_types)):
                    p_type = partnership_query.values('partner_id__partnership').filter(
                        partner_id__partnership=partner_types[x],
                        project_id__investment_primary=
                        investment_list[i]).annotate(Sum(view))
                    p_data = []
                    if p_type:
                        partner_type.append({
                            "name": partner_types[x],
                            "size": p_type[0][view + '__sum'],
                            "children": p_data,

                        })
                        partner_filter_list = p_type.values_list('partner_id', flat=True).distinct()
                        for y in range(0, len(partner_filter_list)):
                            partner_q = p_type.values('partner_id__name').filter(
                                partner_id=partner_filter_list[y]).annotate(Sum(view))
                            partner_data = []
                            if partner_q:
                                p_data.append({
                                    "name": partner_q[0]['partner_id__name'],
                                    "size": partner_q[0][view + '__sum'],
                                    "children": partner_data,

                                })
                                project_filter_list = partner_q.values_list('project_id', flat=True).distinct()
                                for z in range(0, len(project_filter_list)):
                                    project_q = partner_q.values('project_id__name').filter(
                                        project_id=int(project_filter_list[z])).annotate(Sum(view))

                                    if project_q:
                                        partner_data.append({
                                            "name": project_q[0]['project_id__name'],
                                            "size": project_q[0][view + '__sum'],

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
        project_id = []
        partner_id = []
        investment_id = []

        if request.GET.getlist('status'):
            status_get = request.GET['status']
            status = status_get.split(",")
        else:
            status = ['Ongoing', 'Completed']

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
                Partner.objects.filter(partnership__in=partner_types).values_list('partnership', flat=True).distinct())

        else:
            partner_types = list(Partner.objects.values_list('partnership', flat=True).distinct())

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

        partnership_query = Partnership.objects.prefetch_related('project_id', 'partner_id').filter(
            status__in=status,
            project_id__in=project_filter_list,
            project_id__investment_primary__in=investment_list,
            partner_id__partnership__in=partner_types,
            partner_id__id__in=partner_filter_list,
            province_id__id__in=province_filter_list,
            district_id__id__in=district_filter_list,
            municipality_id__id__in=municipality_filter_list,
        )

        project = partnership_query.values("project_id__name", "project_id").distinct('project_id')
        for c in project:
            node.append({
                'id': c['project_id__name'],

            })
            project_id.append(c['project_id'])

        for i in range(0, len(investment_list)):
            node.append({
                'id': investment_list[i],

            })
            investment_id.append(investment_list[i])

        partner = partnership_query.values("partner_id__name", "partner_id").distinct('partner_id')
        for part in partner:
            node.append({
                'id': part['partner_id__name'],

            })
            partner_id.append(part['partner_id'])

        # for i in range(0, len(project_id)):
        #     q = partnership_query.values('project_id__investment_primary', 'project_id__name',
        #                                  'partner_id__type', 'partner_id__name', ).filter(
        #         project_id=project_id[i])
        #     budget = q.aggregate(Sum(view))
        #     source = q[0]['project_id__name']
        #     target = q[0]['project_id__investment_primary']
        #     links.append({
        #         'source': source,
        #         'target': target,
        #         'value': int(budget[view + '__sum']),
        #     })

        # for x in range(0, len(partner_id)):
        q = partnership_query.values('partner_id', 'partner_id__name', 'project_id__name', 'partner_id__type',
                                     'project_id__investment_primary', )

        # budget = q.aggregate(Sum(view))
        budgets = q.annotate(Sum(view))
        # print(budgets)
        # print(budget)
        for b in budgets:
            links.append({
                'source': b['project_id__name'],
                'target': b['project_id__investment_primary'],
                'value': int(b[view + '__sum']),
            })

            links.append({
                'source': b['project_id__investment_primary'],
                'target': b['partner_id__name'],
                'value': int(b[view + '__sum']),
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

        if request.GET.getlist('status'):
            status_get = request.GET['status']
            status = status_get.split(",")
        else:
            status = ['Ongoing', 'Completed']

        if request.GET.getlist('province_id'):
            province_get = request.GET['province_id']
            province_filter_list = province_get.split(",")
            for i in range(0, len(province_filter_list)):
                province_filter_list[i] = int(province_filter_list[i])

        else:
            province_filter_list = list(Province.objects.values_list('code', flat=True).distinct())

        if request.GET.getlist('district_id'):
            district_get = request.GET['district_id']
            district_filter_list = district_get.split(",")
            for i in range(0, len(district_filter_list)):
                district_filter_list[i] = int(district_filter_list[i])

        else:
            district_filter_list = list(District.objects.values_list('n_code', flat=True).distinct())

        if request.GET.getlist('municipality_id'):
            municipality_get = request.GET['municipality_id']
            municipality_filter_list = municipality_get.split(",")
            for i in range(0, len(municipality_filter_list)):
                municipality_filter_list[i] = int(municipality_filter_list[i])

        else:
            municipality_filter_list = list(Municipality.objects.values_list('code', flat=True).distinct())

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
                Partner.objects.filter(partnership__in=partner_types).values_list('partnership', flat=True).distinct())

        else:
            partner_types = list(Partner.objects.values_list('partnership', flat=True).distinct())

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
                                                       status__in=status,
                                                       project_id__in=project_filter_list,
                                                       partner_id__partnership__in=partner_types,
                                                       partner_id__in=partner_filter_list,
                                                       province_id__code__in=province_filter_list,
                                                       district_id__n_code__in=district_filter_list,
                                                       municipality_id__code__in=municipality_filter_list,
                                                       )
        partner = partnership_query.values('partner_id').distinct().count()
        project = partnership_query.values('project_id').distinct().count()
        investment = partnership_query.values('project_id__investment_primary').distinct().count()
        other_products = partnership_query.aggregate(Sum('other_products'))['other_products__sum']
        extension = partnership_query.aggregate(Sum('extension_counter'))['extension_counter__sum']
        tablet = partnership_query.aggregate(Sum('tablet'))['tablet__sum']
        branch = partnership_query.aggregate(Sum('branch'))['branch__sum']
        blb = partnership_query.aggregate(Sum('blb'))['blb__sum']
        budget = partnership_query.aggregate(Sum('allocated_budget'))['allocated_budget__sum']
        beneficiary = partnership_query.aggregate(Sum('total_beneficiary'))['total_beneficiary__sum']
        return Response({
            'investment_focus': investment,
            'total_budget': budget if budget else 0,
            'beneficiary': beneficiary if beneficiary else 0,
            'project': project,
            'partner': partner,
            'other_products': other_products if other_products else 0,
            'branch': branch if branch else 0 + extension if extension else 0,
            'extension': extension if extension else 0,
            'blb': blb if blb else 0,
            'tablet': tablet if tablet else 0,

        })


class PartnershipMap(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = True

    def list(self, request, **kwargs):
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        group = Group.objects.get(user=user)
        data = []

        partnership_query = Partnership.objects.values('project_id', 'partner_id', )

        if request.GET.getlist('pie'):
            pie_type = request.GET['pie']
        else:
            pie_type = 0

        if request.GET.getlist('status'):
            status_get = request.GET['status']
            status = status_get.split(",")
            partnership_query = partnership_query.filter(status__in=status)
        else:
            # status = ['Ongoing', 'Completed']
            partnership_query = partnership_query

        if request.GET.getlist('investment_filter'):
            investment_get = request.GET['investment_filter']
            investment_list = investment_get.split(",")
            # for i in range(0, len(investment_filter_id)):
            #     investment_filter_id[i] = int(investment_filter_id[i])
            investment_list = list(
                Project.objects.filter(investment_primary__in=investment_list).values_list('investment_primary',
                                                                                           flat=True).distinct())
            partnership_query = partnership_query.filter(project_id__investment_primary__in=investment_list)

        else:
            # investment_list = list(Project.objects.values_list('investment_primary', flat=True).distinct())
            partnership_query = partnership_query

        if request.GET.getlist('partner_type_filter'):
            partner_type_get = request.GET['partner_type_filter']
            partner_types = partner_type_get.split(",")
            partner_types = list(
                Partner.objects.filter(partnership__in=partner_types).values_list('partnership', flat=True).distinct())

            partnership_query = partnership_query.filter(partner_id__partnership__in=partner_types)

        else:
            # partner_types = list(Partner.objects.values_list('type', flat=True).distinct())
            partnership_query = partnership_query

        if request.GET.getlist('partner_filter'):
            partner_get = request.GET['partner_filter']
            partner_filter_list = partner_get.split(",")
            for i in range(0, len(partner_filter_list)):
                partner_filter_list[i] = int(partner_filter_list[i])
            partner_filter_list = list(
                Partner.objects.filter(id__in=partner_filter_list).values_list('id', flat=True).distinct())
            partnership_query = partnership_query.filter(project_id__id__in=partner_filter_list)
        else:
            # partner_filter_list = list(Partner.objects.values_list('id', flat=True).distinct())
            partnership_query = partnership_query

        if request.GET.getlist('project_filter'):
            project_get = request.GET['project_filter']
            project_filter_list = project_get.split(",")
            for i in range(0, len(project_filter_list)):
                project_filter_list[i] = int(project_filter_list[i])
            project_filter_list = list(
                Project.objects.filter(id__in=project_filter_list).values_list('id', flat=True).distinct())
            partnership_query = partnership_query.filter(project_id__id__in=project_filter_list)
        else:
            # project_filter_list = list(Project.objects.values_list('id', flat=True).distinct())
            partnership_query = partnership_query

        # partnership_query = Partnership.objects.values('project_id', 'partner_id', ).filter(
        #     project_id__investment_primary__in=investment_list,
        #     project_id__id__in=project_filter_list,
        #     partner_id__type__in=partner_types,
        #     partner_id__id__in=partner_filter_list,
        #     status__in=status,
        # )

        if request.GET.getlist('province_id'):
            province_get = request.GET['province_id']
            if province_get == '0':
                data_v = partnership_query.values('province_id__id', 'province_id__name',
                                                  'province_id__code').annotate(Count('project_id', distinct=True))
                for y in data_v:
                    investment = []
                    print(pie_type)
                    if pie_type == 'investment':
                        pie_invest = partnership_query.values('project_id__investment_primary').filter(
                            province_id__id=y['province_id__id']).annotate(Count('partner_id', distinct=True))
                        for pie in pie_invest:
                            project = partnership_query.filter(
                                project_id__investment_primary=pie['project_id__investment_primary'],
                                province_id__id=y['province_id__id']).values_list('partner_id__name',
                                                                                  flat=True).distinct()

                            investment.append({
                                'investment_primary': pie['project_id__investment_primary'],
                                'partner_count': pie['partner_id__count'],
                                'partner_list': project,
                                'total_beneficiary': 0,
                                'allocated_budget': 0

                            })

                    if pie_type == 'total_beneficiary':
                        pie_invest = partnership_query.values('project_id__investment_primary').filter(
                            province_id__id=y['province_id__id']).annotate(Sum('total_beneficiary'),
                                                                           Sum('allocated_budget'))
                        for pie in pie_invest:
                            investment.append({
                                'investment_primary': pie['project_id__investment_primary'],
                                'partner_count': 0,
                                'partner_list': [],
                                'total_beneficiary': pie['total_beneficiary__sum'],
                                'allocated_budget': pie['allocated_budget__sum']

                            })

                    data.append({
                        'id': y['province_id__id'],
                        'name': y['province_id__name'],
                        'code': y['province_id__code'],
                        'pie': investment,
                        'count': y['project_id__count'],
                    })

                # for y in province_filter_list:
                #     prov = partnership_query.values_list('project_id', flat=True).filter(
                #         province_id__id=y['id'])
                #     project_list = Project.objects.filter(id__in=prov).values_list('name', flat=True)
                #     count = len(project_list)
                #     data.append({
                #         'id': y['id'],
                #         'name': y['name'],
                #         'code': y['code'],
                #         'project_list': project_list,
                #         'count': count,
                #     })

            else:
                province_filter_list = province_get.split(",")
                for i in range(0, len(province_filter_list)):
                    province_filter_list[i] = int(province_filter_list[i])
                data_v = partnership_query.filter(province_id__code__in=province_filter_list).values('province_id__id',
                                                                                                     'province_id__name',
                                                                                                     'province_id__code').annotate(
                    Count('project_id', distinct=True))
                for y in data_v:
                    investment = []
                    if pie_type == 'investment':
                        pie_invest = partnership_query.values('project_id__investment_primary').filter(
                            province_id__id=y['province_id__id']).annotate(Count('partner_id', distinct=True))
                        for pie in pie_invest:
                            project = partnership_query.filter(
                                project_id__investment_primary=pie['project_id__investment_primary'],
                                province_id__id=y['province_id__id']).values_list('partner_id__name',
                                                                                  flat=True).distinct()

                            investment.append({
                                'investment_primary': pie['project_id__investment_primary'],
                                'partner_count': pie['partner_id__count'],
                                'partner_list': project,
                                'total_beneficiary': 0,
                                'allocated_budget': 0

                            })

                    if pie_type == 'total_beneficiary':
                        pie_invest = partnership_query.values('project_id__investment_primary').filter(
                            province_id__id=y['province_id__id']).annotate(Sum('total_beneficiary'),
                                                                           Sum('allocated_budget'))
                        for pie in pie_invest:
                            investment.append({
                                'investment_primary': pie['project_id__investment_primary'],
                                'partner_count': 0,
                                'partner_list': [],
                                'total_beneficiary': pie['total_beneficiary__sum'],
                                'allocated_budget': pie['allocated_budget__sum']

                            })

                    data.append({
                        'id': y['province_id__id'],
                        'name': y['province_id__name'],
                        'code': y['province_id__code'],
                        'pie': investment,
                        'count': y['project_id__count'],
                    })

        if request.GET.getlist('district_id'):
            district_get = request.GET['district_id']
            if district_get == '0':
                data_v = partnership_query.values('district_id__id', 'district_id__name',
                                                  'district_id__n_code').annotate(Count('project_id', distinct=True))
                for y in data_v:
                    pie_invest = partnership_query.values('project_id__investment_primary').filter(
                        district_id__id=y['district_id__id']).annotate(Count('partner_id', distinct=True))
                    investment = []
                    if pie_type == 'investment':
                        for pie in pie_invest:
                            project = partnership_query.filter(
                                project_id__investment_primary=pie['project_id__investment_primary'],
                                district_id__id=y['district_id__id']).values_list('partner_id__name',
                                                                                  flat=True).distinct()

                            investment.append({
                                'investment_primary': pie['project_id__investment_primary'],
                                'partner_count': pie['partner_id__count'],
                                'partner_list': project,
                                'total_beneficiary': 0,
                                'allocated_budget': 0

                            })

                    if pie_type == 'total_beneficiary':
                        pie_invest = partnership_query.values('project_id__investment_primary').filter(
                            district_id__id=y['district_id__id']).annotate(Sum('total_beneficiary'),
                                                                           Sum('allocated_budget'))
                        for pie in pie_invest:
                            investment.append({
                                'investment_primary': pie['project_id__investment_primary'],
                                'partner_count': 0,
                                'partner_list': [],
                                'total_beneficiary': pie['total_beneficiary__sum'],
                                'allocated_budget': pie['allocated_budget__sum']

                            })

                    data.append({
                        'id': y['district_id__id'],
                        'name': y['district_id__name'],
                        'code': y['district_id__n_code'],
                        'pie': investment,
                        'count': y['project_id__count'],
                    })

            else:
                district_filter_list = district_get.split(",")
                for i in range(0, len(district_filter_list)):
                    district_filter_list[i] = int(district_filter_list[i])
                data_v = partnership_query.filter(district_id__n_code__in=district_filter_list).values(
                    'district_id__id', 'district_id__name',
                    'district_id__n_code').annotate(Count('project_id', distinct=True))
                for y in data_v:

                    investment = []
                    if pie_type == 'investment':
                        pie_invest = partnership_query.values('project_id__investment_primary').filter(
                            district_id__id=y['district_id__id']).annotate(Count('partner_id', distinct=True))
                        for pie in pie_invest:
                            project = partnership_query.filter(
                                project_id__investment_primary=pie['project_id__investment_primary'],
                                district_id__id=y['district_id__id']).values_list('partner_id__name',
                                                                                  flat=True).distinct()

                            investment.append({
                                'investment_primary': pie['project_id__investment_primary'],
                                'partner_count': pie['partner_id__count'],
                                'partner_list': project,
                                'total_beneficiary': 0,
                                'allocated_budget': 0

                            })

                    if pie_type == 'total_beneficiary':
                        pie_invest = partnership_query.values('project_id__investment_primary').filter(
                            district_id__id=y['district_id__id']).annotate(Sum('total_beneficiary'),
                                                                           Sum('allocated_budget'))
                        for pie in pie_invest:
                            investment.append({
                                'investment_primary': pie['project_id__investment_primary'],
                                'partner_count': 0,
                                'partner_list': [],
                                'total_beneficiary': pie['total_beneficiary__sum'],
                                'allocated_budget': pie['allocated_budget__sum']

                            })
                    data.append({
                        'id': y['district_id__id'],
                        'name': y['district_id__name'],
                        'code': y['district_id__n_code'],
                        'pie': investment,
                        'count': y['project_id__count'],
                    })

        if request.GET.getlist('municipality_id'):
            municipality_get = request.GET['municipality_id']
            if municipality_get == '0':
                data_v = partnership_query.values(
                    'municipality_id__id', 'municipality_id__name',
                    'municipality_id__code').annotate(Count('project_id', distinct=True))
                for y in data_v:

                    investment = []
                    if pie_type == 'investment':
                        pie_invest = partnership_query.values('project_id__investment_primary').filter(
                            municipality_id__id=y['municipality_id__id']).annotate(Count('partner_id', distinct=True))
                        for pie in pie_invest:
                            project = partnership_query.filter(
                                project_id__investment_primary=pie['project_id__investment_primary'],
                                municipality_id__id=y['municipality_id__id']).values_list('partner_id__name',
                                                                                          flat=True).distinct()

                            investment.append({
                                'investment_primary': pie['project_id__investment_primary'],
                                'partner_count': pie['partner_id__count'],
                                'partner_list': project,
                                'total_beneficiary': 0,
                                'allocated_budget': 0

                            })
                    if pie_type == 'total_beneficiary':
                        pie_invest = partnership_query.values('project_id__investment_primary').filter(
                            municipality_id__id=y['municipality_id__id']).annotate(Sum('total_beneficiary'),
                                                                                   Sum('allocated_budget'))
                        for pie in pie_invest:
                            investment.append({
                                'investment_primary': pie['project_id__investment_primary'],
                                'partner_count': 0,
                                'partner_list': [],
                                'total_beneficiary': pie['total_beneficiary__sum'],
                                'allocated_budget': pie['allocated_budget__sum']

                            })

                    data.append({
                        'id': y['municipality_id__id'],
                        'name': y['municipality_id__name'],
                        'code': y['municipality_id__code'],
                        'pie': investment,
                        'count': y['project_id__count'],
                    })
            else:
                municipality_filter_list = municipality_get.split(",")
                for i in range(0, len(municipality_filter_list)):
                    municipality_filter_list[i] = int(municipality_filter_list[i])
                data_v = partnership_query.filter(municipality_id__code__in=municipality_filter_list).values(
                    'municipality_id__id', 'municipality_id__name',
                    'municipality_id__code').annotate(Count('project_id', distinct=True))
                for y in data_v:

                    investment = []
                    if pie_type == 'investment':
                        pie_invest = partnership_query.values('project_id__investment_primary').filter(
                            municipality_id__id=y['municipality_id__id']).annotate(Count('partner_id', distinct=True))
                        for pie in pie_invest:
                            project = partnership_query.filter(
                                project_id__investment_primary=pie['project_id__investment_primary'],
                                municipality_id__id=y['municipality_id__id']).values_list('partner_id__name',
                                                                                          flat=True).distinct()

                            investment.append({
                                'investment_primary': pie['project_id__investment_primary'],
                                'partner_count': pie['partner_id__count'],
                                'partner_list': project,
                                'total_beneficiary': 0,
                                'allocated_budget': 0

                            })
                    if pie_type == 'total_beneficiary':
                        pie_invest = partnership_query.values('project_id__investment_primary').filter(
                            municipality_id__id=y['municipality_id__id']).annotate(Sum('total_beneficiary'),
                                                                                   Sum('allocated_budget'))
                        for pie in pie_invest:
                            investment.append({
                                'investment_primary': pie['project_id__investment_primary'],
                                'partner_count': 0,
                                'partner_list': [],
                                'total_beneficiary': pie['total_beneficiary__sum'],
                                'allocated_budget': pie['allocated_budget__sum']

                            })

                    data.append({
                        'id': y['municipality_id__id'],
                        'name': y['municipality_id__name'],
                        'code': y['municipality_id__code'],
                        'pie': investment,
                        'count': y['project_id__count'],
                    })

        return Response(data)


class OutreachApi(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = Outreach.objects.values('id')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'partner_id', 'province_id', 'district_id', 'municipality_id', 'expansion_driven_by',
                        'partner_type', 'g2p_payment', 'demonstration_effect', 'point_service']

    def list(self, request, **kwargs):
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        group = Group.objects.get(user=user)
        data = []

        outreach_query = Outreach.objects.values('id', 'partner_id__outreach_expansion', 'partner_id__id',
                                                 'partner_id__name',
                                                 'market_name', 'province_id__name', 'province_id__code',
                                                 'district_id__name', 'district_id__n_code',
                                                 'municipality_id__name', 'municipality_id__code',
                                                 'expansion_driven_by', 'point_service',
                                                 'date_established', 'g2p_payment', 'demonstration_effect',
                                                 'gps_point').order_by('id')

        if request.GET.getlist('partner_id'):
            partners_ids = request.GET['partner_id']
            partners_id = partners_ids.split(",")
            for i in range(0, len(partners_id)):
                partners_id[i] = int(partners_id[i])
            outreach_query = outreach_query.filter(partner_id__id__in=partners_id)

        if request.GET.getlist('province_id'):
            prov_ids = request.GET['province_id']
            prov_id = prov_ids.split(",")
            for i in range(0, len(prov_id)):
                prov_id[i] = int(prov_id[i])
            outreach_query = outreach_query.filter(province_id__code__in=prov_id)

        if request.GET.getlist('district_id'):
            dist_ids = request.GET['district_id']
            dist_id = dist_ids.split(",")
            for i in range(0, len(dist_id)):
                dist_id[i] = int(dist_id[i])
            outreach_query = outreach_query.filter(district_id__n_code__in=dist_id)

        if request.GET.getlist('municipality_id'):
            mun_ids = request.GET['municipality_id']
            mun_id = mun_ids.split(",")
            for i in range(0, len(mun_id)):
                mun_id[i] = int(mun_id[i])
            outreach_query = outreach_query.filter(municipality_id__code__in=mun_id)

        if request.GET.getlist('expansion_driven_by'):
            expansion = request.GET['expansion_driven_by']
            exp = expansion.split(",")
            # for i in range(0, len(mun_id)):
            #     mun_id[i] = int(mun_id[i])
            outreach_query = outreach_query.filter(expansion_driven_by__in=exp)

        if request.GET.getlist('partner_type'):
            partner_types = request.GET['partner_type']
            partner_type = partner_types.split(",")
            # for i in range(0, len(mun_id)):
            #     mun_id[i] = int(mun_id[i])
            outreach_query = outreach_query.filter(partner_id__outreach_expansion__in=partner_type)

        if request.GET.getlist('g2p_payment'):
            g2p_payment = request.GET['g2p_payment']
            g2 = g2p_payment.split(",")
            # for i in range(0, len(mun_id)):
            #     mun_id[i] = int(mun_id[i])
            outreach_query = outreach_query.filter(g2p_payment__in=g2)

        if request.GET.getlist('demonstration_effect'):
            demonstration_effect = request.GET['demonstration_effect']
            effect = demonstration_effect.split(",")
            # for i in range(0, len(mun_id)):
            #     mun_id[i] = int(mun_id[i])
            outreach_query = outreach_query.filter(demonstration_effect__in=effect)

        if request.GET.getlist('point_service'):
            point_service = request.GET['point_service']
            point = point_service.split(",")
            # for i in range(0, len(mun_id)):
            #     mun_id[i] = int(mun_id[i])
            outreach_query = outreach_query.filter(point_service__in=point)

        for m in outreach_query:
            data.append({
                'id': m['id'],
                'partner': m['partner_id__name'],
                'partner_id': m['partner_id__id'],
                'partner_type': m['partner_id__outreach_expansion'],
                'market_name': m['market_name'],
                'province': m['province_id__name'],
                'province_code': m['province_id__code'],
                'district': m['district_id__name'],
                'district_code': m['district_id__n_code'],
                'municipality': m['municipality_id__name'],
                'municipality_code': m['municipality_id__code'],
                'gps_point': m['gps_point'],
                'expansion_driven_by': m['expansion_driven_by'],
                'date_established': m['date_established'],
                'point_service': m['point_service'],
                'g2p_payment': m['g2p_payment'],
                'demonstration_effect': m['demonstration_effect'],

            })

        return Response(data)


class OutreachMap(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = Outreach.objects.values('id')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'partner_id', 'province_id', 'district_id', 'municipality_id', 'expansion_driven_by',
                        'partner_type', 'g2p_payment', 'demonstration_effect', 'point_service']

    def list(self, request, **kwargs):
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        group = Group.objects.get(user=user)
        data = []

        outreach_query = Outreach.objects.values('id', 'point_service')

        if request.GET.getlist('partner_id'):
            partners_ids = request.GET['partner_id']
            partners_id = partners_ids.split(",")
            for i in range(0, len(partners_id)):
                partners_id[i] = int(partners_id[i])
            outreach_query = outreach_query.filter(partner_id__id__in=partners_id)

        if request.GET.getlist('expansion_driven_by'):
            expansion = request.GET['expansion_driven_by']
            exp = expansion.split(",")
            # for i in range(0, len(mun_id)):
            #     mun_id[i] = int(mun_id[i])
            outreach_query = outreach_query.filter(expansion_driven_by__in=exp)

        if request.GET.getlist('partner_type'):
            partner_types = request.GET['partner_type']
            partner_type = partner_types.split(",")
            # for i in range(0, len(mun_id)):
            #     mun_id[i] = int(mun_id[i])
            outreach_query = outreach_query.filter(partner_id__outreach_expansion__in=partner_type)

        if request.GET.getlist('g2p_payment'):
            g2p_payment = request.GET['g2p_payment']
            g2 = g2p_payment.split(",")
            # for i in range(0, len(mun_id)):
            #     mun_id[i] = int(mun_id[i])
            outreach_query = outreach_query.filter(g2p_payment__in=g2)

        if request.GET.getlist('demonstration_effect'):
            demonstration_effect = request.GET['demonstration_effect']
            effect = demonstration_effect.split(",")
            # for i in range(0, len(mun_id)):
            #     mun_id[i] = int(mun_id[i])
            outreach_query = outreach_query.filter(demonstration_effect__in=effect)

        if request.GET.getlist('point_service'):
            point_service = request.GET['point_service']
            point = point_service.split(",")
            # for i in range(0, len(mun_id)):
            #     mun_id[i] = int(mun_id[i])
            outreach_query = outreach_query.filter(point_service__in=point)

        if request.GET.getlist('province_id'):
            prov_ids = request.GET['province_id']
            if prov_ids == '0':
                data_v = outreach_query.values('province_id__id', 'province_id__name',
                                               'province_id__code').annotate(Count('point_service'))

            else:
                prov_id = prov_ids.split(",")
                for i in range(0, len(prov_id)):
                    prov_id[i] = int(prov_id[i])
                data_v = outreach_query.filter(province_id__code__in=prov_id).values('province_id__id',
                                                                                     'province_id__name',
                                                                                     'province_id__code').annotate(
                    Count('point_service'))

            for y in data_v:
                data.append({
                    'id': y['province_id__id'],
                    'name': y['province_id__name'],
                    'code': y['province_id__code'],
                    'count': y['point_service__count'],
                })

        if request.GET.getlist('district_id'):
            dist_ids = request.GET['district_id']
            if dist_ids == '0':
                data_v = outreach_query.values('district_id__id', 'district_id__name',
                                               'district_id__n_code').annotate(Count('point_service'))

            else:
                dist_id = dist_ids.split(",")
                for i in range(0, len(dist_id)):
                    dist_id[i] = int(dist_id[i])
                data_v = outreach_query.filter(district_id__n_code__in=dist_id).values('district_id__id',
                                                                                       'district_id__name',
                                                                                       'district_id__n_code').annotate(
                    Count('point_service'))

            for y in data_v:
                data.append({
                    'id': y['district_id__id'],
                    'name': y['district_id__name'],
                    'code': y['district_id__n_code'],
                    'count': y['point_service__count'],
                })

        if request.GET.getlist('municipality_id'):
            mun_ids = request.GET['municipality_id']
            if mun_ids == '0':
                data_v = outreach_query.values('municipality_id__id', 'municipality_id__name',
                                               'municipality_id__code').annotate(Count('point_service'))

            else:
                mun_id = mun_ids.split(",")
                for i in range(0, len(mun_id)):
                    mun_id[i] = int(mun_id[i])
                data_v = outreach_query.filter(municipality_id__code__in=mun_id).values('municipality_id__id',
                                                                                        'municipality_id__name',
                                                                                        'municipality_id__code').annotate(
                    Count('point_service'))

            for y in data_v:
                data.append({
                    'id': y['municipality_id__id'],
                    'name': y['municipality_id__name'],
                    'code': y['municipality_id__code'],
                    'count': y['point_service__count'],
                })

        return Response(data)


class MfsData(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = MFS.objects.values('id')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'partner_id', 'province_id', 'district_id', 'municipality_id',
                        'key_innovation', 'achievement_type', 'achieved_number']

    def list(self, request, **kwargs):
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        group = Group.objects.get(user=user)
        data = []

        mfs_query = MFS.objects.values('id', 'partner_id__code', 'province_id__code', 'district_id__n_code',
                                       'municipality_id__code', 'partner_id__name',
                                       'key_innovation', 'achievement_type', 'achieved_number').exclude(
            province_id__isnull=True)
        for y in mfs_query:
            data.append({
                'id': y['id'],
                'partner_id': y['partner_id__code'],
                'partner_name': y['partner_id__name'],
                'province_code': y['province_id__code'],
                'district_code': y['district_id__n_code'],
                'municipality_code': y['municipality_id__code'],
                'key_innovation': y['key_innovation'],
                'achievement_type': y['achievement_type'],
                'achieved_number': y['achieved_number'],
            })

        return Response(data)


class InsuranceData(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = Insurance.objects.values('id')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'partner_id', 'distribution_channel', 'innovation',
                        'product', 'description', 'amount_of_claim',
                        'number_of_insurance_sold', 'amount_of_insurance',
                        'amount_of_sum_insuranced']

    def list(self, request, **kwargs):
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        group = Group.objects.get(user=user)
        data = []

        mfs_query = Insurance.objects.values('id', 'partner_id__code', 'distribution_channel', 'innovation',
                                             'product', 'description', 'amount_of_claim',
                                             'number_of_insurance_sold', 'amount_of_insurance',
                                             'amount_of_sum_insuranced', 'partner_id__name')

        for y in mfs_query:
            data.append({
                'id': y['id'],
                'partner_id': y['partner_id__code'],
                'partner_name': y['partner_id__name'],
                'product': y['product'],
                'description': y['description'],
                'distribution_channel': y['distribution_channel'],
                'amount_of_claim': y['amount_of_claim'],
                'number_of_insurance_sold': y['number_of_insurance_sold'],
                'amount_of_insurance': y['amount_of_insurance'],
                'amount_of_sum_insuranced': y['amount_of_sum_insuranced'],
                'innovation': y['innovation'],
            })

        return Response(data)


class PartnershipTimeline(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = True

    def list(self, request, **kwargs):
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        group = Group.objects.get(user=user)
        year_data = []
        timeline_data = []

        year = [d.year for d in Partnership.objects.values('start_date').dates('start_date', 'year')]
        for i in range(0, len(year)):
            month = 4
            for m in range(month, 13):
                if m % 4 == 0:
                    print(m)
                    quarter = str(year[i]) + '-' + str(m) + '-' + '1'
                    print(quarter)
                    year_data.append(quarter)

        for y in range(0, len(year_data)):
            project = []
            if request.GET.getlist('province_id'):
                timeline_query = Partnership.objects.values('province_id__code', 'province_id__name').filter(
                    start_date__lte=year_data[y]).annotate(Count('project_id', distinct=True))
                for t in timeline_query:
                    project.append({
                        'name': t['province_id__name'],
                        'code': t['province_id__code'],
                        'count': t['project_id__count']

                    })

            if request.GET.getlist('district_id'):
                timeline_query = Partnership.objects.values('district_id__n_code', 'district_id__name').filter(
                    start_date__lte=year_data[y]).annotate(Count('project_id', distinct=True))
                for t in timeline_query:
                    project.append({
                        'name': t['district_id__name'],
                        'code': t['district_id__n_code'],
                        'count': t['project_id__count']

                    })

            if request.GET.getlist('municipality_id'):
                timeline_query = Partnership.objects.values('municipality_id__code', 'municipality_id__name').filter(
                    start_date__lte=year_data[y]).annotate(Count('project_id', distinct=True))
                for t in timeline_query:
                    project.append({
                        'name': t['municipality_id__name'],
                        'code': t['municipality_id__code'],
                        'count': t['project_id__count']

                    })

            timeline_data.append({
                'date': year_data[y],
                'data': project
            })

        return Response(timeline_data)


class APIPayment(viewsets.ReadOnlyModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerial
    permission_classes = [IsAuthenticated, ]
