from .serializers import *
from .models import *
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework import viewsets
from django.template.loader import render_to_string
import pdfkit
import random
import os
import base64
from django.shortcuts import render, redirect
from .forms import NewQuestionForm, QuestionForm
from django.forms import modelformset_factory
from django.conf import settings

class NewQuestionViewSet(viewsets.ModelViewSet):
    queryset = NewQuestion.objects.all()
    serializer_class = NewQuestionSerializer

# ViewSet for Question Model
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

# ViewSet for Subject_Details Model
class SubjectDetailsViewSet(viewsets.ModelViewSet):
    queryset = Subject_Details.objects.all()
    serializer_class = SubjectDetailsSerializer

# ViewSet for User Model
class ExamCellUserViewSet(viewsets.ModelViewSet):
    queryset = ExamCellUser.objects.all()
    serializer_class = ExamCellUserSerializer

def image_to_base64(image_field):
    """Helper function to convert image to base64 and handle both PNG and JPG."""
    if not image_field or not image_field.name:
        return None
    try:
        # Construct the full path for the image
        full_path = os.path.join(settings.MEDIA_ROOT, image_field.name)

        # Open the image file in binary mode
        with open(full_path, "rb") as image_file:
            # Get the file extension
            file_extension = image_field.name.split('.')[-1].lower()
            
            # Determine the correct MIME type
            mime_type = 'image/jpeg' if file_extension in ['jpg', 'jpeg'] else 'image/png'
            print(f"data:{mime_type};base64,")
            # Convert image to base64
            return f"data:{mime_type};base64," + base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        return None
def add_new_question(request):
    return render(request,"admin/edit_inline/g.html")
def admin_dashboard(request):
    return render(request, 'admin/edit_inline/admin_dashboard.html')
def pdf_view(request):
    if request.method == 'GET':
        subject_code = request.GET.get('subject_code')
        dept=request.GET.get('dept')
        year=request.GET.get('year')
        semester=request.GET.get('sem')
        modified_subject_code=subject_code.replace(" ","").upper()
        print(modified_subject_code)
        # Generate random question selections
        marks_2 = random.sample(range(1, 15), 7)
        marks_8 = random.sample(range(15, 17), 1)
        marks_13 = random.sample(range(17, 19), 1)
        marks_15 = random.sample(range(19, 21), 1)
        total_marks = marks_2 + marks_8 + marks_13 + marks_15
        print(f"Selected Question IDs: {total_marks}")
        print(f"Modified Subject Code: {modified_subject_code}")
        print(f"Total Marks IDs: {total_marks}")
        # Query the Questions model using the subject code and selected IDs
        questions = Question.objects.filter(subject__subject_code=modified_subject_code,subject__AcademicYear=year, S_No__in=total_marks,subject__semester_term=semester)
        print(questions)

        if not questions.exists():
            return JsonResponse({'error': 'No questions found for the given subject.'}, status=404)

        # Convert each question's image to base64
        questions_with_base64 = []
        for question in questions:
            question_dict = {
                'question_text': question.question_text,
                'id': question.id,
                'BTlevel_COs':question.BTlevel_COs,
                'image_base64': image_to_base64(question.image) if question.image else None
            }
            questions_with_base64.append(question_dict)

        # Query the subjects based on subject_code
        subjects = NewQuestion.objects.filter(subject_code=subject_code)

        # Render HTML using the Django template
        context = {
            'questions': questions_with_base64,
            'subjects': subjects
        }
        

        html_content = render_to_string('pdf_report.html', context)
        config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')

        # Generate the PDF from HTML content
        try:
            pdf = pdfkit.from_string(html_content, False, configuration=config)
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="questions.pdf"'
            return response
        except Exception as e:
            return JsonResponse({'error': f"PDF generation failed: {str(e)}"}, status=500)

def check(request):
    if request.method == 'GET':
        print(request.GET.keys())
        print("name:", request.GET['name'])
        print("password:", request.GET['password'])
        try:
            user = ExamCellUser.objects.get(username=request.GET['name'], password=request.GET['password'])
            print("User logged in ", user)
            if user:
                return JsonResponse({"status": True})
            else:
                return JsonResponse({"status": False})
        except ExamCellUser.DoesNotExist:
            pass

        # Return False if user not found
        return JsonResponse({"status": False})

def get_subjects(request):
    if request.method == "GET":
        data = Subject_Details.objects.values()
        return JsonResponse(list(data), safe=False)

def add_new_question(request):
    if request.method == 'POST':
        new_question_form = NewQuestionForm(request.POST)
        question_formset = QuestionForm(request.POST, request.FILES)

        if new_question_form.is_valid() and question_formset.is_valid():
            new_question = new_question_form.save()
            questions = question_formset.save(commit=False)

            for question in questions:
                question.subject = new_question  # Assign the NewQuestion instance to each Question
                question.save()

            return redirect('success')  # Redirect to a success page or the admin dashboard
    else:
        new_question_form = NewQuestionForm()
        question_formset = QuestionForm()  # No queryset argument here

    return render(request, 'admin/edit_inline/g.html', {
        'new_question_form': new_question_form,
        'question_formset': question_formset,
    })