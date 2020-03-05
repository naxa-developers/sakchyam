from django.db import models

# Create your models here.


class LogCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    input = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.name


class LogSubCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(LogCategory, on_delete=models.CASCADE, related_name='Category')

    def __str__(self):
        return self.name


class MilestoneYear(models.Model):
    year = models.CharField(max_length=100)

    def __str__(self):
        return self.year


class LogData(models.Model):
    DATA_TYPE = (
        (0, 'Number'),
        (1, 'Funds'),
        (2, 'Percentage'),
    )
    data_type = models.IntegerField(choices=DATA_TYPE, default=0)
    planned = models.CharField(max_length=30)
    achieved = models.CharField(max_length=30)
    year = models.ForeignKey(MilestoneYear, on_delete=models.CASCADE, related_name='LogData')
    sub_category = models.ForeignKey(LogSubCategory, on_delete=models.CASCADE, related_name='LogData')
    category = models.ForeignKey(LogCategory, on_delete=models.CASCADE, related_name='LogData')

    def __str__(self):
        return self.sub_category.name

