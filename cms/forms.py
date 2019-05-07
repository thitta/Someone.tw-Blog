from django.forms import CharField, Form, ModelForm, HiddenInput, \
    Textarea, TextInput, CheckboxInput, PasswordInput

from .models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["Title", "Subtitle", "BodyMarkdown", "CoverImageUrl",
                  "IsPublic", "IsOnList", "IsTop", "RankingIndex", ]
        widgets = {
            "Title": TextInput(attrs={"class": "form-control", "placeholder": "*Title"}),
            "Subtitle": TextInput(attrs={"class": "form-control", "placeholder": "*Subtitle"}),
            "CoverImageUrl": TextInput(attrs={"class": "form-control", "placeholder": "Cover Image URL"}),
            "BodyMarkdown": Textarea(attrs={"class": "form-control", "placeholder": "*Body(Markdown)"}),
            "IsPublic": CheckboxInput(attrs={"class": "form-check-input"}),
            "IsOnList": CheckboxInput(attrs={"class": "form-check-input"}),
            "IsTop": CheckboxInput(attrs={"class": "form-check-input"}),
            "RankingIndex": TextInput(attrs={"class": "form-control", "placeholder": "Ranking Index"}),
        }


class LoginForm(Form):
    username = CharField(max_length=150,
                         widget=TextInput(attrs={"class": "form-control", "placeholder": "account"}))
    password = CharField(max_length=32,
                         widget=PasswordInput(attrs={"class": "form-control", "placeholder": "password"}))
