from django.core.management.base import BaseCommand
import pandas as pd
from api.models import Partner, Province, District, Municipality, MFS


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
                if int(df['Province_Code'][row]) == -1:
                    p = None
                else:
                    p = Province.objects.get(code=df['Province_Code'][row])

                if int(df['District_Code'][row]) == -1:
                    d = None
                else:
                    d = District.objects.get(n_code=df['District_Code'][row])
                mf = MFS.objects.get_or_create(
                    province_id=p,
                    district_id=d,
                    # municipality_id=Municipality.objects.get(hlcit_code=df['HLCIT'][row]),
                    partner_id=Partner.objects.get(code=df['Partner id'][row]),
                    key_innovation=df['Key Innovation'][row],
                    achievement_type=df['Achievement Type'][row],
                    achieved_number=int(df['Achieved Number'][row]),

                )
                print(row, 'Data was successfully updated')
        except Exception as e:
            print(e)
