from . import models
from django.forms import ModelForm, ModelChoiceField
from django import forms

class PointCheckbox(ModelForm):
    pointbased = forms.BooleanField(label = '',required = False, widget = forms.CheckboxInput(attrs={'onchange': 'submit();'}))
    class Meta:
        model = models.course
        fields = ('pointbased',)
class courseForm(ModelForm):
    class Meta:
        model = models.course
        fields = ('course_name',)

class assTypeForm(ModelForm):

    class Meta:
        model = models.assType
        #using a model form for those excluded from this
        #see https://stackoverflow.com/questions/11933548/in-a-form-how-to-display-fields-from-other-models-using-foreign-keys-specially?noredirect=1&lq=1
        fields = ('ass_type','grade_percentage')
    def clean(self):
        # https://django.cowhite.com/blog/django-form-validation-and-customization-adding-your-own-validation-rules/
        super(assTypeForm, self).clean()
        ass_type = self.cleaned_data.get('ass_type')
        grade_percentage = self.cleaned_data.get('grade_percentage')
        if grade_percentage < 0:
            self._errors['grade_percentage'] = self.error_class(['Assignment weight must be above 0'])
        if grade_percentage > 100:
            self._errors['grade_percentage'] = self.error_class(['Assignment weight must be below 100'])
        if ass_type == None:
            self._errors['ass_type'] = self.error_class(['Please enter the assignment type'])
        if grade_percentage == None:
            self._errors['grade_percentage'] = self.error_class(['Please enter the weight of the assignment type'])
   
class assignmentForm(ModelForm):
    class Meta:
        model = models.assignment
        fields = ('ass_type','ass_name', 'grade')
    def clean(self):
        super(assignmentForm, self).clean()
        ass_type = self.cleaned_data.get('ass_type')
        ass_name = self.cleaned_data.get('ass_name')
        grade = self.cleaned_data.get('grade')
        if grade < 0:
            self._errors['grade'] = self.error_class(['Grade must be above 0'])
            # raise forms.ValidationError("bruh")
        if ass_name == None:
            self._errors['ass_name'] = self.error_class(['Please input a name'])
        if ass_type == None:
            self._errors['ass_type'] = self.error_class(['Please select a type'])

        return self.cleaned_data

class pointAssignmentForm(ModelForm):
    class Meta:
        model = models.pointAssignment
        fields = ('point_ass_name', 'points_achieved', 'points_total')