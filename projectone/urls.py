from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add-company/', views.add_company, name='add-company'),
    path('delete-company/', views.delete_company, name='delete-company'),
    path('top_companies/', views.top_companies, name='top-companies'),
    path('company-detail/<slug>/', views.company_detail, name='company-detail'),
]