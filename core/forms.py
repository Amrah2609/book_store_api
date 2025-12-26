import email
from django import forms
from django.contrib.auth.models import User
from core.models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Name",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "Email",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "placeholder": "Phone",
                }
            ),
            "message": forms.TextInput(
                attrs={
                    "placeholder": "Message",
                    "class": "message-box",
                }
            ),
        }


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Username",
            }
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password",
            }
        ),
        max_length=200,
    )


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password",
            }
        ),
        max_length=200,
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirm Password",
            }
        ),
        max_length=200,
        label="Confirm Password",
    )

    class Meta:
        model = User
        fields = ["username", "email", "password"]
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter your username"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Enter your email"}
            ),
        }

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("password2")
        if password != confirm_password:
            raise forms.ValidationError("Passwords don't match")
        return cleaned_data
