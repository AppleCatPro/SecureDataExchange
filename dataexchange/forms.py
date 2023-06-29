from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser, ConfidentialData, Message

#
# class CustomUserForm(forms.ModelForm):
#     class Meta:
#         model = CustomUser
#         fields = ('username', 'email', 'last_name', 'first_name', 'birth_date', 'gender', 'photo', 'city', 'country')


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'last_name', 'first_name', 'birth_date', 'gender', 'photo', 'city', 'country')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'last_name', 'first_name', 'birth_date', 'gender', 'photo', 'city', 'country')


class CustomUserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'last_name', 'first_name', 'birth_date', 'gender', 'photo', 'city', 'country')


class ConfidentialDataForm(forms.ModelForm):
    class Meta:
        model = ConfidentialData
        fields = ('title', 'data')


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('sender', 'recipient', 'subject', 'content', 'attached_data', 'is_read')
