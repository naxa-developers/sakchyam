from django.core.management.base import BaseCommand
import pandas as pd
from api.models import Project, Province, District, Municipality


class Command(BaseCommand):
    help = 'load province data from province.xlsx file'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']

        df = pd.read_csv(path)
        upper_range = len(df)
        print("Wait Data is being Loaded")

        try:
            proj = [
                Project(
                    province_id=Province.objects.get(code=df['Province No.'][row]),
                    district_id=District.objects.get(n_code=df['District_Code'][row]),
                    municipality_id=Municipality.objects.get(hlcit_code=df['HLCIT'][row]),
                    head_quarter=df['Head-Quarter of the Local Unit'][row],
                    hdi=df['HDI of District'][row],
                    population=df['Population in the Local Unit'][row],
                    yearly_fund=df['Yearly Central Government Funding'][row],
                    social_security_recipients=df['Social Security Payment Recipients'][row],
                    yearly_social_security_payment=df['Yearly Social Security Payments'][row],
                    nearest_branch_distance=df['Road distrance from nearest Commercial Bank Branch'][row],
                    communication_landline=df['Available Means of Communication_Landline'][row],
                    communication_mobile=df['Available Means of Communication_Mobile'][row],
                    communication_internet=df['Available Means of Communication_Internet'][row],
                    communication_internet_other=df['Available Means of Communication_OtherInternet'][row],
                    available_electricity_maingrid=df['Availability of Electricity_MainGrid'][row],
                    available_electricity_micro_hydro=df['Availability of Electricity_Micro-Hydro'][row],
                    nearest_road_location_name=df['Nearest Road Access_LocationName'][row],
                    nearest_road_distance=df['Nearest Road Access_Distance'][row],
                    nearest_road_type=df['Nearest Road Access_TypeOfRoad'][row],
                    nearest_police_location_name=df['Nearest Police Presence_LocationName'][row],
                    nearest_police_distance=df['Nearest Police Presence_Distance'][row],
                    categorisation_by_sakchyam=df['Categorisation by Sakchyam'][row],

                ) for row in range(0, upper_range)
            ]
            proj_data = Project.objects.bulk_create(proj)

            if proj_data:
                self.stdout.write('Successfully loaded Partner data ..')
            # for row in range(0, upper_range):
            #     print(df['Partner Name'][row])

        except Exception as e:
            print(e)
