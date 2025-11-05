from django.urls import path
from . import views

app_name = 'site_portfolio'

urlpatterns = [
    path('', views.index, name='index'),
    path('projects/<slug:slug>/', views.project_detail, name='project_detail'),
    path('contact/', views.contact, name='contact'),
    path('resume/download/', views.download_resume, name='download_resume'),
]
