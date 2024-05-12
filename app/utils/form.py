from app import models
from django import forms
from app.utils.encrypt import md5

class ProblemForm(forms.ModelForm):
    class Meta:
        model = models.FavoriteProblem
        fields = ['title', 'link', 'category', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'link': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class UserForm(forms.ModelForm):
    confirm_password = forms.CharField(label='confirm_password')

    class Meta:
        model = models.UserInfo
        fields = ['username', 'password', 'confirm_password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}, render_value=True),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['confirm_password'].widget = forms.PasswordInput(attrs={
            'type': 'password',
            'class': 'form-control'}, render_value=True)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        return md5(password)

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = md5(self.cleaned_data.get('confirm_password'))
        if password != confirm_password:
            raise forms.ValidationError('Passwords must match')
        return confirm_password


class LoginForm(forms.Form):
    username = forms.CharField(
        label='username',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    password = forms.CharField(
        label='password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}, render_value=True),
    )

    def clean_password(self):
        password = self.cleaned_data.get('password')
        return md5(password)


