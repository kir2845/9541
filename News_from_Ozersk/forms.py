from django import forms
from django.core.exceptions import ValidationError

from .models import New


class NewForm(forms.ModelForm):
    textPost = forms.CharField(min_length=100)

    class Meta:
       model = New
       fields = ['name', 'author', 'textPost']

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        textPost = cleaned_data.get("textPost")

        if name == textPost:
            raise ValidationError(
                "Описание новости/статьи не должно быть идентично её заголовку"
            )

        return cleaned_data