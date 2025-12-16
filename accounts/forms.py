from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    """Регистрация формасы"""
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Колдонуучу аты',
            'email': 'Электрондук почта',
        }
        help_texts = {
            'username': 'Латын тамгалары жана сандар колдонулат.',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Колдонуучу аты'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Сыр сөз'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Сыр сөздү кайталаңыз'})
        self.fields['password1'].label = 'Сыр сөз'
        self.fields['password2'].label = 'Сыр сөздү кайталоо'


class ProfileUpdateForm(forms.ModelForm):
    """Профилди жаңыртуу формасы"""
    
    class Meta:
        model = Profile
        fields = ['user_type', 'phone', 'location', 'bio', 'avatar']
        widgets = {
            'user_type': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+996 XXX XXX XXX'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Сиздин шаарыңыз/айылыңыз'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Өзүңүз жөнүндө кыскача...'
            }),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'user_type': 'Сиз ким?',
            'phone': 'Телефон',
            'location': 'Жайгашкан жер',
            'bio': 'Өзү жөнүндө',
            'avatar': 'Профиль сүрөтү',
        }


class UserUpdateForm(forms.ModelForm):
    """Колдонуучу маалыматын жаңыртуу"""
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Атыңыз'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Фамилияңыз'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
        }
        labels = {
            'first_name': 'Аты',
            'last_name': 'Фамилия',
            'email': 'Email',
        }
