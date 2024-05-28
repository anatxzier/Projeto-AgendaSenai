from django import forms

class FormLogin(forms.Form):
    user = forms.CharField(label="User", max_length=20)
    password = forms.CharField(widget=forms.PasswordInput())
