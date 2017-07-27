from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    
    def __init__(self, *args, **kwargs):
       super(RegisterForm, self).__init__(*args, **kwargs)
       del self.fields['password1']
       del self.fields['password2']

    company_name = forms.CharField(max_length=30, 
        required=True, help_text='Required.')
    web_domain = forms.CharField(max_length=30, 
        required=True, help_text='Required.')

    class Meta:
        model = User
        fields = ('company_name', 'web_domain')