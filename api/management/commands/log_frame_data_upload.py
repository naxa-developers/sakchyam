from django.core.management.base import BaseCommand

import pandas as pd

from api.models import LogData, LogSubCategory, LogCategory, MilestoneYear

from django.contrib.gis.geos import GEOSGeometry


class Command(BaseCommand):
    help = 'load province data from province.xlsx file'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        df = pd.read_excel(path)
        upper_range = len(df)

        for row in range(0, upper_range):
            print(df['Impact Indicator 1'][row])

        # print("Wait Data is being Loaded")
        #
        # for row in range(0, upper_range):
        #     try:
        #         animal = AnimalDetailData.objects.create(
        #             index=df['index'][row],
        #             parent_index=df['parent_index'][row],
        #             animal_type=df['animal_type'][row],
        #             animal_number=df['animal_number'][row],
        #             is_it_for_commercial_purpose=df['is_it_for_commercial_purpose'][row],
        #             survey=HouseHoldData.objects.get(index=df['parent_index'][row]),
        #
        #         )
        #
        #         print(row, 'Data was successfully updated')
        #
        #     except Exception as e:
        #         print(e)




