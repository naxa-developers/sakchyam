from django.core.management.base import BaseCommand

import pandas as pd

from api.models import Province, District, Municipality, Automation

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
                # district = District.objects.get(code=df['districtid'][row])
                municipality = Municipality.objects.get(hlcit_code=df['HLCIT'][row])
                automation = Automation.objects.get_or_create(
                    partner_institution=df['Partner Institution'][row],
                    branch=df['Name of branch'][row],
                    num_tablet_deployed=df['No. of Tablet Deployed'][row],
                    province_id=municipality.province_id,
                    district_id=municipality.district_id,
                    municipality_id=municipality,
                )

                print(row, 'Data was successfully updated')

            except Exception as e:
                print(e)




