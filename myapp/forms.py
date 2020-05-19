from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from myapp.models import *

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30,widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=30,widget=forms.PasswordInput)
    email = forms.CharField(max_length=50,widget=forms.EmailInput())
    first_name = forms.CharField(max_length=20)
    last_name =forms.CharField(max_length=20)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords did not match.")
        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30,label="Username")
    password = forms.CharField(max_length=30,label="Password",widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Invalid username/password")
        return cleaned_data

class RequestForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title','image','description','budget')
        widgets={
            'image':forms.FileInput(),
            'description':forms.Textarea(attrs={'id':'description','placeholder':'Describe the task here...'}),
            'title': forms.TextInput(attrs={'required':True,'placeholder':'Enter title here'}),
            'budget':forms.NumberInput(attrs={'required':True,'placeholder':'In USD'})
        }

class WorkForm(forms.ModelForm):
    class Meta:
        model = Work
        fields = ('image', 'description')
        widgets={
            'image':forms.FileInput(),
            'description': forms.Textarea(attrs={'placeholder':'Write a description here...'})
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar','bio')
        widgets = {
            'avatar':forms.FileInput,
            'bio': forms.Textarea(attrs={'placeholder':'Write something about you'})
        }