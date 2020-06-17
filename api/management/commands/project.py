from django.core.management.base import BaseCommand
import pandas as pd
from api.models import Project


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
                    name=(df['Project Name'][row]),
                    code=df['Project Code'][row],
                    investment_primary=df['Investment Focus (Primary)'][row],
                    investment_secondary=df['Investment Focus (Additional)'][row],

                ) for row in range(0, upper_range)
            ]
            proj_data = Project.objects.bulk_create(proj)

            if proj_data:
                self.stdout.write('Successfully loaded Partner data ..')
            # for row in range(0, upper_range):
            #     print(df['Partner Name'][row])

        except Exception as e:
            print(e)
