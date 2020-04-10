from django.core.management.base import BaseCommand

import pandas as pd

from api.models import Province, District, Municipality

from django.contrib.gis.geos import GEOSGeometry


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
                district = District.objects.get(code=df['districtid'][row])
                municipality = Municipality.objects.get_or_create(
                    name=df['Municipality'][row],
                    municipality_type=df['Municipality Type'][row],
                    code=df['munid'][row],
                    hlcit_code=df['hlcit'][row],
                    province_id=district.province_id,
                    district_id=district
                )

                print(row, 'Data was successfully updated')

            except Exception as e:
                print(e)




