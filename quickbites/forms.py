from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import User, Feedback

class UserRegistrationForm(UserCreationForm):
    """
    Custom registration form for users
    """
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your full name'
        })
    )
    uprn = forms.CharField(
        max_length=9,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your College ID'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })
    )
    
    class Meta:
        model = User
        fields = ('name', 'uprn', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['uprn']
        if commit:
            user.save()
        return user

class UserLoginForm(forms.Form):
    """
    Custom login form using College ID and password
    """
    uprn = forms.CharField,
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your College ID'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        uprn = cleaned_data.get('uprn')
        password = cleaned_data.get('password')
        
        if uprn and password:
            user = authenticate(username=uprn, password=password)
            if not user:
                raise forms.ValidationError("Invalid College ID or password.")
            if not user.is_active:
                raise forms.ValidationError("This account is inactive.")
        
        return cleaned_data

class FeedbackForm(forms.ModelForm):
    """
    Form for customer support (renamed from feedback)
    """
    class Meta:
        model = Feedback
        fields = ['subject', 'message']
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter subject'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter your message or feedback'
            })
        }
