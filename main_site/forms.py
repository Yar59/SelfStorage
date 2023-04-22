from django import forms
from phonenumber_field.formfields import PhoneNumberField

from main_site.models import User


class UserProfileForm(forms.ModelForm):
    username = forms.CharField(label='Имя', widget=forms.TextInput(
        attrs={'class': 'form-control fs_24 ps-2 SelfStorage__input', 'disabled': 'True', 'id': 'username'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(
        attrs={'class': 'form-control fs_24 ps-2 SelfStorage__input', 'disabled': 'True', 'id': 'email'}))

    password1 = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control fs_24 ps-2 SelfStorage__input', 'disabled': '', 'id': 'password1'}))
    password2 = forms.CharField(label='Подтверждение пароля',
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control fs_24 ps-2 SelfStorage__input', 'disabled': '', 'id': 'password2'}))
    phonenumber = PhoneNumberField(label='Номер телефона', widget=forms.TextInput(
        attrs={'class': 'form-control fs_24 ps-2 SelfStorage__input', 'disabled': 'True', 'id': 'phonenumber'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'phonenumber')
