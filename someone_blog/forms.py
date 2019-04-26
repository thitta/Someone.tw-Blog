from django.forms import CharField, Form, TextInput, PasswordInput


class LoginForm(Form):
    username = CharField(max_length=150,
                         widget=TextInput(attrs={"class": "form-control", "placeholder": "account"}))
    password = CharField(max_length=32,
                         widget=PasswordInput(attrs={"class": "form-control", "placeholder": "password"}))
