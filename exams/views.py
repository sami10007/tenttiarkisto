from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.template import RequestContext
from exams.models import Course, Exam, ExamFile
from django.forms import EmailField, ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from datetime import datetime

def courselist(request):
  q = request.GET.get('q', '')
  all_courses = Course.objects.annotate(exam_count=Count('exam')).order_by('code').filter(Q(name__icontains=q)|Q(code__icontains=q)).all()
  return render_to_response('courselist.html', {'courses': all_courses}, context_instance=RequestContext(request))

def courseview(request, course_id):
  course = get_object_or_404(Course, pk=course_id)
  return render_to_response('courseview.html', {'course': course, 'exams': course.exam_set.order_by('-exam_date').all()}, context_instance=RequestContext(request))

class CourseForm(ModelForm):
  class Meta:
    model = Course

def addcourse(request):
  saved = False
  course = None
  if request.method == 'POST':
    form = CourseForm(request.POST)
    if form.is_valid():
      course = form.save()
      saved = True
      form = CourseForm()
  else:
    form = CourseForm()
  return render_to_response('addcourse.html', {'form': form, 'saved': saved, 'course': course}, context_instance=RequestContext(request))

# exam & add exam views

class ExamForm(ModelForm):
  class Meta:
    model = Exam
    exclude = ('submitter',)

class ExamFileForm(ModelForm):
  class Meta:
    model = ExamFile
    exclude = ('exam',)

def examview(request, exam_id):
  exam = get_object_or_404(Exam, pk=exam_id)
  fileform = ExamFileForm()
  added = False
  if request.method == 'POST':
    fileform = ExamFileForm(request.POST, request.FILES)
    if fileform.is_valid():
      examfile = fileform.save(commit = False)
      examfile.exam = exam
      examfile.save()
      fileform = ExamFileForm()
      added = True
  return render_to_response('examview.html', {'exam': exam, 'files': exam.examfile_set.all(), 'fileform': fileform, 'added': added}, context_instance=RequestContext(request))

def addexam(request):
  added = False
  exam = None
  form = ExamForm(initial = {"exam_date": datetime.now().strftime("%Y-%m-%d")})
  fileform = ExamFileForm()
  if request.method == 'POST':
    form = ExamForm(request.POST)
    fileform = ExamFileForm(request.POST, request.FILES)
    if form.is_valid() and fileform.is_valid():
      exam = form.save(commit = False)
      if request.user.is_authenticated():
        exam.submitter = request.user
      exam.save()
      examfile = fileform.save(commit = False)
      examfile.exam = exam
      examfile.save()
      fileform = ExamFileForm()
      form = ExamForm()
      added = True
  # sort the courses properly
  form.fields["course"].queryset = Course.objects.order_by('code').all()
  return render_to_response('addexam.html', {'form': form, 'added': added, 'fileform': fileform, 'new_exam': exam}, context_instance=RequestContext(request))


# user registration view

# a user creation form that requires email
class UserCreationEmailForm(UserCreationForm):
  email = EmailField(required=True, help_text = "We will only use email to help you recover your account.")
  class Meta:
    model = User
    fields = ("username", "email", "password1", "password2")
  def save(self, commit=True):
    user = super(UserCreationEmailForm, self).save(commit=False)
    user.email = self.cleaned_data["email"]
    if commit:
      user.save()
    return user

def register(request):
  if request.user.is_authenticated():
    return HttpResponseRedirect('/')

  created = False
  if request.method == 'POST':
    form = UserCreationEmailForm(request.POST)
    if form.is_valid():
      created = True
      form.save()
      # a hack (?) to log the user in after registering
      user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
      login(request, user)
  else:
    form = UserCreationEmailForm()
  return render_to_response('register.html', {'form': form, 'created': created}, context_instance=RequestContext(request))
