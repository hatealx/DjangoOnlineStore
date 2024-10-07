from django.contrib.auth import get_user_model
from django import forms
from .models import Command

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'email']
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Passwords don't match.")
        return cd['password2']


class CommandForm(forms.ModelForm):
    class Meta:
        model = Command
        fields = ['details']
        widgets = {
            'details': forms.Textarea(attrs={'placeholder': 'Entrer la quantité, l\'adresse, and autres detail de livraison'})
        }
