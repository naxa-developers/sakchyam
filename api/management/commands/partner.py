from django.core.management.base import BaseCommand

import pandas as pd

from api.models import Partner


class Command(BaseCommand):
    help = 'load district data from district_sak.csv file'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        df = pd.read_csv(path)
        upper_range = len(df)

        for row in range(0, upper_range):
            try:

                partner = Partner.objects.get_or_create(
                    name=df['name'][row],
                    code=df['code'][row],

                )

                print(row, 'Data was successfully updated')

            except Exception as e:
                print(e)
