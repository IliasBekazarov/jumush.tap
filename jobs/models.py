from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Category(models.Model):
    """Жумуш категориялары"""
    name = models.CharField(max_length=100, unique=True, verbose_name='Аталышы')
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text='FontAwesome icon class')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категориялар'
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Job(models.Model):
    """Жумуш жарыялары"""
    JOB_TYPE_CHOICES = [
        ('onetime', 'Бир жолку'),
        ('daily', 'Күнүмдүк'),
        ('parttime', 'Подработка'),
        ('fulltime', 'Толук жумуш'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Активдүү'),
        ('completed', 'Аткарылды'),
        ('cancelled', 'Жокко чыгарылды'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='Аталышы')
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(verbose_name='Сүрөттөмө')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='jobs', verbose_name='Категория')
    job_type = models.CharField(max_length=10, choices=JOB_TYPE_CHOICES, default='onetime', verbose_name='Түрү')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Баасы (сом)', help_text='Баа сомдо көрсөтүлөт')
    location = models.CharField(max_length=200, verbose_name='Жайгашкан жер')
    employer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_jobs', verbose_name='Жарыялаган')
    contact_phone = models.CharField(max_length=20, verbose_name='Байланыш телефону')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active', verbose_name='Статус')
    image = models.ImageField(upload_to='job_images/', blank=True, null=True, verbose_name='Сүрөт')
    views_count = models.PositiveIntegerField(default=0, verbose_name='Көрүүлөр')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Түзүлгөн убакыт')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Жаңыртылган убакыт')
    
    class Meta:
        verbose_name = 'Жумуш'
        verbose_name_plural = 'Жумуштар'
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Job.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def increment_views(self):
        """Көрүүлөрдү көбөйтүү"""
        self.views_count += 1
        self.save(update_fields=['views_count'])


class JobApplication(models.Model):
    """Жумушка өтүнмөлөр"""
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications', verbose_name='Жумуш')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_applications', verbose_name='Өтүнүүчү')
    message = models.TextField(blank=True, verbose_name='Билдирүү')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Өтүнгөн убакыт')
    
    class Meta:
        verbose_name = 'Өтүнмө'
        verbose_name_plural = 'Өтүнмөлөр'
        unique_together = ['job', 'applicant']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.applicant.username} -> {self.job.title}"
