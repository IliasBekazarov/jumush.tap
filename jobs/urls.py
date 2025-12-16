from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/create/', views.job_create, name='job_create'),
    path('jobs/my/', views.my_jobs, name='my_jobs'),
    path('jobs/applications/', views.my_applications, name='my_applications'),
    path('jobs/<slug:slug>/', views.job_detail, name='job_detail'),
    path('jobs/<slug:slug>/edit/', views.job_edit, name='job_edit'),
    path('jobs/<slug:slug>/delete/', views.job_delete, name='job_delete'),
    path('jobs/<slug:slug>/apply/', views.job_apply, name='job_apply'),
    path('jobs/<slug:slug>/applications/', views.job_applications, name='job_applications'),
]
