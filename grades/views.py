from django.shortcuts import render, redirect, get_object_or_404
from .forms import courseForm, assTypeForm, assignmentForm, PointCheckbox, pointAssignmentForm
from django.urls import reverse
from django.views import generic
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.db import IntegrityError

from .models import course, assType, assignment
from django import forms


#TODO: make queryset based on logged in user


class IndexView(generic.ListView):
    template_name = 'grades/index.html'
    context_object_name = 'course_list'

    def get_queryset(self):
        if not (self.request.user.is_anonymous):
            return course.objects.filter(owner=self.request.user)
        else:
            return course.objects.none()


def RemoveCourse(request, course_id):
    removed = course.objects.get(id = course_id)
    removed.delete()
    return HttpResponseRedirect(reverse('grades:index'))

def RemoveAssignment(request, course_id, assignment_id):
    indCourse = course.objects.get(id = course_id)
    removed = indCourse.assignment_set.get(id = assignment_id)
    removed.delete()
    CalculateGrade(request, course_id)
    return HttpResponseRedirect(reverse('grades:toIndCourse', args=(course_id,)))

def RemovePointAssignment(request, course_id, assignment_id):
    indCourse = course.objects.get(id = course_id)
    removed = indCourse.pointassignment_set.get(id = assignment_id)
    removed.delete()
    CalculatePointGrade(request, course_id)
    return HttpResponseRedirect(reverse('grades:toIndCourse', args=(course_id,)))

def IndCourse(request, course_id):

    try:
        indCourse = course.objects.filter(owner=request.user).get(id = course_id)
        course_id = indCourse.id
        points = PointCheckbox(request.POST or None)
        if(request.method == "POST"):
            if points.is_valid():
                pointschecked = request.POST.get('points')
           
                if pointschecked is None:
                    indCourse.pointbased = not(indCourse.pointbased)
                    indCourse.save()
                    template = 'grades/indCourse.html'
                    context = {'indCourse': indCourse, 'points': points}
                    return HttpResponseRedirect(reverse('grades:toIndCourse', args=(course_id,)))
        context = {'indCourse': indCourse, 'points': points}
        template = 'grades/indCourse.html'
        return render(request, template, context)
        # print(indCourse)
        # print(indCourse.assignment_set.all())
        # print(indCourse.asstype_set.all())
#         context = {'indCourse': indCourse}
#         template = 'grades/indCourse.html'
#         return render(request, template, context)
    except:
        # TODO: REPLACE THIS WITH AN ERROR
        return HttpResponseRedirect(reverse('grades:error'))

   
def RemoveType(request, course_id, asstype_id):
  
    atype = get_object_or_404(assType, pk = asstype_id)
    for i in atype.assignment_set.all():
        i.delete()
    atype.delete()
    CalculateGrade(request, course_id)
    return HttpResponseRedirect(reverse('grades:toIndCourse', args = (course_id,)))

def NewType(request, pk):
    indCourse = get_object_or_404(course, pk=pk)
    if(request.method == 'POST'):
        form = assTypeForm(request.POST)
       
        if form.is_valid():
            counter = 0
            counter = int(request.POST.get('grade_percentage'))
            
            for i in indCourse.asstype_set.all():
                counter += i.grade_percentage
            if counter > 100:
                # form._errors['grade_percentage'] = ErrorList([u"Grade percentage exceeded max of 100%"])
                # return HttpResponseRedirect(reverse('grades:toIndCourse', args = (pk,)))
                errors = form._errors.setdefault(forms.forms.NON_FIELD_ERRORS, forms.utils.ErrorList())
                errors.append("Grade weights must add up to less than 100%")
                template = 'grades/indCourse.html'
                return render(request, template, {'form2': form, 'indCourse': indCourse})
            indCourse.asstype_set.create(course = indCourse, ass_type = request.POST.get('ass_type'), grade_percentage = request.POST.get('grade_percentage'))
            return HttpResponseRedirect(reverse('grades:toIndCourse', args = (pk,)))
        else:
            template = 'grades/indCourse.html'
            return render(request, template, {'form2': form, 'indCourse': indCourse})
    return HttpResponseRedirect(reverse('grades:toIndCourse', args = (pk,)))

def NewAssignment2(request, course_id):
    IndCourse = get_object_or_404(course, pk = course_id)    
    if(request.method == 'POST'):
        form = assignmentForm(request.POST)
        if form.is_valid():
            atype = request.POST.get('ass_type')
            atype1 = get_object_or_404(assType, pk = atype)
            atype1.assignment_set.create(course = IndCourse, ass_type = atype1, ass_name = request.POST.get('ass_name'), grade = request.POST.get('grade'))
            CalculateGrade(request, course_id)
            return HttpResponseRedirect(reverse('grades:toIndCourse', args=(course_id,)))
        else:
            template = 'grades/indCourse.html' 
            return render(request, template, {'form':form, 'indCourse': IndCourse})
    return HttpResponseRedirect(reverse('grades:toIndCourse', args=(course_id,)))
def NewAssignment(request, course_id):
    indCourse = get_object_or_404(course, pk=course_id)
   
    if(request.method == 'POST'):
        form = pointAssignmentForm(request.POST)
        if form.is_valid():
            # if int(request.POST.get('grade_input')) < 0:
                # return HttpResponseRedirect(reverse('grades:toIndCourse', args=(course_id,)))

            indCourse.pointassignment_set.create(course = indCourse, point_ass_name = request.POST.get("point_ass_name"), points_achieved = request.POST.get('points_achieved'), points_total = request.POST.get('points_total'))
                # indCourse.assignment_set.add(target)
            # except IntegrityError as e:
            # CalculateGrade(request, course_id)
            CalculatePointGrade(request, course_id)
            return HttpResponseRedirect(reverse('grades:toIndCourse', args=(course_id,)))
                
    return HttpResponseRedirect(reverse('grades:toIndCourse', args=(course_id,)))
def CalculateGrade(request, course_id):
    indCourse = get_object_or_404(course, pk = course_id)
    current = indCourse.course_grade
    overall = 0
    total_grade_percent = 0
    if indCourse.pointbased is True:
        return
    if indCourse.asstype_set.exists() is False:
        indCourse.course_grade = 0
        indCourse.improved = False
        indCourse.save()
        return
    total_grade_percent = 0
    for i in indCourse.asstype_set.all():
        if(i.assignment_set.exists()):
            num_of_assignments = 0
            assignment_type_sum= 0
            for j in i.assignment_set.all():
                assignment_type_sum += j.grade 
                num_of_assignments += 1
            assignment_type_sum = assignment_type_sum * i.grade_percentage / num_of_assignments
            overall += assignment_type_sum
        total_grade_percent += i.grade_percentage
    # if indCourse.pointbased is True:
    #     for i in indCourse.assignment_set.all():
    #         if(i.pointbased is True):
    #             overall += i.grade
    #             total_grade_percent += i.grade
    x = float(overall/total_grade_percent)
    indCourse.course_grade = x
    if x >= current:
        indCourse.improved = True
    if x < current:
        indCourse.improved = False
    indCourse.save()
    return

def CalculatePointGrade(request, course_id):
    indCourse = get_object_or_404(course, pk = course_id)
    current = indCourse.course_grade_points
    earned = 0
    total = 0
    # if indCourse.pointbased is False:
    if indCourse.pointassignment_set.exists() is False:
        indCourse.course_grade_points = 0
        indCourse.point_improved = False
        indCourse.save()
        return
    # total_grade_percent = 0
    for i in indCourse.pointassignment_set.all():
        earned += i.points_achieved
        total += i.points_total
            
       
  
    x = float(earned/total) * 100
    indCourse.course_grade_points = x
    if x >= current:
        indCourse.point_improved = True
    if x < current:
        indCourse.point_improved = False
    indCourse.save()
    return

def NewCourse (request):
    # course1 = get_object_or_404(course)
    print(course.objects.all())
    if request.method == 'POST':
        form = courseForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = request.user
            # name = course1.course_name.get(pk = request.POST['course'])
            post.save()
            # course.objects.create(course_name = )
            return HttpResponseRedirect(reverse('grades:index'))
            # return redirect('grades/index.html', pk=post.pk)
    else:
        form = courseForm()
    # return render(request, 'grades/index.html', {'form': form})
    return HttpResponseRedirect(reverse('grades:index'))

def errormeth(request):
    return render(request=request, template_name='grades/error.html')

