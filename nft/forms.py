from django import forms
from django.utils import timezone

from administration.models import Configuration
from api.v1.account.utils import create_transfer
from nft.utils import create_collection, create_nft
from users.utils import create_nft_sale


class NFTCollectionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.address = kwargs.pop('address', None)
        self.request = kwargs.pop('request', None)

        super().__init__(*args, **kwargs)

        if not self.instance or self.instance.pk is None:
            self.fields["categories"].empty_label = "Без категории"

        for field in ("name", "description", "image"):
            if form_field := self.fields.get(field):
                form_field.required = True

    def clean_user(self, value):
        return self.request.user

    def clean(self):
        clean = super(NFTCollectionForm, self).clean()

        if not self.instance.address:
            configuration = Configuration.get_solo()
            if (configuration.collection_create_amount
                    and self.request.user.wallet_balance < configuration.collection_create_amount):
                raise forms.ValidationError(f"Not enough money (TON {configuration.collection_create_amount})")

            try:
                response = create_collection(user=self.request.user, **clean)
                if not type(response) == dict or not response.get("address"):
                    raise forms.ValidationError(response)
                address = response.get("address")
            except Exception as e:
                print(e)
                raise forms.ValidationError("Something went wrong..")

            if not address:
                raise forms.ValidationError("Something went wrong..")

            self.address = address

        return clean

    def save(self, commit=True):
        self.instance.user = self.request.user
        self.instance.address = self.address

        return super(NFTCollectionForm, self).save(commit)


class NFTForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.index = kwargs.pop('index', None)
        self.address = kwargs.pop('address', None)
        self.request = kwargs.pop('request', None)
        self.sale_address = kwargs.pop('sale_address', None)

        super().__init__(*args, **kwargs)

        for field in ("collection", "name", "description", "price", "image"):
            if form_field := self.fields.get(field):
                form_field.required = True

    def clean_user(self, value):
        return self.request.user

    def clean(self):
        clean = super(NFTForm, self).clean()

        if not self.instance.address:
            configuration = Configuration.get_solo()
            user = self.request.user

            if (configuration.nft_create_amount
                    and user.wallet_balance < configuration.nft_create_amount):
                raise forms.ValidationError(f"Not enough money (TON {configuration.nft_create_amount})")

            if configuration.nft_create_amount and clean.get("price", 0) < configuration.nft_create_amount:
                raise forms.ValidationError({"price": f"Minimal value: TON {configuration.nft_create_amount}"})

            if clean.get("price", 0) > user.wallet_balance:
                raise forms.ValidationError({"price": f"Not enough money: TON {user.wallet_balance}"})

            try:
                nft_info = create_nft(user=user, **clean)
                address = nft_info.get("address")
                index = nft_info.get("index")

            except Exception as e:
                print(e)
                raise forms.ValidationError("Something went wrong..")

            if not address:
                raise forms.ValidationError("Something went wrong..")

            self.address = address
            self.index = index

            collection_address = clean.get("collection").address
            price = clean.get("price")

            create_transfer(source_wallet=user.wallet_address, mnemonic=user.wallet_mnemonic,
                            dest_wallet=collection_address, amount=price, comment="nft create")

            sale = create_nft_sale(nft_address=address, full_price=price, collection_address=collection_address)

            sale_address = sale.get("address")
            self.sale_address = sale_address

        return clean

    def save(self, commit=True):
        self.instance.index = self.index
        self.instance.address = self.address
        self.instance.user = self.request.user
        self.instance.sale_address = self.sale_address

        return super(NFTForm, self).save(commit)


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
