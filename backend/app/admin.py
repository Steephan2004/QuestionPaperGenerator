from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import *

admin.site.site_header = "Question Paper Generator"
admin.site.site_title = "Your Custom Site Title"
admin.site.index_title = "Welcome to Your Editing site"

class QuestionInline(admin.TabularInline):
    
    model = Question
    extra=20
    max_num=20

class SubjectForm(forms.ModelForm):
    class Meta:
        model = NewQuestion
        fields = '__all__'

class SubjectAdmin(admin.ModelAdmin):
    form = SubjectForm
    inlines = [QuestionInline]

admin.site.register(NewQuestion, SubjectAdmin)
admin.site.register([Subject_Details,ExamCellUser])