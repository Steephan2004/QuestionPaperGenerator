from rest_framework import serializers
from .models import NewQuestion, Question, Subject_Details, ExamCellUser

# Serializer for Subject Model
class NewQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewQuestion
        fields = ['AcademicYear','Department','subject_code', 'subject_name', 'branch', 'year', 'semester', 'course_instructor', 'date','session']

# Serializer for Question Model
class QuestionSerializer(serializers.ModelSerializer):
    subject = NewQuestionSerializer(read_only=True)  # Nested serializer for the subject field
    subject_id = serializers.PrimaryKeyRelatedField(queryset=NewQuestion.objects.all(), source='subject', write_only=True)
    
    class Meta:
        model = Question
        fields = [ 'subject', 'subject_id', 'question_text', 'image', 'BTlevel,COs', 'created_at']

# Serializer for Subject_Details Model
class SubjectDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject_Details
        fields = "__all__"

# Serializer for ExamCellUser Model
class ExamCellUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamCellUser
        fields = ['username', 'password']
        
