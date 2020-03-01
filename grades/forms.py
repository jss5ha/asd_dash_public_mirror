from . import models
from django.forms import ModelForm, ModelChoiceField

class courseForm(ModelForm):
    class Meta:
        model = models.course
        fields = ('course_name',)

class assTypeForm(ModelForm):

    class Meta:
        model = models.assType
        #using a model form for those excluded from this
        #see https://stackoverflow.com/questions/11933548/in-a-form-how-to-display-fields-from-other-models-using-foreign-keys-specially?noredirect=1&lq=1
        fields = ('course','ass_type','grade_percentage')

class assignmentForm(ModelForm):
    class Meta:
        model = models.assignment
        fields = ('course', 'ass_name', 'grade', 'grade_percentage')