from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from authors.models import Registration

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'id': 'required'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'id': 'required'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'id': 'required'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def save(self, commit=True):
        our_user = super().save(commit=False)

        if commit:
            our_user.save()

            Registration.objects.create(
                user = our_user
            )
            return our_user
        

    