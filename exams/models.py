from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from os import path

class Course(models.Model):
  code = models.CharField(max_length = 20, unique = True)
  name = models.CharField(max_length = 100)
  def get_absolute_url(self):
    return "/courses/%i/" % self.id
  def __unicode__(self):
    return "%s: %s" % (self.code, self.name)

class Lang(models.Model):
  code = models.CharField(max_length = 3)
  name = models.CharField(max_length = 20)
  def __unicode__(self):
    return self.name

class Exam(models.Model):
  course = models.ForeignKey(Course)
  desc = models.CharField(max_length = 100)
  exam_date = models.DateField()
  date_added = models.DateField(auto_now_add = True)
  lang = models.ForeignKey(Lang)
  submitter = models.ForeignKey(User, null = True, blank = True)
  def get_absolute_url(self):
    return "/exams/%i/%s/%s/" % (self.id, slugify(self.course.code), slugify(self.exam_date))
  def __unicode__(self):
    return "%s: %s %s" % (self.course.code, self.exam_date, self.desc)

def exam_file_name(instance, filename):
  return '/'.join(['exams',  ''.join([str(instance.exam.id), path.splitext(filename)[1]])])

class ExamFile(models.Model):
  exam = models.ForeignKey(Exam)
  exam_file = models.FileField(upload_to = exam_file_name)
