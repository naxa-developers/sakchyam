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
    name = models.CharField(max_length=100, null=True, blank=True)
    range = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    title = models.CharField(max_length=500)
    source = models.CharField(max_length=500, null=True, blank=True)
    sub_category = models.ForeignKey(LogSubCategory, on_delete=models.CASCADE, related_name='TitleSubCat')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class LogData(models.Model):
    DATA_TYPE = (
        (0, 'Number'),
        (1, 'Funds'),
        (2, 'Percentage'),
    )
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='LogTitle', blank=True, null=True)
    data_type = models.IntegerField(choices=DATA_TYPE, default=0)
    planned = models.CharField(max_length=30, blank=True, null=True)
    planned_afp = models.CharField(max_length=30, blank=True, null=True)
    achieved = models.CharField(max_length=30, blank=True, null=True)
    year = models.ForeignKey(MilestoneYear, on_delete=models.CASCADE, related_name='LogYear')
    sub_category = models.ForeignKey(LogSubCategory, on_delete=models.CASCADE, related_name='LogSubCat')
    category = models.ForeignKey(LogCategory, on_delete=models.CASCADE, related_name='LogCat')

    def __str__(self):
        return self.sub_category.name
