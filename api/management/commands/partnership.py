from django.core.management.base import BaseCommand
import pandas as pd
from api.models import Project, Partner, Partnership, Province, District, Municipality


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
            p = [
                Partnership(
                    partner_id=Partner.objects.get(code=df['Partner Code'][row]),
                    project_id=Project.objects.get(code=df['Project Code'][row]),
                    province_id=Province.objects.get(code=df['State Code'][row]),
                    district_id=District.objects.get(n_code=df['District Code'][row]),
                    municipality_id=Municipality.objects.get(code=df['Local Unit code'][row]),
                    branch=df['Branch'][row],
                    blb=df['BLB'][row],
                    extension_counter=df['Extension Counter'][row],
                    tablet=df['Tablet'][row],
                    other_products=df['Other Major Products (Local units coverage)'][row],
                    beneficiary=df['Beneficiaries'][row],
                    scf_funds=df['S-CF Funds'][row],
                    allocated_budget=df['Allocated Funds to Local Units'][row],
                    allocated_beneficiary=df['Allocated Beneficiaries at Local Units'][row],
                    female_percentage=df['Female Pct'][row],
                    total_beneficiary=df['Total Beneficiaries'][row],
                    female_beneficiary=df['Female Beneficiaries'][row],
                    status=df['Status'][row],
                    start_date=df['Start date'][row],
                    end_date=df['End Date'][row],
                    project_year=df['Project Year'][row],

                ) for row in range(0, upper_range)
            ]
            p_data = Partnership.objects.bulk_create(p)

            if p_data:
                self.stdout.write('Successfully loaded Partner data ..')
            # for row in range(0, upper_range):
            #     print(df['New Local Unit'][row])
            #     print(df['District Code'][row])
            #     print(District.objects.get(n_code=df['District Code'][row]))

        except Exception as e:
            print(e)
