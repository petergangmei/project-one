from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from projectone.models import *


# Create your views here.
def index(request):
    return render(request,'projectone/index.html')

def top_companies(request):
    top_c = Company.objects.all()
    context ={
        'top_companies':top_c
    }
    return render(request, 'projectone/top-companies.html',context)

@login_required
def company_detail(request,slug):
    company = Company.objects.get(slug=slug)
    context ={
        'company':company,
    }
    return render(request, 'projectone/company-detail.html',context)

def add_company(request):
    if request.method == 'POST':
        cname = request.POST.get('cname')
        cabout= request.POST.get('cabout')

        Company.objects.create(name=cname,about=cabout,user=request.user)
        return redirect(reverse('account:profile'))


def delete_company(request):
    if request.method == 'POST':
        slug = request.POST.get('slug')
        c = Company.objects.get(slug=slug)
        c.delete()

        return redirect(reverse('account:profile'))