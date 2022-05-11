from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(NewUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'input',
            'placeholder': "Nazwa użytkownika"
        })
        self.fields['email'].widget.attrs.update({
            'class': 'input',
            "placeholder": "Adres e-mail"
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'input',
            "placeholder": "Hasło"
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'input',
            "placeholder": "Potwierdź hasło"
        })

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class AuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'input',
            'placeholder': "Nazwa użytkownika"
        })
        self.fields['password'].widget.attrs.update({
            'class': 'input',
            "placeholder": "Hasło"
        })