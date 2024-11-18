from django import forms
from .models import NewQuestion, Question

class NewQuestionForm(forms.ModelForm):
    class Meta:
        model = NewQuestion
        fields = ['Department', 'subject_code', 'subject_name', 'branch', 'year', 'semester', 'course_instructor', 'date']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'image', 'BTlevel_COs']
class NewQuestionForm(forms.ModelForm):
    branch = forms.MultipleChoiceField(
        choices=[
            ("CSE", "CSE"),
            ("ECE", "ECE"),
            ("EEE", "EEE"),
            ("MECH", "MECH"),
            ("CIVIL", "CIVIL"),
        ],
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = NewQuestion
        fields = ['AcademicYear', 'Department', 'subject_code', 'subject_name', 'branch', 'year', 'semester', 'course_instructor', 'date', 'session']


