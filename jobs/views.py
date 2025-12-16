from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Job, Category, JobApplication
from .forms import JobForm


def home(request):
    """Башкы барак - акыркы жумуштар"""
    jobs = Job.objects.filter(status='active').select_related('category', 'employer')[:12]
    categories = Category.objects.all()
    
    context = {
        'jobs': jobs,
        'categories': categories,
    }
    return render(request, 'jobs/home.html', context)


def job_list(request):
    """Бардык жумуштардын тизмеси фильтрлер менен"""
    jobs = Job.objects.filter(status='active').select_related('category', 'employer')
    
    # Фильтрлөө
    category_slug = request.GET.get('category')
    job_type = request.GET.get('type')
    location = request.GET.get('location')
    search = request.GET.get('search')
    
    if category_slug:
        jobs = jobs.filter(category__slug=category_slug)
    
    if job_type:
        jobs = jobs.filter(job_type=job_type)
    
    if location:
        jobs = jobs.filter(location__icontains=location)
    
    if search:
        jobs = jobs.filter(
            Q(title__icontains=search) | 
            Q(description__icontains=search)
        )
    
    categories = Category.objects.all()
    
    context = {
        'jobs': jobs,
        'categories': categories,
        'selected_category': category_slug,
        'selected_type': job_type,
    }
    return render(request, 'jobs/job_list.html', context)


def job_detail(request, slug):
    """Жумуштун толук маалыматы"""
    job = get_object_or_404(Job, slug=slug)
    job.increment_views()
    
    # Колдонуучу мурда өтүнгөнбү текшерүү
    has_applied = False
    if request.user.is_authenticated:
        has_applied = JobApplication.objects.filter(
            job=job, 
            applicant=request.user
        ).exists()
    
    context = {
        'job': job,
        'has_applied': has_applied,
    }
    return render(request, 'jobs/job_detail.html', context)


@login_required
def job_create(request):
    """Жумуш жарыялоо"""
    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user
            job.save()
            messages.success(request, 'Жумуш ийгиликтүү жарыяланды!')
            return redirect('job_detail', slug=job.slug)
    else:
        form = JobForm()
    
    return render(request, 'jobs/job_form.html', {'form': form})


@login_required
def job_edit(request, slug):
    """Жумушту түзөтүү"""
    job = get_object_or_404(Job, slug=slug, employer=request.user)
    
    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Жумуш ийгиликтүү жаңыртылды!')
            return redirect('job_detail', slug=job.slug)
    else:
        form = JobForm(instance=job)
    
    return render(request, 'jobs/job_form.html', {'form': form, 'job': job})


@login_required
def job_delete(request, slug):
    """Жумушту өчүрүү"""
    job = get_object_or_404(Job, slug=slug, employer=request.user)
    
    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Жумуш ийгиликтүү өчүрүлдү!')
        return redirect('my_jobs')
    
    return render(request, 'jobs/job_confirm_delete.html', {'job': job})


@login_required
def job_apply(request, slug):
    """Жумушка өтүнүү"""
    job = get_object_or_404(Job, slug=slug, status='active')
    
    # Экинчи жолу өтүнбөс үчүн
    if JobApplication.objects.filter(job=job, applicant=request.user).exists():
        messages.warning(request, 'Сиз мурда эле бул жумушка өтүндүңүз!')
        return redirect('job_detail', slug=slug)
    
    if request.method == 'POST':
        message = request.POST.get('message', '')
        JobApplication.objects.create(
            job=job,
            applicant=request.user,
            message=message
        )
        messages.success(request, 'Өтүнмөңүз жиберилди!')
        return redirect('job_detail', slug=slug)
    
    return render(request, 'jobs/job_apply.html', {'job': job})


@login_required
def my_jobs(request):
    """Менин жарыялаган жумуштарым"""
    jobs = Job.objects.filter(employer=request.user).order_by('-created_at')
    return render(request, 'jobs/my_jobs.html', {'jobs': jobs})


@login_required
def my_applications(request):
    """Менин өтүнмөлөрүм"""
    applications = JobApplication.objects.filter(
        applicant=request.user
    ).select_related('job').order_by('-created_at')
    return render(request, 'jobs/my_applications.html', {'applications': applications})


@login_required
def job_applications(request, slug):
    """Жумушка келген өтүнмөлөр (жумуш берүүчү үчүн)"""
    job = get_object_or_404(Job, slug=slug, employer=request.user)
    applications = job.applications.select_related('applicant').order_by('-created_at')
    return render(request, 'jobs/job_applications.html', {
        'job': job, 
        'applications': applications
    })
