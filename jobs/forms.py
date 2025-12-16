from django import forms
from .models import Job


class JobForm(forms.ModelForm):
    """Жумуш жарыялоо формасы"""
    
    class Meta:
        model = Job
        fields = ['title', 'description', 'category', 'job_type', 'price', 
                  'location', 'contact_phone', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Мисалы: Үй тазалоо керек'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Жумуштун толук сүрөттөмөсүн жазыңыз...'
            }),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'job_type': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Баа (сом)'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Мисалы: Бишкек, Ала-Тоо район'
            }),
            'contact_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+996 XXX XXX XXX'
            }),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Аталышы',
            'description': 'Сүрөттөмө',
            'category': 'Категория',
            'job_type': 'Жумуштун түрү',
            'price': 'Баасы (сом)',
            'location': 'Жайгашкан жер',
            'contact_phone': 'Байланыш телефону',
            'image': 'Сүрөт (милдеттүү эмес)',
        }
