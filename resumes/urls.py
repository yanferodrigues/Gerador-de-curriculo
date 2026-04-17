from django.urls import path
from . import views

app_name = 'resumes'

urlpatterns = [
    # Pages
    path('',                           views.index_view,          name='index'),
    path('dashboard/',                 views.dashboard_view,      name='dashboard'),
    path('builder/',                   views.builder_view,        name='builder'),
    path('builder/<uuid:pk>/',         views.builder_view,        name='builder_edit'),
    path('preview/<uuid:pk>/',         views.preview_view,        name='preview'),
    path('delete/<uuid:pk>/',          views.delete_resume_view,  name='delete_resume'),

    # API (chamadas AJAX do frontend JS)
    path('api/resumes/',            views.api_resume_list,   name='api_resume_list'),
    path('api/resumes/<uuid:pk>/',  views.api_resume_detail, name='api_resume_detail'),
]
