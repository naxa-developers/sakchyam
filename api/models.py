from django.db import models

# Create your models here.


class LogCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    input = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class LogSubCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(LogCategory, on_delete=models.CASCADE, related_name='Category')

    def __str__(self):
        return self.name


class MilestoneYear(models.Model):
    year = models.DateField()

    def __str__(self):
        return self.date


class LogData(models.Model):
    baseline = models.CharField(max_length=30)
    planned = models.CharField(max_length=30)
    achieved = models.CharField(max_length=30)
    year = models.ForeignKey(MilestoneYear, on_delete=models.CASCADE, related_name='LogData')
    sub_category = models.ForeignKey(LogSubCategory, on_delete=models.CASCADE, related_name='LogData')
    category = models.ForeignKey(LogCategory, on_delete=models.CASCADE, related_name='LogData')

    def __str__(self):
        return self.sub_category.name

