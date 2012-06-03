from exams.models import Course, Exam, ExamFile, Maintainer
from django.contrib import admin

class ExamFileInline(admin.TabularInline):
  model = ExamFile

class ExamAdmin(admin.ModelAdmin):
  search_fields = ['id', 'course__code', 'course__name', 'desc']
  list_display = ['course', 'exam_date', 'desc']
  inlines = [
      ExamFileInline,
  ]

class CourseAdmin(admin.ModelAdmin):
  search_fields = ['id', 'code', 'name']
  list_display = ['code', 'name']

class MaintainerAdmin(admin.ModelAdmin):
  list_display = ['id', 'group', 'email']
  list_editable = ['group', 'email']

admin.site.register(Course, CourseAdmin)
admin.site.register(Exam, ExamAdmin)
admin.site.register(Maintainer, MaintainerAdmin)
