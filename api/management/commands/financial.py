from django.core.management.base import BaseCommand
import pandas as pd
from api.models import Partner, FinancialLiteracy, FinancialProgram


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
            financial = [
                FinancialLiteracy(
                    partner_type=df['Partner Type'][row],
                    partner_id=Partner.objects.get(code=df['PartnerID'][row]),
                    program_id=FinancialProgram.objects.get(code=df['Programme_ID'][row]),
                    value=int(df['Value'][row]),
                    single_count=df['Total Single Count'][row],

                ) for row in range(0, upper_range)
            ]
            financial_data = FinancialLiteracy.objects.bulk_create(financial)

            if financial_data:
                self.stdout.write('Successfully loaded Financial Value  ..')
            # for row in range(0, upper_range):
            #     print(df['Partner Institution'][row])
            #     print(Partner.objects.get(code=df['PartnerID'][row]))


        except Exception as e:
            print(e)
