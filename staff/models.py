from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
class TestReport(models.Model):

    Age=models.IntegerField(validators=[MaxValueValidator(102),MinValueValidator(0)])
    HR=models.FloatField()
    O2Sat=models.FloatField()
    Temp=models.FloatField()
    SBP=models.FloatField()
    DBP=models.FloatField()
    Resp=models.FloatField()
    MAP=models.FloatField()