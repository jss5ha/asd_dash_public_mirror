from django.shortcuts import render, redirect, get_object_or_404
from .models import course, assType, assignment
from .forms import courseForm, assTypeForm, assignmentForm
from django.urls import reverse
from django.views import generic
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.db import IntegrityError

#TODO: make queryset based on logged in user

class IndexView(generic.ListView):
    template_name = 'grades/index.html'
    context_object_name = 'course_list'

    def get_queryset(self):
        return course.objects.filter(owner=self.request.user)

class CourseView(generic.ListView):
    model = course
    template_name = 'grades/courses.html'
    def get_queryset(self):
        return course.objects.all()

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

def IndCourse(request, course_id):
    indCourse = course.objects.get(id = course_id)
    # print(indCourse)
    # print(indCourse.assignment_set.all())
    # print(indCourse.asstype_set.all())
    context = {'indCourse': indCourse}
    template = 'grades/indCourse.html'
    return render(request, template, context)
   
def RemoveType(request, course_id, asstype_id):
    # indCourse = get_object_or_404(course, pk = course_id)
    atype = get_object_or_404(assType, pk = asstype_id)
    for i in atype.assignment_set.all():
        i.delete()
    atype.delete()
    CalculateGrade(request, course_id)
    return HttpResponseRedirect(reverse('grades:toIndCourse', args = (course_id,)))

def NewType(request, pk):
    indCourse = get_object_or_404(course, pk=pk)
    if(request.method == 'POST'):
        form = courseForm(request.POST)
        if form.is_valid():
            counter = 0
            if int(request.POST.get('grade_input')) < 0:
                return HttpResponseRedirect(reverse('grades:toIndCourse', args = (pk,)))
            counter = int(request.POST.get('grade_input'))
            for i in indCourse.asstype_set.all():
                counter += i.grade_percentage
            if counter > 100 or counter < 0:
                return HttpResponseRedirect(reverse('grades:toIndCourse', args = (pk,)))
            indCourse.asstype_set.create(course = indCourse, ass_type = request.POST.get('course_name'), grade_percentage = request.POST.get('grade_input'))
            return HttpResponseRedirect(reverse('grades:toIndCourse', args = (pk,)))
            
def NewAssignment(request, course_id, asstype_id):
    indCourse = get_object_or_404(course, pk=course_id)
    atype = get_object_or_404(assType, pk = asstype_id)
    if(request.method == 'POST'):
        form = courseForm(request.POST)
        if form.is_valid():
            if int(request.POST.get('grade_input')) < 0:
                return HttpResponseRedirect(reverse('grades:toIndCourse', args=(course_id,)))
           
            atype.assignment_set.create(course = indCourse, ass_type = atype, ass_name = request.POST.get("course_name"), grade = request.POST.get('grade_input'))
                # indCourse.assignment_set.add(target)
            # except IntegrityError as e:
            CalculateGrade(request, course_id)
            return HttpResponseRedirect(reverse('grades:toIndCourse', args=(course_id,)))
                
    return HttpResponseRedirect(reverse('grades:toIndCourse', args=(course_id,)))
def CalculateGrade(request, course_id):
    indCourse = get_object_or_404(course, pk = course_id)
    current = indCourse.course_grade
    overall = 0
    if indCourse.asstype_set.exists() is False:
        indCourse.course_grade = 0
        indCourse.improved = False
        indCourse.save()
        return
    total_grade_percent = 0
    for i in indCourse.asstype_set.all():
        if(i.assignment_set.exists()):
            num_of_assignments = 0
            for j in i.assignment_set.all():
                overall += j.grade * i.grade_percentage
                num_of_assignments += 1
            overall = overall / num_of_assignments

        total_grade_percent += i.grade_percentage
    
    x = float(overall/total_grade_percent)
    indCourse.course_grade = x
    if x >= current:
        indCourse.improved = True
    if x < current:
        indCourse.improved = False
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

class assView(generic.ListView):
    model = course
    template_name = 'grades/assignmentlist.html'
    def get_queryset(self):
        return course

class addAssignmentView(generic.ListView):
    model = course
    template_name = 'grades/assignments.html'
    def get_queryset(self):
        return course