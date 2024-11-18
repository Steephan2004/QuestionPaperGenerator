from django.db import models
from django.utils import timezone

class NewQuestion(models.Model):
    time_choice=[
        ("FN","FN"),
        ("AN","AN")
    ]
    AcademicYear_choice=[
        ("2024-2025","2024-2025"),
        ("2025-2026","2025-2026"),
        ("2026-2027","2026-2027"),
        ("2027-2028","2027-2028"),
        ("2028-2029","2028-2029")
    ]
    # branch_choice=[
    #     ("CSE","CSE"),
    #     ("ECE","ECE"),
    #     ("EEE","EEE"),
    #     ("MECH","MECH"),
    #     ("CIVIL","CIVIL")
    # ]
    year_choice = [
    ("I", "I"),
    ("II", "II"),
    ("III", "III"),
    ("IV", "IV"),
    ]
    semester_choice = [
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
    ("6", "6"),
    ("7", "7"),
    ("8", "8"),
]
    semester_term_choice = [
        ("Odd", "Odd"),
        ("Even", "Even"),
    ]

    AcademicYear = models.CharField(max_length=20,choices=AcademicYear_choice)
    Department=models.CharField(max_length=50,default="Enter the department in full form(caps)")
    subject_code = models.CharField(max_length=10)
    subject_name = models.CharField(max_length=100)
    branch = models.CharField(max_length=100)
    year = models.CharField(max_length=20,choices=year_choice)
    semester = models.CharField(max_length=15,choices=semester_choice)
    semester_term = models.CharField(max_length=15,choices=semester_term_choice)
    course_instructor = models.CharField(max_length=100)
    date = models.DateField(default=timezone.now)
    session=models.CharField(max_length=5,choices=time_choice,null=True)

    def __str__(self):
        return f"{self.subject_name} ({self.subject_code})"

class Question(models.Model):
    MARK_CHOICES = [
        ('R,CO1', 'R,CO1'),
        ('U,CO1', 'U,CO1'),
        ('A,CO2', 'A,CO2'),
        ('Az,CO3', 'Az,CO3'),
        ('E,CO4', 'E,CO4'),
        ('C,CO5', 'C,CO5'),
    ]
    subject = models.ForeignKey('NewQuestion', on_delete=models.CASCADE, default=False)
    S_No = models.PositiveIntegerField(null=True,blank=True)
    question_text = models.TextField(null=True,blank=True)
    image = models.ImageField(upload_to='questions/', blank=True, null=True)  # Optional image
    BTlevel_COs = models.CharField(max_length=15, choices=MARK_CHOICES, null=True)  # New field for marks type
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def save(self, *args, **kwargs):
        if not self.pk:  # Only auto-increment when creating a new object
            last_question = Question.objects.filter(subject=self.subject).order_by('-S_No').first()
            if last_question:
                self.S_No = last_question.S_No + 1
            else:
                self.S_No = 1  # Start from 1 if no previous question exists for this subject
        super(Question, self).save(*args, **kwargs)
    def __str__(self):
        return f"{self.question_text} ({self.get_BTlevel_COs_display()})"
    
class Subject_Details(models.Model):
    semester_choices = [
        ('Odd', 'Odd'),
        ('Even', 'Even'),
    ]
    year_choices = [
        ('2024-2025', '2024-2025'),
        ('2025-2026', '2025-2026'),
        ('2026-2027', '2026-2027'),
        ('2027-2028', '2027-2028'),
        ('2028-2029', '2028-2029'),
    ]
    department_choices = [
        ('CSE', 'CSE'),
        ('ECE', 'ECE'),
        ('EEE', 'EEE'),
        ('CIVIL', 'CIVIL'),
        ('MECH', 'MECH'),
    ]
    year=models.CharField(choices=year_choices,max_length=15)
    semester=models.CharField(choices=semester_choices,max_length=5)
    department=models.CharField(choices=department_choices,max_length=30)
    staffname=models.CharField(max_length=50)
    subjectCode=models.CharField(max_length=10)
    subjectName=models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.subjectCode}"
class ExamCellUser(models.Model):
    username=models.CharField(max_length=20)
    password=models.CharField(max_length=10)
    
    def __str__(self):
        return f"{self.username}"
