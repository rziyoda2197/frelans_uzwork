from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegisterForm(UserCreationForm):
    """User registration form with role selection."""
    role = forms.ChoiceField(
        choices=[('client', 'Buyurtmachi'), ('freelancer', 'Frilanser')],
        widget=forms.RadioSelect(attrs={'class': 'role-radio'}),
        label="Rolni tanlang"
    )
    email = forms.EmailField(required=True, label="Email")
    first_name = forms.CharField(max_length=50, required=True, label="Ism")
    last_name = forms.CharField(max_length=50, required=True, label="Familiya")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'role', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'role':
                field.widget.attrs['class'] = 'form-input'
            field.widget.attrs['placeholder'] = field.label
        self.fields['password1'].label = "Parol"
        self.fields['password2'].label = "Parolni tasdiqlash"


class LoginForm(forms.Form):
    """Login form."""
    username = forms.CharField(
        max_length=150, label="Foydalanuvchi nomi",
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Foydalanuvchi nomi'})
    )
    password = forms.CharField(
        label="Parol",
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Parol'})
    )


class ProfileForm(forms.ModelForm):
    """Profile edit form."""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'bio', 'skills',
                  'location', 'portfolio_url', 'avatar']
        labels = {
            'first_name': 'Ism',
            'last_name': 'Familiya',
            'email': 'Email',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'avatar':
                field.widget.attrs['class'] = 'form-file'
            elif field_name == 'bio':
                field.widget.attrs['class'] = 'form-textarea'
                field.widget.attrs['rows'] = 4
            else:
                field.widget.attrs['class'] = 'form-input'
