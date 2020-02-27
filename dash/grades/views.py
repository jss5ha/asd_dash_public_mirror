from django.shortcuts import render, redirect, get_object_or_404
from .models import course, assType, assignment
from .forms import courseForm, assTypeForm, assignmentForm
from django.urls import reverse
from django.views import generic
from django.http import HttpResponseRedirect
from django.db import IntegrityError


#todo: i think we can get rid of index view and the index.html file -joebediah
class IndexView(generic.ListView):
    template_name = 'grades/index.html'
    context_object_name = 'course_list'

    def get_queryset(self):
        return course.objects.all()

class CourseView(generic.ListView):
    model = course
    template_name = 'grades/courses.html'
    def get_queryset(self):
        return course.objects.all()



def IndCourse(request, pk):
    indCourse = course.objects.get(id = pk)
    print(indCourse)
    context = {'indCourse': indCourse}
    template = 'grades/indCourse.html'
    return render(request, template, context)
   
def NewAssignment(request, pk):
    indCourse = get_object_or_404(course, pk=pk)
    if(request.method == 'POST'):
        form = courseForm(request.POST)
        if form.is_valid():

            # try: 
            indCourse.assignment_set.create(course = indCourse, ass_name = request.POST.get("course_name"), grade = request.POST.get('grade_input'), grade_percentage = request.POST.get('grade_percentage'))
                # indCourse.assignment_set.add(target)
            # except IntegrityError as e:
    
            return IndCourse(request, pk)
                
    return IndCourse(request, pk)

def NewCourse (request):
    # course1 = get_object_or_404(course)
    if request.method == 'POST':
        form = courseForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            # name = course1.course_name.get(pk = request.POST['course'])
            post.save()
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