from django.core.management.base import BaseCommand
import pandas as pd
from api.models import Product


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
                Product(
                    name=df['Product'][row],
                    type=df['Product Category'][row],
                    code=int(df['Product Code'][row]),

                ) for row in range(0, upper_range)
            ]
            p_data = Product.objects.bulk_create(p)

            if p_data:
                self.stdout.write('Successfully loaded Partner data ..')
            # for row in range(0, upper_range):
            #     print(df['New Local Unit'][row])
            #     print(df['District Code'][row])
            #     print(District.objects.get(n_code=df['District Code'][row]))

        except Exception as e:
            print(e)
