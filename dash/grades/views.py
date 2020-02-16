from django.shortcuts import render, redirect
from .models import course, assType, assignment
from .forms import courseForm, assTypeForm, assignmentForm
from django.urls import reverse
from django.views import generic
from django.http import HttpResponseRedirect

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


def NewCourse (request):
    if request.method == 'POST':
        form = courseForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return HttpResponseRedirect(reverse('grades:index'))
            # return redirect('grades/index.html', pk=post.pk)
    else:
        form = courseForm()
    # return render(request, 'grades/index.html', {'form': form})
    return HttpResponseRedirect(reverse('grades:index'))