from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.db.models import Count, Q
from django.template import RequestContext
from exams.models import Course, Exam
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect

def courselist(request):
  q = request.GET.get('q', '')
  all_courses = Course.objects.annotate(exam_count=Count('exam')).order_by('code').filter(Q(name__icontains=q)|Q(code__icontains=q)).all()
  return render_to_response('courselist.html', {'courses': all_courses}, context_instance=RequestContext(request))

def courseview(request, course_id):
  course = get_object_or_404(Course, pk=course_id)
  return render_to_response('courseview.html', {'course': course, 'exams': course.exam_set.all()}, context_instance=RequestContext(request))

class CourseForm(ModelForm):
  class Meta:
    model = Course

@login_required
def addcourse(request):
  saved = False
  if request.method == 'POST':
    form = CourseForm(request.POST)
    if form.is_valid():
      form.save()
      saved = True
      form = CourseForm()
  else:
    form = CourseForm()
  return render_to_response('addcourse.html', {'form': form, 'saved': saved}, context_instance=RequestContext(request))

def examview(request, exam_id):
  exam = get_object_or_404(Exam, pk=exam_id)
  return render_to_response('examview.html', {'exam': exam, 'files': exam.examfile_set.all()}, context_instance=RequestContext(request))


def register(request):
  if request.user.is_authenticated():
    return HttpResponseRedirect('/')

  created = False
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      created = True
      form.save()
      # a hack (?) to log the user in after registering
      user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
      login(request, user)
  else:
    form = UserCreationForm()
  return render_to_response('register.html', {'form': form, 'created': created}, context_instance=RequestContext(request))
