from django import forms 
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Request


class SignInForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=[('user', 'User'), ('admin', 'Admin')])

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")


from django import forms
from .models import Request

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['requirement', 'email', 'phone', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
