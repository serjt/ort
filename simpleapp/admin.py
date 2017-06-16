from django.contrib import admin
from .models import *


# Register your models here.


class AlumniInline(admin.StackedInline):
    model = Alumni
    fields = 'ortId'.split()
    extra = 1


class FacultyAdmin(admin.ModelAdmin):
    fields = 'name lessons manager'.split()
    list_display = 'name'.split()
    inlines = [AlumniInline]


class AlumniLessonInline(admin.StackedInline):
    model = AlumniLesson
    fields = 'lesson grade'.split()
    extra = 1


class AlumniAdmin(admin.ModelAdmin):
    list_per_page = 30
    list_filter = 'tour place olimpiadnik lgotnik atestat'.split()
    list_editable = 'tour passed'.split()
    fields = 'barcode main extra_num summa ortId faculty tour place atestat lgotnik olimpiadnik passed'.split()
    list_display = 'ortId tour faculty passed'.split()

    inlines = [AlumniLessonInline]

admin.site.register(Tour)
admin.site.register(Otchet)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Lesson)
admin.site.register(Alumni,AlumniAdmin)
