from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from app.views import *
from rest_framework import routers
from app import views

router=routers.DefaultRouter()
router.register(r'subjects', NewQuestionViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'subject-details', SubjectDetailsViewSet)
router.register(r'users', ExamCellUserViewSet)
urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('pdf/', pdf_view, name='pdf_view'),
    path('check/',views.check),
    path('get_subjects',views.get_subjects),
    path('staff_dash/', admin_dashboard, name='admin_dashboard'),
    path('newquestion/add/', add_new_question, name='add_new_question'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
