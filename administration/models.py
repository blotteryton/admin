from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from solo.models import SingletonModel


class Project(models.Model):
    class Languages(models.TextChoices):
        RUSSIAN = "RUSSIAN", "Русский"
        ENGLISH = "ENGLISH", "English"

    name = models.CharField(max_length=255)
    language = models.CharField(max_length=255, choices=Languages.choices)
    channel_link = models.URLField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"


class ProjectMember(models.Model):
    project = models.ForeignKey(Project, on_delete=models.PROTECT)
    name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    email = models.EmailField(max_length=255)
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=255)

    avatar = models.ImageField(upload_to="blogger_avatars/", blank=True, null=True)
    cover = models.ImageField(upload_to="blogger_covers/", blank=True, null=True)

    user = models.ForeignKey("users.User", on_delete=models.PROTECT, blank=True, null=True)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.user:
            User = get_user_model()

            user = User(first_name=self.name, last_name=self.last_name, email=self.email, username=self.username)
            user.is_staff = True
            user.save()

            user.set_password(self.password)
            user.save()

            bloggers_group = Group.objects.get(name='bloggers')
            bloggers_group.user_set.add(user)

            self.user = user
        else:
            self.user.first_name = self.name
            self.user.last_name = self.last_name
            self.user.email = self.email
            self.user.username = self.username
            self.user.avatar = self.avatar
            self.user.cover = self.cover

            if not self.user.check_password(self.password):
                self.user.set_password(self.password)

            self.user.save()

        return super(ProjectMember, self).save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Project Member"
        verbose_name_plural = "Project Members"


class Configuration(SingletonModel):
    collection_create_royalty = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True, validators=[
            MinValueValidator(0.0099)
        ])
    collection_create_royalty_address = models.CharField(max_length=255, blank=True, null=True)

    collection_create_external_link = models.URLField(blank=True, null=True)
    collection_create_seller_fee_basis_points = models.PositiveIntegerField(validators=[
            MaxValueValidator(10000),
            MinValueValidator(1)
        ], blank=True, null=True)
    collection_create_fee_recipient = models.CharField(
        max_length=255, blank=True, null=True, help_text="use \"self\" for the address of the collection's creator."
    )
    collection_create_amount = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True, validators=[
            MinValueValidator(0.0099)
        ])

    nft_create_amount = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True, validators=[
        MinValueValidator(0.0099)
    ])

    nft_item_content_base_uri = models.CharField(max_length=255, blank=True, null=True)

    nft_marketplace_fee = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True, validators=[
            MinValueValidator(0.0099)
        ])
    nft_create_royalty = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True, validators=[
            MinValueValidator(0.0099)
        ])

    def is_configured(self):
        return all(self.__getattribute__(field.name) for field in self._meta.fields)

    def __str__(self):
        return "Configuration"

    class Meta:
        verbose_name = "Configuration"
        verbose_name_plural = "Configuration"


class MarketplaceConfiguration(SingletonModel):
    recommended_collections = models.ManyToManyField("nft.CollectionNFT", related_name="recommended_collections")
    popular_collections = models.ManyToManyField("nft.CollectionNFT", related_name="popular_collections")
    recommended_authors = models.ManyToManyField("users.User")

    marketplace_address = models.CharField(max_length=255, blank=True, null=True)
    marketplace_deployed = models.BooleanField(default=False)

    def __str__(self):
        return "Marketplace configuration"

    class Meta:
        verbose_name = "Marketplace configuration"
        verbose_name_plural = "Marketplace configuration"
