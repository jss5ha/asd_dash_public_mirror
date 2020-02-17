from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class course (models.Model):
    course_name = models.CharField(max_length=75)

    def __str__(self):
        return self.course_name

class assType (models.Model):
    course = models.ForeignKey(course, on_delete=models.CASCADE)
    ass_type = models.CharField(max_length=30)
    grade_percentage = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(1)])

    def __str__(self):
        return self.ass_type + ' ' + str(self.grade_percentage)

class assignment (models.Model):
    ass_type = models.ForeignKey(assType, on_delete=models.CASCADE)
    course = models.ForeignKey(course, on_delete=models.CASCADE)
    ass_name = models.CharField(max_length=100)
    grade = models.IntegerField(default=0)

    def __str__(self):
        return self.ass_name + ' ' + str(self.grade)