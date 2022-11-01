from django import forms
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm


User = get_user_model()


class UserCreationForm(UserCreationForm):
    email = forms.EmailField(label=_("Email"), max_length=254, widget=forms.EmailInput(attrs={"autocomplete": "email"}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = {'username', 'email'}


class NFTCollectionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["category"].empty_label = "Без категории"


class NFTDrawForm(forms.ModelForm):
    def clean_start_date(self):
        start_date = self.cleaned_data.get("start_date")

        if timezone.now() > start_date:
            raise forms.ValidationError("Дата и время должны быть больше текущих!")

        return start_date

    def clean_finish_date(self):
        finish_date = self.cleaned_data.get("finish_date")

        if timezone.now() > finish_date:
            raise forms.ValidationError("Дата и время должны быть больше текущих!")

        return finish_date

    def clean(self):
        start_date = self.cleaned_data.get("start_date")
        finish_date = self.cleaned_data.get("finish_date")
        if start_date and finish_date and not (finish_date > start_date):
            raise forms.ValidationError("Дата и время конца розыгрыша должная быть больше даты и времени старта!")
        return super(NFTDrawForm, self).clean()


class NFTSaleForm(forms.ModelForm):
    def clean_start_date(self):
        start_date = self.cleaned_data.get("start_date")

        if timezone.now() > start_date:
            raise forms.ValidationError("Дата и время должны быть больше текущих!")

        return start_date

    def clean_finish_date(self):
        finish_date = self.cleaned_data.get("finish_date")

        if timezone.now() > finish_date:
            raise forms.ValidationError("Дата и время должны быть больше текущих!")

        return finish_date

    def clean(self):
        start_date = self.cleaned_data.get("start_date")
        finish_date = self.cleaned_data.get("finish_date")
        if start_date and finish_date and not (finish_date > start_date):
            raise forms.ValidationError("Дата и время конца розыгрыша должная быть больше даты и времени старта!")
        return super(NFTSaleForm, self).clean()
