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
    first_name = forms.CharField(max_length=100, label='Prénom')
    last_name = forms.CharField(max_length=100, label='Nom')
    email = forms.EmailField(label='Email')
    phone_number = forms.CharField(max_length=15, label='Numéro de téléphone')
    command_details = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5}),
        label='Entrez vos informations (Quantité, Adresse, etc.)'
    )

    class Meta:
        model = Command
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'command_details']