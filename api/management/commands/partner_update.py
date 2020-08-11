from django.core.management.base import BaseCommand
import pandas as pd
from api.models import Partner, Project


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
            for row in range(0, upper_range):
                # print(df['Project Code'][row])
                # print(int(df['Leverage'][row]))
                # print(df['hlcitId'][row])

                # palika_update = District.objects.filter(code=df['id'][row]).update(
                #     boundary=GEOSGeometry(df['geom'][row]))

                palika_update = Partner.objects.filter(code=df['Partner Name ID'][row]).update(
                    financial_literacy=df['Financial Literacy'][row],
                    partnership=df['Partnership'][row],
                    outreach_expansion=df['Outreach Expansion'][row],
                    mfs=df['MFS'][row],
                    product_process=df['ProductProcess'][row],
                )
                # palika_update = Project.objects.filter(code=df['Project Code'][row]).update(
                #     scf_funds=int(df['S-CF Funds'][row]))
            if palika_update:
                self.stdout.write('Successfully  updated data ..')

        except Exception as e:
            print(e)
